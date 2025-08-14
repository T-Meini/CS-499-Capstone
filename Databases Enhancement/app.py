import pandas as pd
from flask import Flask, render_template, jsonify, request, make_response
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
from dotenv import load_dotenv
import csv
import io

load_dotenv()

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

    def __init__(self, mongo_uri=None, database_name=None, collection_name=None):
        # Get credentials and connection info from .env
        username = os.getenv('MONGO_USERNAME')
        password = os.getenv('MONGO_PASSWORD')
        cluster = os.getenv('MONGO_CLUSTER')
        default_db = os.getenv('MONGO_DB', "animal_shelter")
        default_collection = os.getenv('MONGO_COLLECTION', "outcomes")

        # Build full URI only if not passed manually
        if not mongo_uri:
            if not (username and password and cluster):
                raise ValueError("Missing MongoDB credentials or cluster in environment variables.")
            mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/{default_db}?retryWrites=true&w=majority"

        self.mongo_uri = mongo_uri
        self.database_name = database_name or default_db
        self.collection_name = collection_name or default_collection
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
    
    def create_indexes(self):
        """Create performance indexes"""
        try:
            # Create compound index for common queries
            self.collection.create_index([
                ("breed", 1),
                ("sex_upon_outcome", 1),
                ("age_upon_outcome_in_weeks", 1)
            ])
            
            # Create index for outcome type queries
            self.collection.create_index([("outcome_type", 1)])
            
            # Create index for animal type queries
            self.collection.create_index([("animal_type", 1)])
            
            # Create index for date queries
            self.collection.create_index([("date_of_birth", 1)])
            
            logger.info("Performance indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

    def aggregate_by_outcome_type(self, match_query=None):
        """Aggregate data by outcome type"""
        try:
            pipeline = []
            
            if match_query:
                pipeline.append({"$match": match_query})
            
            pipeline.extend([
                {"$group": {
                    "_id": "$outcome_type",
                    "count": {"$sum": 1},
                    "avg_age_weeks": {"$avg": "$age_upon_outcome_in_weeks"}
                }},
                {"$sort": {"count": -1}}
            ])
            
            results = list(self.collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Error in outcome type aggregation: {e}")
            return []

    def aggregate_by_animal_type(self, match_query=None):
        """Aggregate data by animal type"""
        try:
            pipeline = []
            
            if match_query:
                pipeline.append({"$match": match_query})
            
            pipeline.extend([
                {"$group": {
                    "_id": "$animal_type",
                    "count": {"$sum": 1},
                    "breeds": {"$addToSet": "$breed"}
                }},
                {"$sort": {"count": -1}}
            ])
            
            results = list(self.collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Error in animal type aggregation: {e}")
            return []

    def aggregate_by_breed(self, match_query=None):
        """Aggregate data by breed"""
        try:
            pipeline = []
            
            if match_query:
                pipeline.append({"$match": match_query})
            
            pipeline.extend([
                {"$group": {
                    "_id": "$breed",
                    "count": {"$sum": 1},
                    "avg_age_weeks": {"$avg": "$age_upon_outcome_in_weeks"},
                    "outcome_types": {"$addToSet": "$outcome_type"}
                }},
                {"$sort": {"count": -1}},
                {"$limit": 20}  # Top 20 breeds
            ])
            
            results = list(self.collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Error in breed aggregation: {e}")
            return []

    def get_monthly_statistics(self, match_query=None):
        """Get monthly statistics"""
        try:
            pipeline = []

            if match_query:
                pipeline.append({"$match": match_query})

            pipeline.extend([
                {
                    "$addFields": {
                        "parsed_date": {
                            "$toDate": "$datetime"
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "year": {"$year": "$parsed_date"},
                            "month": {"$month": "$parsed_date"}
                        },
                        "count": {"$sum": 1},
                        "outcome_types": {"$addToSet": "$outcome_type"}
                    }
                },
                {
                    "$sort": {"_id.year": 1, "_id.month": 1}
                }
            ])

            results = list(self.collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Error in monthly statistics: {e}")
            return []


# Initialize Flask app
app = Flask(__name__)

# Initialize data manager
try:
    data_manager = MongoDataManager()
    data_manager.create_indexes()  # Create performance indexes
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
    
@app.route('/analytics')
def analytics():
    """Analytics dashboard page"""
    return render_template('analytics.html')

@app.route('/api/aggregation/outcome-type')
def get_outcome_type_aggregation():
    """API endpoint for outcome type aggregation"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    filter_type = request.args.get('filter_type', 'All')
    match_query = get_filter_query(filter_type)
    
    results = data_manager.aggregate_by_outcome_type(match_query)
    return jsonify(results)

@app.route('/api/aggregation/animal-type')
def get_animal_type_aggregation():
    """API endpoint for animal type aggregation"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    filter_type = request.args.get('filter_type', 'All')
    match_query = get_filter_query(filter_type)
    
    results = data_manager.aggregate_by_animal_type(match_query)
    return jsonify(results)

@app.route('/api/aggregation/breed')
def get_breed_aggregation():
    """API endpoint for breed aggregation"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    filter_type = request.args.get('filter_type', 'All')
    match_query = get_filter_query(filter_type)
    
    results = data_manager.aggregate_by_breed(match_query)
    return jsonify(results)

@app.route('/api/aggregation/monthly')
def get_monthly_aggregation():
    """API endpoint for monthly statistics"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500
    
    filter_type = request.args.get('filter_type', 'All')
    match_query = get_filter_query(filter_type)
    
    results = data_manager.get_monthly_statistics(match_query)
    return jsonify(results)

@app.route('/api/export/csv')
def export_csv():
    """Export current data to CSV"""
    if not data_manager:
        return jsonify({"error": "Database connection not available"}), 500

    filter_type = request.args.get('filter_type', 'All')
    search_query = request.args.get('search', '')

    # Get data based on filter or search
    if search_query:
        query = {
            "$text": {
                "$search": search_query,
                "$caseSensitive": False
            }
        }
        data = data_manager.read(query)
    else:
        query = get_filter_query(filter_type)
        data = data_manager.read(query)

    if not data:
        return jsonify({"error": "No data to export"}), 404

    # Create CSV in memory
    output = io.StringIO()

    # Build headers from all documents
    all_headers = set()
    for row in data:
        all_headers.update(row.keys())
    all_headers.discard('_id')  # Optionally exclude MongoDB ID
    headers = list(all_headers)

    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()

    for row in data:
        # Write row, converting values to strings if necessary
        clean_row = {k: str(v) if v is not None else '' for k, v in row.items() if k in headers}
        writer.writerow(clean_row)

    # Create response
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = f"attachment; filename=animal_shelter_data_{filter_type.replace(' ', '_')}.csv"

    return response


def get_filter_query(filter_type):
    """Get MongoDB query for filter type"""
    if filter_type == 'Water Rescue':
        return {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Mountain or Wilderness Rescue':
        return {
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'Disaster or Individual Tracking':
        return {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
    else:
        return {}

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