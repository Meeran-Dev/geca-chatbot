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
collectionName = "Syllabus"
collection = client[dbName][collectionName]
PDF_FILE_PATH = "./Data/NEP_SYCSE.pdf"

text_content = ("""
    Choices for Multidisciplinary Minor:
        Management and Finance
        Digital and Multimedia Forensics
        Internet of Things
        Social Science
    """)

metadata = {
    "Branch" : "CSE",
    "Year" : "Second", 
    "Semester" : "Third",
    "Subject" : "Multidisciplinary Minor"
}
documents = []
doc = Document(page_content=text_content, metadata=metadata)
documents.append(doc)

print(f"✅ Converted into LangChain Documents.")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

try:
    vectorStore = MongoDBAtlasVectorSearch.from_documents(
        documents = documents, 
        embedding = embeddings, 
        collection = collection,
        index_name = "vector_index",
    )
    print("✅ Successfully inserted document and created embeddings in MongoDB Atlas.")
    
except Exception as e:
    print(f"An error occurred during vector store creation: {e}")

finally:
    client.close()
