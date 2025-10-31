from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI

from pymongo import MongoClient

from dotenv import load_dotenv
import os

load_dotenv()

dbName = "Second-Year-CSE"
index = "vector_index"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

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
).as_retriever(search_kwargs={"k": 3})

retriever_timetable = MongoDBAtlasVectorSearch.from_connection_string(
    os.environ["MONGODB_URI"],
    dbName + "." + "Time-Table", 
    embeddings,
    index_name=index,
).as_retriever(search_kwargs={"k": 24})


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
        "context": combined_retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])), 
        "question": RunnablePassthrough()
        } 
    
    llm = ChatGoogleGenerativeAI(
    google_api_key = os.environ["GEMINI_API_KEY"], 
    temperature = 0, 
    model = "gemini-2.5-flash"
    )

    response_parser = StrOutputParser()

    rag_chain = (
        retrieve_context
        | custom_rag_prompt
        | llm
        | response_parser
    )

    answer = rag_chain.invoke(query)
    return answer

print(query_data("Which classes are there on Friday?"))