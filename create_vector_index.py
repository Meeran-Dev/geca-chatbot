"""
Script to create vector search indexes on MongoDB collections
"""
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Second-Year-CSE"
db = client[dbName]

index_name = "vector_index"

# Define index configurations for each collection
for collection_name in ["Syllabus", "Faculty", "Time-Table"]:
    collection = db[collection_name]
    
    print(f"\n--- Creating index on {collection_name} ---")
    
    # Check if index already exists
    existing_indexes = list(collection.list_search_indexes())
    print(f"Existing indexes: {existing_indexes}")
    
    # Create the search index model
    search_index_model = SearchIndexModel(
        name=index_name,
        definition={
            "mappings": {
                "dynamic": False,
                "fields": {
                    "embedding": {
                        "dimensions": 384,
                        "metric": "cosine",
                        "type": "knnVector"
                    }
                }
            }
        }
    )
    
    # Create the index
    try:
        result = collection.create_search_index(search_index_model)
        print(f"Index creation result: {result}")
        print(f"✅ Index created successfully for {collection_name}")
    except Exception as e:
        print(f"Error creating index for {collection_name}: {e}")

print("\n--- Index creation complete ---")
client.close()