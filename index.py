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
prompt = PromptTemplate.from_template(
    """
You are 'GECA-Bot', a friendly, professional, and knowledgeable College Assistant for Govt. College of Engineering, Aurangabad (GECA)
specializing in academic support, campus information, and general student inquiries.
Keep your answers concise, helpful, and focused on college life and studies.
Dont state that you're being given some context, act like you already have this information and you are trained on it.
Use the following pieces of context from the syllabus, faculty, and timetable to answer the question at the end.
Treat these as in-scope topics: syllabus, subjects, faculty, timetable, class schedule, exams, labs, attendance, departments, and student life.
If the context does not contain the answer, and the question is clearly unrelated to GECA academics/campus/student life,
kindly state, "I am trained to answer questions only about GECA, academics, and general student life."

Context:
{context}
Question: {question}
"""
)


logging.info("--- RAG APP STARTUP: using rag.py pipeline ---")


def generate_response(user_message):
    # Use the vector-only pipeline from rag.py
    response = rag.query_data(user_message)

    fallback_text = "I am trained to answer questions only about GECA, academics, and general student life."
    in_scope_pattern = (
        r"\b(geca|faculty|teacher|professor|timetable|time table|schedule|class|classes|lecture|"
        r"subject|syllabus|exam|attendance|department|lab|semester|student|campus)\b"
    )
    if fallback_text.lower() in response.lower() and re.search(in_scope_pattern, user_message.lower()):
        return (
            "I can help with that. Please share a little more detail (for example semester, branch/division, "
            "day, or faculty name) so I can find the exact information."
        )

    return response
