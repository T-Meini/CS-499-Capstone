from pymongo import MongoClient
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

class MongoCRUD:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="animal_shelter", collection_name="outcomes"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        # Create compound text index for efficient search
        try:
            self.collection.create_index([
                ("name", "text"),
                ("breed", "text"),
                ("outcome_type", "text")
            ])
            logger.info("Compound text index created (or already exists).")
        except Exception as e:
            logger.error(f"Index Creation Error: {e}")

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
