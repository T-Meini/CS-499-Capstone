import pandas as pd
from flask import Flask, render_template, jsonify, request
import plotly.express as px
import plotly.graph_objects as go
import json
import plotly
import base64
import os
from pymongo import MongoClient
import logging
from crud import MongoCRUD
from collections import OrderedDict
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LRUCache:
    def __init__(self, capacity=50):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            # Update existing key
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used (first item)
            self.cache.popitem(last=False)
        
        self.cache[key] = value

# Initialize cache
search_cache = LRUCache(50)

class MongoDataManager:
    """Data management class to handle MongoDB operations"""
    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", 
                 database_name="animal_shelter", collection_name="outcomes"):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            # Test connection
            self.client.server_info()
            logger.info(f"Connected to MongoDB: {self.database_name}.{self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def read(self, query=None, limit=None):
        """
        Query data from MongoDB
        :param query: MongoDB query dictionary
        :param limit: Maximum number of documents to return
        :return: List of documents
        """
        try:
            if query is None:
                query = {}
            
            cursor = self.collection.find(query)
            
            if limit:
                cursor = cursor.limit(limit)
            
            # Convert MongoDB cursor to list of dictionaries
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            logger.info(f"Retrieved {len(results)} documents from MongoDB")
            return results
            
        except Exception as e:
            logger.error(f"Error querying MongoDB: {e}")
            return []
    
    def get_stats(self):
        """Get collection statistics"""
        try:
            count = self.collection.count_documents({})
            return {"total_documents": count}
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_documents": 0}
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Initialize Flask app
app = Flask(__name__)

# Initialize data manager
try:
    data_manager = MongoDataManager()
    stats = data_manager.get_stats()
    logger.info(f"MongoDB initialized with {stats['total_documents']} documents")
except Exception as e:
    logger.error(f"Failed to initialize MongoDB: {e}")
    data_manager = None

# Initialize CRUD manager for create/read/update/delete functionality
crud_manager = MongoCRUD()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get filtered data"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    filter_type = request.args.get('filter_type', 'All')
    
    query = {}
    
    if filter_type == 'Water Rescue':
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Mountain or Wilderness Rescue':
        query = {
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Disaster or Individual Tracking':
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
    
    # Get filtered data
    data = data_manager.read(query)
    
    # Remove MongoDB ObjectId from response
    for record in data:
        if '_id' in record:
            del record['_id']
    
    return jsonify(data)

@app.route('/api/chart')
def get_chart():
    """API endpoint to get pie chart data"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    filter_type = request.args.get('filter_type', 'All')
    
    query = {}
    
    if filter_type == 'Water Rescue':
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Mountain or Wilderness Rescue':
        query = {
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Disaster or Individual Tracking':
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
    
    # Get filtered data
    data = data_manager.read(query)
    
    if not data:
        return jsonify({'error': 'No data available'})
    
    # Convert to DataFrame for plotting
    df = pd.DataFrame(data)
    
    if 'breed' not in df.columns:
        return jsonify({'error': 'No breed data available'})
    
    # Create pie chart
    fig = px.pie(df, names='breed')
    fig.update_layout(
        height=800,
        font=dict(size=18),
        legend=dict(
            title="Dog Breeds",
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=16)
        )
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/api/map')
def get_map_data():
    """API endpoint to get map data for selected animal"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    row_index = request.args.get('row_index', type=int)
    filter_type = request.args.get('filter_type', 'All')
    
    query = {}
    
    if filter_type == 'Water Rescue':
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Mountain or Wilderness Rescue':
        query = {
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Disaster or Individual Tracking':
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
    
    # Get filtered data
    data = data_manager.read(query)
    
    if not data or row_index is None or row_index >= len(data):
        return jsonify({'error': 'No animal selected or invalid index'})
    
    # Get selected row data
    selected_row = data[row_index]
    
    # Check if location data is available
    if 'location_lat' in selected_row and 'location_long' in selected_row:
        lat = selected_row['location_lat']
        lon = selected_row['location_long']
        breed = selected_row.get('breed', 'Unknown')
        name = selected_row.get('name', 'Unknown')
        
        if lat is not None and lon is not None:
            return jsonify({
                'lat': float(lat),
                'lon': float(lon),
                'breed': breed,
                'name': name
            })
    
    return jsonify({'error': 'Location data not available for selected animal'})

@app.route('/api/stats')
def get_stats():
    """API endpoint to get database statistics"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    stats = data_manager.get_stats()
    return jsonify(stats)

@app.route('/api/animal', methods=['POST'])
def create_animal():
    data = request.json
    inserted_id = crud_manager.create(data)
    if inserted_id:
        return jsonify({"success": True, "id": inserted_id}), 201
    return jsonify({"error": "Insertion failed"}), 500

@app.route('/api/animal/<string:doc_id>', methods=['GET'])
def get_animal(doc_id):
    result = crud_manager.read_one(doc_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Document not found"}), 404

@app.route('/api/animal/<string:doc_id>', methods=['PUT'])
def update_animal(doc_id):
    updated_data = request.json
    success = crud_manager.update(doc_id, updated_data)
    if success:
        return jsonify({"success": True})
    return jsonify({"error": "Update failed"}), 500

@app.route('/api/animal/<string:doc_id>', methods=['DELETE'])
def delete_animal(doc_id):
    success = crud_manager.delete(doc_id)
    if success:
        return jsonify({"success": True})
    return jsonify({"error": "Deletion failed"}), 500

@app.route('/api/search')
def search_animals():
    """API endpoint for real-time search"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    query_text = request.args.get('q', '').strip()
    
    if not query_text:
        return jsonify([])
    
    # Check cache first
    cache_key = f"search:{query_text.lower()}"
    cached_result = search_cache.get(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit for query: {query_text}")
        return jsonify(cached_result)
    
    # MongoDB text search query
    search_query = {
        "$text": {
            "$search": query_text,
            "$caseSensitive": False
        }
    }
    
    try:
        # Perform text search with relevance scoring
        results = list(data_manager.collection.find(
            search_query,
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(100))
        
        # Convert ObjectId to string and remove score field
        clean_results = []
        for doc in results:
            doc['_id'] = str(doc['_id'])
            doc.pop('score', None)  # Remove score field
            clean_results.append(doc)
        
        # Cache the results
        search_cache.put(cache_key, clean_results)
        
        logger.info(f"Search performed for '{query_text}': {len(clean_results)} results")
        return jsonify(clean_results)
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": "Search failed"}), 500

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Ensure cleanup on exit
        if data_manager:
            data_manager.close()