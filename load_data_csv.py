import pandas as pd
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Second-Year-CSE"
collectionName = "Time-Table"
collection = client[dbName][collectionName]
CSV_FILE_PATH = "./Data/timetable.csv"

df = pd.read_csv(CSV_FILE_PATH)

id_vars = ['Day']
value_vars = df.columns.tolist()[1:]
# Use the melt function to turn column headers (time slots) into a new column
# Each row now represents ONE single class slot.
df_long = pd.melt(
    df, 
    id_vars=id_vars, 
    value_vars=value_vars, 
    var_name='Time_Slot', 
    value_name='Course_Name'
)

documents = []
for index, record in df_long.iterrows():
    
    text_content = (
        f"The class on {record['Day']} at {record['Time_Slot']} is: "
        f"{record['Course_Name']}"
    )
    
    metadata = {
        "day": record['Day'],
        "time_slot": record['Time_Slot'],
    }

    doc = Document(page_content=text_content, metadata=metadata)
    documents.append(doc)

    print(f"✅ Converted {len(documents)} class slots into LangChain Documents.")

# --- 3. Instantiate Embeddings Model ---

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

try:
    vectorStore = MongoDBAtlasVectorSearch.from_documents(
        documents=documents, 
        embedding=embeddings, 
        collection=collection,
        index_name="vector_index",
    )
    print("✅ Successfully inserted documents and created embeddings in MongoDB Atlas.")
    
except Exception as e:
    print(f"An error occurred during vector store creation: {e}")
    # You might need to check your Atlas connection URI or if the index exists.

finally:
    client.close()