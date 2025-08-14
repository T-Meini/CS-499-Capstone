import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MongoCRUD:
    def __init__(self, uri=None, db_name=None, collection_name=None):
        # Pull from .env
        username = os.getenv('MONGO_USERNAME')
        password = os.getenv('MONGO_PASSWORD')
        cluster = os.getenv('MONGO_CLUSTER')
        default_db = os.getenv('MONGO_DB', 'animal_shelter')
        default_collection = os.getenv('MONGO_COLLECTION', 'outcomes')

        # Validate credentials
        if not (username and password and cluster):
            raise ValueError("MongoDB credentials (MONGO_USERNAME, MONGO_PASSWORD, MONGO_CLUSTER) must be set in .env.")

        # Build full URI with database and authentication options
        if not uri:
            uri = (
                f"mongodb+srv://{username}:{password}@{cluster}/"
                f"{default_db}?retryWrites=true&w=majority&authSource=admin&appName=AAC-Cluster"
            )

        self.uri = uri
        self.db_name = db_name or default_db
        self.collection_name = collection_name or default_collection

        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]

            # Create compound text index for efficient search
            self.collection.create_index([
                ("name", "text"),
                ("breed", "text"),
                ("outcome_type", "text")
            ])
            logger.info("Compound text index created (or already exists).")

        except Exception as e:
            logger.error(f"Error initializing MongoDB: {e}")
            raise

    def create(self, data):
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Insert Error: {e}")
            return None

    def read_all(self, query=None):
        try:
            documents = self.collection.find(query or {})
            return [{**doc, "_id": str(doc["_id"])} for doc in documents]
        except Exception as e:
            logger.error(f"Read Error: {e}")
            return []

    def read_one(self, doc_id):
        try:
            doc = self.collection.find_one({"_id": ObjectId(doc_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        except Exception as e:
            logger.error(f"Read One Error: {e}")
            return None

    def update(self, doc_id, updated_data):
        try:
            result = self.collection.update_one({"_id": ObjectId(doc_id)}, {"$set": updated_data})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Update Error: {e}")
            return False

    def delete(self, doc_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Delete Error: {e}")
            return False
