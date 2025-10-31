from flask import Flask, render_template, request, jsonify
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

dbName = "Second-Year-CSE"
index = "vector_index"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- 1. Define Merge Function ---
def merge_documents(retrieved_dict):
    """Combines lists of documents from all keys in the dictionary."""
    merged_list = []
    for doc_list in retrieved_dict.values():
        merged_list.extend(doc_list)
    return merged_list

# --- 2. Initialize Multiple Retrievers ---
print("Initializing MongoDB Atlas Vector Search and Retrievers...")

try:
    retriever_syllabus = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        dbName + "." + "Syllabus",
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 6})

    retriever_faculty = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        dbName + "." + "Faculty",
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 3})

    retriever_timetable = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        dbName + "." + "Time-Table", 
        embeddings,
        index_name=index,
    ).as_retriever(search_kwargs={"k": 36})
    
    # --- 3. Construct the Combined Retriever Chain ---
    combined_retriever = (
        RunnableParallel(
            syllabus=retriever_syllabus,
            faculty=retriever_faculty,
            timetable=retriever_timetable,
        )
        | merge_documents 
    )
    print("Retrievers initialized successfully.")

except Exception as e:
    print(f"Error during MongoDB/RAG initialization. Check MONGODB_URI and collection names. Error: {e}")
    combined_retriever = None

# --- 4. Define the LLM and RAG Chain ---
if combined_retriever:
    template = """
    You are 'GECA-Bot', a friendly, professional, and knowledgeable College Assistant for Govt. College of Engineering, Aurangabad (GECA) 
    specializing in academic support, campus information, and general student inquiries. 
    Keep your answers concise, helpful, and focused on college life and studies.
    Dont state that you're being given some context, act like you already have this information and you are trained on it.
    Use the following pieces of context from the syllabus, faculty, and timetable to answer the question at the end.
    If the context does not contain the answer, and the question is unrelated to college academics or general well-being, 
    kindly state, "I am trained to answer questions only about GECA, academics, and general student life."
    
    Context:
    {context}
    Question: {question}
    """
    custom_rag_prompt = PromptTemplate.from_template(template)
    
    llm = ChatGoogleGenerativeAI(
        google_api_key=GEMINI_API_KEY, 
        temperature=0, 
        model="gemini-2.5-flash"
    )
    response_parser = StrOutputParser()
    
    retrieve_context = {
        "context": combined_retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])), 
        "question": RunnablePassthrough()
    }
    
    RAG_CHAIN = (
        retrieve_context
        | custom_rag_prompt
        | llm
        | response_parser
    )
else:
    RAG_CHAIN = None


# --- Flask Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if RAG_CHAIN is None:
        return jsonify({'response': 'GECA-Bot is offline. RAG system failed to initialize. Please check backend configuration.'}), 503

    try:
        print(f"Invoking RAG chain with query: {user_message}")
        bot_response = RAG_CHAIN.invoke(user_message)
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"An error occurred during RAG chain invocation: {e}")
        return jsonify({'error': 'An internal error occurred while generating the response.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
