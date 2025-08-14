from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

class CRUD:
    """CRUD operations for any MongoDB collection."""

    def __init__(self, user, password, host, port, db_name, collection_name):
        """
        Initialize the CRUD class by establishing a connection to MongoDB.
        
        :param user: Username for MongoDB authentication
        :param password: Password for MongoDB authentication
        :param host: Host address of the MongoDB server
        :param port: Port on which the MongoDB server is running
        :param db_name: The name of the database to connect to
        :param collection_name: The name of the collection to operate on
        """
        try:
            # MongoDB connection string using the provided credentials
            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]
            print(f"Connected to MongoDB database: {db_name}, collection: {collection_name}")
        except ConnectionFailure as e:
            raise Exception(f"Could not connect to MongoDB: {e}")

    def create(self, data):
        """
        Insert a document into the collection.
        
        :param data: Dictionary containing the key-value pairs to insert into the collection
        :return: True if insert was successful, False otherwise
        """
        if data is not None and isinstance(data, dict):
            try:
                result = self.collection.insert_one(data)
                return True if result.acknowledged else False
            except OperationFailure as e:
                print(f"Insert operation failed: {e}")
                return False
        else:
            raise ValueError("Invalid data format: data should be a non-empty dictionary")

    def read(self, query):
        """
        Query documents from the collection.
        
        :param query: Dictionary containing the key-value pairs to search for
        :return: List of matching documents, or an empty list if none found or query fails
        """
        if query is not None and isinstance(query, dict):
            try:
                cursor = self.collection.find(query)
                result = list(cursor)  # Convert cursor to a list
                return result
            except OperationFailure as e:
                print(f"Query operation failed: {e}")
                return []
        else:
            raise ValueError("Invalid query format: query should be a non-empty dictionary")

    def update(self, query, new_values):
        """
        Update an existing document in the collection.
        
        :param query: Dictionary used to find the document to update
        :param new_values: Dictionary containing the updated fields and values
        :return: True if update was successful, False otherwise
        """
        if query is not None and isinstance(query, dict) and new_values is not None and isinstance(new_values, dict):
            try:
                result = self.collection.update_one(query, {"$set": new_values})
                return True if result.modified_count > 0 else False
            except OperationFailure as e:
                print(f"Update operation failed: {e}")
                return False
        else:
            raise ValueError("Invalid input format: both query and new_values should be non-empty dictionaries")

    def delete(self, query):
        """
        Delete a document from the collection.
        
        :param query: Dictionary used to find the document to delete
        :return: True if deletion was successful, False otherwise
        """
        if query is not None and isinstance(query, dict):
            try:
                result = self.collection.delete_one(query)
                return True if result.deleted_count > 0 else False
            except OperationFailure as e:
                print(f"Delete operation failed: {e}")
                return False
        else:
            raise ValueError("Invalid query format: query should be a non-empty dictionary")
