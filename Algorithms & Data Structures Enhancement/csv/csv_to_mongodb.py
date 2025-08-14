#!/usr/bin/env python3
"""
Script to import CSV data into MongoDB
Run this script once to migrate your data from CSV to MongoDB
"""

import pandas as pd
import pymongo
from pymongo import MongoClient
import numpy as np
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_data(df):
    """Clean and prepare data for MongoDB insertion"""
    # Replace NaN values with None (MongoDB null)
    df = df.replace({np.nan: None})
    
    # Convert numpy types to Python native types
    for col in df.columns:
        if df[col].dtype == 'int64':
            df[col] = df[col].astype('Int64')  # Nullable integer
        elif df[col].dtype == 'float64':
            df[col] = df[col].astype('Float64')  # Nullable float
    
    return df

def import_csv_to_mongodb(csv_file_path, mongo_uri="mongodb://localhost:27017/", 
                         database_name="animal_shelter", collection_name="outcomes"):
    """
    Import CSV data into MongoDB
    
    Args:
        csv_file_path (str): Path to the CSV file
        mongo_uri (str): MongoDB connection URI
        database_name (str): Name of the database
        collection_name (str): Name of the collection
    """
    try:
        # Read CSV file
        logger.info(f"Reading CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        logger.info(f"Successfully loaded {len(df)} records from CSV")
        
        # Clean data
        df = clean_data(df)
        
        # Connect to MongoDB
        logger.info(f"Connecting to MongoDB at {mongo_uri}")
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        
        # Clear existing data (optional - remove if you want to append)
        logger.info("Clearing existing data...")
        collection.delete_many({})
        
        # Convert DataFrame to dictionary records
        records = df.to_dict('records')
        
        # Insert data in batches (more efficient for large datasets)
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            result = collection.insert_many(batch)
            total_inserted += len(result.inserted_ids)
            logger.info(f"Inserted batch {i//batch_size + 1}: {len(result.inserted_ids)} records")
        
        logger.info(f"Successfully imported {total_inserted} records to MongoDB")
        
        # Create indexes for better query performance
        logger.info("Creating indexes...")
        collection.create_index("breed")
        collection.create_index("sex_upon_outcome")
        collection.create_index("age_upon_outcome_in_weeks")
        collection.create_index([("location_lat", 1), ("location_long", 1)])
        
        # Verify the import
        count = collection.count_documents({})
        logger.info(f"Verification: {count} documents in collection")
        
        # Show sample document
        sample = collection.find_one()
        if sample:
            logger.info("Sample document:")
            for key, value in sample.items():
                if key != '_id':  # Skip MongoDB ObjectId
                    logger.info(f"  {key}: {value}")
        
        client.close()
        logger.info("Import completed successfully!")
        
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_file_path}")
    except pymongo.errors.ConnectionFailure:
        logger.error("Failed to connect to MongoDB. Make sure MongoDB is running.")
    except Exception as e:
        logger.error(f"Error during import: {str(e)}")

def test_connection(mongo_uri="mongodb://localhost:27017/"):
    """Test MongoDB connection"""
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection
        logger.info("MongoDB connection successful!")
        client.close()
        return True
    except pymongo.errors.ServerSelectionTimeoutError:
        logger.error("MongoDB connection failed. Make sure MongoDB is running.")
        return False

if __name__ == "__main__":
    # Configuration
    CSV_FILE_PATH = "aac_shelter_outcomes.csv"  # Update this path
    MONGO_URI = "mongodb://localhost:27017/"     # Update if needed
    DATABASE_NAME = "animal_shelter"
    COLLECTION_NAME = "outcomes"
    
    # Test connection first
    if test_connection(MONGO_URI):
        # Import CSV to MongoDB
        import_csv_to_mongodb(
            csv_file_path=CSV_FILE_PATH,
            mongo_uri=MONGO_URI,
            database_name=DATABASE_NAME,
            collection_name=COLLECTION_NAME
        )
    else:
        logger.error("Please install and start MongoDB before running this script.")
        logger.info("Installation instructions:")
        logger.info("- Ubuntu/Debian: sudo apt-get install mongodb")
        logger.info("- macOS: brew install mongodb/brew/mongodb-community")
        logger.info("- Windows: Download from https://www.mongodb.com/try/download/community")