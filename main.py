from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

from index import generate_response

load_dotenv()

app = FastAPI(title="GECA Chatbot", version="1.0.0")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class MessageRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate_response")
async def generate_response_endpoint(payload: MessageRequest):
    user_message = payload.message.strip()
    if not user_message:
        return JSONResponse({"error": "No message provided"}, status_code=400)

    try:
        bot_response = generate_response(user_message)
        return JSONResponse({"response": bot_response})
    except RuntimeError:
        return JSONResponse(
            {"response": "GECA-Bot is offline. RAG system failed to initialize. Please check backend configuration."},
            status_code=503,
        )
    except Exception:
        return JSONResponse(
            {"error": "An internal error occurred while generating the response."},
            status_code=500,
        )
