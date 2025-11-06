import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(MONGO_URI)

db = client["Second-Year-CSE"]
mycollection = db["Syllabus"]

filter_query = {}

delete_result = mycollection.delete_many(filter_query)

print(f"✅ Delete operation successful.")
print(f"Total documents deleted: {delete_result.deleted_count}")

client.close()