from pymongo import MongoClient
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()

class DocumentMetadata(BaseModel):
    title: str = Field(description="The main title or topic of the document chunk.")
    keywords: List[str] = Field(description="A list of important keywords or tags for the content.")


llm = ChatGoogleGenerativeAI(
    google_api_key = os.environ["GEMINI_API_KEY"], 
    temperature = 0, 
    model = "gemini-2.0-flash-lite"
)

parser = PydanticOutputParser(pydantic_object=DocumentMetadata)
prompt = PromptTemplate(
    template = "Extract the following metadata from the text:\n{format_instructions}\n\nText: {text}",
    input_variables = ["text"],
    partial_variables = {"format_instructions": parser.get_format_instructions()},
)
metadata_chain = prompt | llm.with_structured_output(DocumentMetadata)

def gemini_metadata_tagger(documents, chain):
    tagged_documents = []
    for doc in documents:
        try:
            metadata = chain.invoke({"text": doc.page_content})
            doc.metadata.update(metadata.dict())
            tagged_documents.append(doc)

        except Exception as e:
            print(f"Warning: Failed to tag document: {e}")
            tagged_documents.append(doc) 
            
    return tagged_documents


client = MongoClient(os.environ["MONGODB_URI"])
dbName = "Second-Year-CSE"
collectionName = "Faculty"
collection = client[dbName][collectionName]

loader = PyPDFLoader("./Data/Faculty.pdf")
pages = loader.load()
cleaned_pages = []

for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

#docs = gemini_metadata_tagger(cleaned_pages, metadata_chain)
docs = cleaned_pages

split_docs = text_splitter.split_documents(docs)

#embeddings = VoyageAIEmbeddings(voyage_api_key=os.environ["VOYAGE_API_KEY"], model="voyage-3.5-lite")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorStore = MongoDBAtlasVectorSearch.from_documents(
    split_docs, embeddings, collection=collection
)