# Reform Guide - Customize GECA Chatbot with Your Own Data

This guide will help you replace the developer's database and data with your own, and extend the RAG agent to handle additional data sources.

---

## Table of Contents
1. [Overview](#overview)
2. [Setting Up Your Own MongoDB Database](#setting-up-your-own-mongodb-database)
3. [Understanding the Current Data Structure](#understanding-the-current-data-structure)
4. [Preparing Your Own Data](#preparing-your-own-data)
5. [Replacing Data Loaders](#replacing-data-loaders)
6. [Adding New Data Sources](#adding-new-data-sources)
7. [Modifying the RAG Pipeline](#modifying-the-rag-pipeline)
8. [Updating the Chatbot Prompts](#updating-the-chatbot-prompts)
9. [Complete Example: Adding a New Department](#complete-example-adding-a-new-department)
10. [Testing Your Changes](#testing-your-changes)

---

## Overview

The GECA Chatbot uses:
- **MongoDB Atlas** as the vector database
- **Three collections**: `Syllabus`, `Faculty`, `Time-Table`
- **LangChain** for RAG pipeline orchestration
- **HuggingFace embeddings** for vector representations

To customize it with your own data, you'll need to:
1. Set up your own MongoDB Atlas database
2. Prepare your data in compatible formats
3. Modify or create data loaders
4. Update the RAG pipeline configuration
5. Adjust the chatbot's prompts and scope

---

## Setting Up Your Own MongoDB Database

### Step 1: Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create a free account and cluster
3. Configure database access:
   - Go to "Database Access" → "Add New Database User"
   - Create username/password (save these!)
   - Set privileges to "Read and Write to any database"

### Step 2: Configure Network Access
1. Go to "Network Access" → "Add IP Address"
2. For development: Add `0.0.0.0/0` (allows access from anywhere)
3. For production: Add only your server's IP address

### Step 3: Get Connection String
1. Go to "Databases" → "Connect"
2. Choose "Drivers" → "Python"
3. Copy the connection string
4. Replace `<password>` with your database user's password

### Step 4: Update Environment Variables
Update your `.env` file:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
```

### Step 5: Create Your Database
The application uses database name `Second-Year-CSE`. You can:
- Keep the same name (update data loaders)
- Change to your own name (update `rag.py` and all loaders)

To change the database name, edit these files:
- `rag.py` (line 16): `dbName = "Your-Database-Name"`
- `load_data.py` (line 13): `dbName = "Your-Database-Name"`
- `load_data_csv.py` (line 13): `dbName = "Your-Database-Name"`
- `load_data_pdf.py` (line 54): `dbName = "Your-Database-Name"`

---

## Understanding the Current Data Structure

### Current Collections

| Collection | Data Type | Source File | Description |
|------------|-----------|------------|-------------|
| `Syllabus` | PDF | `NEP_SYCSE.pdf` | Academic syllabus information |
| `Faculty` | PDF | `Faculty.pdf` | Faculty details and information |
| `Time-Table` | CSV | `timetable.csv` | Class schedules and timetables |

### Document Structure in MongoDB

Each document in MongoDB has:
```json
{
  "page_content": "The actual text content",
  "embedding": [0.123, 0.456, ...],  // 384-dimensional vector
  "metadata": {
    // Collection-specific metadata
  }
}
```

### Metadata Examples

**Syllabus collection:**
```json
{
  "Branch": "CSE",
  "Year": "Second",
  "Semester": "Third",
  "Subject": "Multidisciplinary Minor"
}
```

**Time-Table collection:**
```json
{
  "day": "Monday",
  "time_slot": "9:00-10:00"
}
```

**Faculty collection:**
```json
{
  // Typically includes page number and source info
}
```

---

## Preparing Your Own Data

### Supported Data Formats

| Format | Loader | Use Case |
|--------|--------|----------|
| PDF | `PyPDFLoader` | Documents, syllabi, manuals |
| CSV | `pandas.read_csv()` | Structured data (timetables, lists) |
| TXT/MD | Custom loader | Plain text documents |
| JSON | Custom loader | Structured data with metadata |
| HTML | `UnstructuredHTMLLoader` | Web-scraped content |

### Data Preparation Checklist

1. **Gather your files** in a `Data/` directory
2. **Clean your data** (remove irrelevant content)
3. **Decide on collections** (group similar data together)
4. **Plan metadata** (what searchable fields do you need?)
5. **Ensure text is readable** (no scanned images without OCR)

### Example: Preparing a New PDF

```bash
Data/
├── syllabus.pdf          # Your institution's syllabus
├── faculty_handbook.pdf  # Faculty information
├── calendar.csv          # Academic calendar
├── courses.json          # Course catalog
└── policies/
    ├── attendance.pdf
    └── grading.pdf
```

---

## Replacing Data Loaders

### Option 1: Modify Existing Loaders

#### Replace Syllabus Data (`load_data.py`)

```python
# load_data.py - Modified for your syllabus
import pandas as pd
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Your-Database-Name"  # Change this
collectionName = "Syllabus"    # Or your collection name
collection = client[dbName][collectionName]
PDF_FILE_PATH = "./Data/your_syllabus.pdf"  # Change this

# Load and split PDF
loader = PyPDFLoader(PDF_FILE_PATH)
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
documents = text_splitter.split_documents(pages)

# Add metadata to each chunk
for doc in documents:
    doc.metadata.update({
        "Branch": "Your Branch",
        "Year": "Your Year",
        "Type": "Syllabus"
    })

print(f"✅ Loaded {len(documents)} document chunks")

# Create embeddings
embeddings = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model="sentence-transformers/all-MiniLM-L6-v2",
)

# Upload to MongoDB
try:
    vectorStore = MongoDBAtlasVectorSearch.from_documents(
        documents=documents,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index",
    )
    print("✅ Successfully inserted documents into MongoDB Atlas.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()
```

#### Replace Timetable Data (`load_data_csv.py`)

```python
# load_data_csv.py - Modified for your CSV
import pandas as pd
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.documents import Document
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Your-Database-Name"
collectionName = "Time-Table"
collection = client[dbName][collectionName]
CSV_FILE_PATH = "./Data/your_timetable.csv"

# Read CSV
df = pd.read_csv(CSV_FILE_PATH)

# Convert to documents based on your CSV structure
documents = []
for index, row in df.iterrows():
    # Adjust this based on your CSV columns
    text_content = f"On {row['Day']} at {row['Time']}: {row['Subject']} in {row['Room']}"
    
    metadata = {
        "day": row['Day'],
        "time": row['Time'],
        "subject": row['Subject'],
        "room": row['Room']
    }
    
    doc = Document(page_content=text_content, metadata=metadata)
    documents.append(doc)

print(f"✅ Converted {len(documents)} rows into documents")

# Create embeddings and upload
embeddings = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model="sentence-transformers/all-MiniLM-L6-v2",
)

try:
    vectorStore = MongoDBAtlasVectorSearch.from_documents(
        documents=documents,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index",
    )
    print("✅ Successfully inserted documents into MongoDB Atlas.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()
```

---

## Adding New Data Sources

### Example 1: Adding JSON Data Loader

Create `load_data_json.py`:

```python
import json
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.documents import Document
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Your-Database-Name"
collectionName = "Courses"  # New collection
collection = client[dbName][collectionName]
JSON_FILE_PATH = "./Data/courses.json"

# Load JSON data
with open(JSON_FILE_PATH, 'r') as f:
    data = json.load(f)

documents = []
for item in data:
    # Adjust based on your JSON structure
    text_content = f"Course: {item['code']} - {item['name']}\nDescription: {item['description']}"
    
    metadata = {
        "code": item['code'],
        "name": item['name'],
        "credits": item.get('credits', 0),
        "type": "Course"
    }
    
    doc = Document(page_content=text_content, metadata=metadata)
    documents.append(doc)

print(f"✅ Loaded {len(documents)} course documents")

# Create embeddings
embeddings = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model="sentence-transformers/all-MiniLM-L6-v2",
)

# Upload to MongoDB
try:
    vectorStore = MongoDBAtlasVectorSearch.from_documents(
        documents=documents,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index",
    )
    print("✅ Successfully inserted course data into MongoDB Atlas.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()
```

### Example 2: Adding Multiple PDFs from a Directory

Create `load_data_multi_pdf.py`:

```python
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pymongo import MongoClient

import os as os_module
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Your-Database-Name"
collectionName = "Policies"  # New collection
collection = client[dbName][collectionName]
PDF_DIR = "./Data/policies"  # Directory with multiple PDFs

# Load all PDFs from directory
all_documents = []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

for filename in os_module.listdir(PDF_DIR):
    if filename.endswith('.pdf'):
        filepath = os_module.path.join(PDF_DIR, filename)
        print(f"Loading {filename}...")
        
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        chunks = text_splitter.split_documents(pages)
        
        # Add metadata
        for doc in chunks:
            doc.metadata.update({
                "source_file": filename,
                "type": "Policy"
            })
        
        all_documents.extend(chunks)

print(f"✅ Loaded {len(all_documents)} document chunks from {len(os_module.listdir(PDF_DIR))} PDFs")

# Create embeddings
embeddings = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model="sentence-transformers/all-MiniLM-L6-v2",
)

# Upload to MongoDB
try:
    vectorStore = MongoDBAtlasVectorSearch.from_documents(
        documents=all_documents,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index",
    )
    print("✅ Successfully inserted policy documents into MongoDB Atlas.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()
```

---

## Modifying the RAG Pipeline

### Update `rag.py` to Include New Collections

```python
# rag.py - Modified to include new collections

from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from pymongo import MongoClient

from dotenv import load_dotenv
import os

load_dotenv()

dbName = "Your-Database-Name"  # Change this
index = "vector_index"

# Test embeddings
print("--- Testing embeddings ---")
try:
    embeddings = HuggingFaceEndpointEmbeddings(
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        model="sentence-transformers/all-MiniLM-L6-v2",
    )
    test_embed = embeddings.embed_query("test")
    print(f"Embedding dimension: {len(test_embed)}")
except Exception as e:
    print(f"Embedding error: {e}")
    embeddings = None

# Test MongoDB connection
print("\n--- Testing MongoDB connection ---")
try:
    mongo_client = MongoClient(os.environ["MONGODB_URI"])
    db = mongo_client[dbName]
    collections = db.list_collection_names()
    print(f"Available collections: {collections}")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    embeddings = None

# Create retrievers for ALL collections (including new ones)
if embeddings:
    # Original collections
    retriever_syllabus = MongoDBAtlasVectorSearch.from_connection_string(
        os.environ["MONGODB_URI"],
        dbName + "." + "Syllabus",
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 6})

    retriever_faculty = MongoDBAtlasVectorSearch.from_connection_string(
        os.environ["MONGODB_URI"],
        dbName + "." + "Faculty",
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 75})

    retriever_timetable = MongoDBAtlasVectorSearch.from_connection_string(
        os.environ["MONGODB_URI"],
        dbName + "." + "Time-Table",
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 24})
    
    # NEW: Add your new collection retriever
    retriever_courses = MongoDBAtlasVectorSearch.from_connection_string(
        os.environ["MONGODB_URI"],
        dbName + "." + "Courses",  # Your new collection
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 10})  # Adjust k as needed
    
    # NEW: Add policies retriever
    retriever_policies = MongoDBAtlasVectorSearch.from_connection_string(
        os.environ["MONGODB_URI"],
        dbName + "." + "Policies",  # Your new collection
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 5})
    
else:
    retriever_syllabus = retriever_faculty = retriever_timetable = None
    retriever_courses = retriever_policies = None  # New ones too

# Merge function
def merge_documents(retrieved_dict):
    """Combines lists of documents from all keys in the dictionary."""
    merged_list = []
    for doc_list in retrieved_dict.values():
        merged_list.extend(doc_list)
    return merged_list

# Update combined retriever to include new sources
combined_retriever = (
    RunnableParallel(
        syllabus=retriever_syllabus,
        faculty=retriever_faculty,
        timetable=retriever_timetable,
        courses=retriever_courses,  # NEW
        policies=retriever_policies,  # NEW
    )
    | merge_documents
)

# ... rest of the file remains the same
```

---

## Updating the Chatbot Prompts

### Modify `index.py` to Reflect New Data

```python
# index.py - Updated for new data scope

import logging
import os
import re
import sys

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import rag

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.info("--- RAG APP STARTUP: module loading started ---")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    model="gemini-2.5-flash-lite",
)
response_parser = StrOutputParser()

# UPDATED PROMPT to include new data types
prompt = PromptTemplate.from_template(
    """
You are a helpful assistant specializing in academic support and campus information.
Keep your answers concise, helpful, and focused on the information provided.

Use the following pieces of context from the syllabus, faculty, timetable, courses, and policies to answer the question.
Treat these as in-scope topics: syllabus, subjects, faculty, timetable, class schedule, exams, labs, 
attendance, departments, student life, courses, academic policies, and general campus information.

If the context does not contain the answer, and the question is clearly unrelated to academics/campus/student life,
kindly state, "I am trained to answer questions only about academic and campus-related topics."

Context:
{context}

Question: {question}
"""
)

logging.info("--- RAG APP STARTUP: using rag.py pipeline ---")

def generate_response(user_message):
    # Use the vector-only pipeline from rag.py
    response = rag.query_data(user_message)
    
    fallback_text = "I am trained to answer questions only about academic and campus-related topics."
    in_scope_pattern = (
        r"\b(syllabus|subject|faculty|teacher|professor|timetable|time table|schedule|"
        r"class|course|credit|policy|exam|attendance|department|lab|semester|student|campus|"
        r"grading|calendar|holiday)\b"
    )
    
    if fallback_text.lower() in response.lower() and re.search(in_scope_pattern, user_message.lower()):
        return (
            "I can help with that. Please share a little more detail (for example semester, "
            "branch/division, day, faculty name, or course code) so I can find the exact information."
        )
    
    return response
```

---

## Complete Example: Adding a New Department

Let's say you want to add Engineering Mathematics as a new subject area:

### Step 1: Prepare Data
```bash
mkdir Data/Math
# Add your math syllabus PDFs to this folder
```

### Step 2: Create Data Loader
Create `load_data_math.py`:

```python
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Your-Database-Name"
collectionName = "Mathematics"
collection = client[dbName][collectionName]

# Load all math PDFs
import glob
pdf_files = glob.glob("./Data/Math/*.pdf")
all_docs = []

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)

for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    pages = loader.load()
    chunks = text_splitter.split_documents(pages)
    
    for doc in chunks:
        doc.metadata.update({
            "subject": "Mathematics",
            "topic": "Engineering Math",
            "source_file": pdf_file.split("\\")[-1]
        })
    
    all_docs.extend(chunks)
    print(f"Loaded {len(chunks)} chunks from {pdf_file}")

print(f"Total documents: {len(all_docs)}")

# Create embeddings
embeddings = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model="sentence-transformers/all-MiniLM-L6-v2",
)

# Upload
vectorStore = MongoDBAtlasVectorSearch.from_documents(
    documents=all_docs,
    embedding=embeddings,
    collection=collection,
    index_name="vector_index",
)
print("✅ Mathematics data uploaded successfully!")
```

### Step 3: Update RAG Pipeline
Add to `rag.py`:
```python
retriever_math = MongoDBAtlasVectorSearch.from_connection_string(
    os.environ["MONGODB_URI"],
    dbName + "." + "Mathematics",
    embeddings,
    index_name=index,
).as_retriever(search_kwargs={"k": 8})
```

Update `combined_retriever`:
```python
combined_retriever = (
    RunnableParallel(
        syllabus=retriever_syllabus,
        faculty=retriever_faculty,
        timetable=retriever_timetable,
        math=retriever_math,  # NEW
    )
    | merge_documents
)
```

### Step 4: Create Vector Index
Run `create_vector_index.py` (it will create indexes for all collections).

---

## Testing Your Changes

### Test 1: Verify Data Upload
```bash
python -c "
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.environ['MONGODB_URI'])
db = client['Your-Database-Name']

# Check collections
print('Collections:', db.list_collection_names())

# Check document counts
for coll in db.list_collection_names():
    count = db[coll].count_documents({})
    print(f'{coll}: {count} documents')
"
```

### Test 2: Test Retrieval
```bash
python -c "
import rag
print('Testing retrieval...')
docs = rag.retriever_syllabus.invoke('What is the syllabus?')
print(f'Retrieved {len(docs)} documents')
"
```

### Test 3: Test Full Pipeline
```bash
python serve.py
# Then in another terminal:
curl -X POST http://localhost:5000/generate_response \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What courses are available?\"}"
```

---

## Quick Reference: File Modification Checklist

- [ ] Update `.env` with your MongoDB URI
- [ ] Modify `rag.py`:
  - [ ] Change `dbName`
  - [ ] Add new retrievers for new collections
  - [ ] Update `combined_retriever`
- [ ] Modify `index.py`:
  - [ ] Update prompt template
  - [ ] Update `in_scope_pattern`
- [ ] Update/create data loaders:
  - [ ] `load_data.py`
  - [ ] `load_data_csv.py`
  - [ ] `load_data_pdf.py`
  - [ ] Create new loaders for new data
- [ ] Run `create_vector_index.py` to create indexes
- [ ] Test the application

---

## Common Issues & Solutions

### Issue 1: "Collection not found"
**Solution:** Ensure you've run the data loader for that collection.

### Issue 2: "Vector index not found"
**Solution:** Run `python create_vector_index.py` after loading data.

### Issue 3: Poor retrieval results
**Solutions:**
- Adjust `k` value in retriever (increase for more context)
- Modify chunk_size in text splitter
- Add more specific metadata
- Improve your prompt template

### Issue 4: Slow responses
**Solutions:**
- Reduce `k` values
- Use smaller chunk sizes
- Consider using a faster embedding model

---

## Advanced: Using Different Embedding Models

To use a different embedding model, update all files:

```python
# Example: Using OpenAI embeddings instead
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small"
)
```

Update `.env`:
```env
OPENAI_API_KEY=your_openai_key_here
```

---

## Support

For issues with customization:
1. Check MongoDB Atlas logs
2. Verify all environment variables are set
3. Test each component individually
4. Check the server logs for detailed error messages

---

**Happy Customizing! 🚀**
