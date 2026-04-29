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

dbName = "Second-Year-CSE"
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
    global mongo_client
    mongo_client = MongoClient(os.environ["MONGODB_URI"])
    db = mongo_client[dbName]
    collections = db.list_collection_names()
    print(f"Available collections: {collections}")
    
    # Check if our collections exist and have vector embeddings
    for coll_name in ["Syllabus", "Faculty", "Time-Table"]:
        if coll_name in collections:
            count = db[coll_name].count_documents({})
            print(f"  {coll_name}: {count} documents")
            
            # List indexes on the collection
            indexes = db[coll_name].list_indexes()
            print(f"    Indexes: {list(indexes)}")
            
            # Check if documents have vector embeddings
            sample = db[coll_name].find_one({})
            if sample:
                has_vector = "$vector" in sample or "embedding" in sample or "vector" in sample
                print(f"    Sample keys: {list(sample.keys())}")
                print(f"    Has vector field: {has_vector}")
        else:
            print(f"  {coll_name}: NOT FOUND")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    import traceback
    traceback.print_exc()
    embeddings = None

# Only create retrievers if embeddings worked
if embeddings:
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
else:
    retriever_syllabus = retriever_faculty = retriever_timetable = None


def merge_documents(retrieved_dict):
    """Combines lists of documents from all keys in the dictionary."""
    merged_list = []
    # retrieved_dict will look like: {'syllabus': [doc1, doc2], 'faculty': [doc3]}
    for doc_list in retrieved_dict.values():
        merged_list.extend(doc_list)
    return merged_list

combined_retriever = (
    RunnableParallel(
        syllabus=retriever_syllabus,
        faculty=retriever_faculty,
        timetable=retriever_timetable,
    )
    | merge_documents
)

def query_data(query):

    # Check if retrievers were initialized
    if not retriever_syllabus or not retriever_faculty or not retriever_timetable:
        print("ERROR: Retrievers not initialized properly")
        return "Sorry, the RAG system failed to initialize. Please check the server logs."

    # Retrieve context and print for debugging
    print(f"\nQuery: {query}")
    
    # Test each retriever individually
    print("\n--- Testing individual retrievers ---")
    try:
        syllabus_docs = retriever_syllabus.invoke(query)
        print(f"Syllabus docs: {len(syllabus_docs)}")
    except Exception as e:
        print(f"Syllabus retriever error: {e}")
        syllabus_docs = []
    
    try:
        faculty_docs = retriever_faculty.invoke(query)
        print(f"Faculty docs: {len(faculty_docs)}")
    except Exception as e:
        print(f"Faculty retriever error: {e}")
        faculty_docs = []
    
    try:
        timetable_docs = retriever_timetable.invoke(query)
        print(f"Timetable docs: {len(timetable_docs)}")
    except Exception as e:
        print(f"Timetable retriever error: {e}")
        timetable_docs = []
    
    # Merge all docs
    retrieved_docs = syllabus_docs + faculty_docs + timetable_docs
    print(f"Total docs retrieved: {len(retrieved_docs)}")
    print("--- End testing ---\n")
    
    context_text = "\n\n".join([d.page_content for d in retrieved_docs])
    print("\n" + "="*50)
    print("CONTEXT BEING GIVEN TO LLM:")
    print("="*50)
    print(context_text if context_text else "[NO CONTEXT RETRIEVED]")
    print("="*50 + "\n")

    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Do not answer the question if there is no given context.
    Feel free to answer the query if it is related to students, teacher, faculty or general well-being as well.
    Context:
    {context}
    Question: {question}
    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    retrieve_context = {
        "context": lambda docs: "\n\n".join([d.page_content for d in docs]),
        "question": RunnablePassthrough()
        } 
    
    # Use Groq LLM
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return "Sorry, Groq API key is not configured."
    
    llm = ChatGroq(
        groq_api_key=groq_key,
        temperature=0,
        model_name="llama-3.1-8b-instant"
    )
    print("Using Groq LLM")

    response_parser = StrOutputParser()

    # Create a simple chain that uses the pre-retrieved context
    rag_chain = (
        {"context": lambda x: context_text, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | response_parser
    )

    answer = rag_chain.invoke(query)
    return answer