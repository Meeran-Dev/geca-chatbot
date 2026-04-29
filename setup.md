# GECA Chatbot - Setup & Installation Guide

## Overview
GECA Chatbot is a RAG-based (Retrieval-Augmented Generation) college assistant for Government College of Engineering, Aurangabad (GECA). It uses FastAPI, LangChain, MongoDB Atlas Vector Search, and multiple LLM providers (Gemini & Groq).

---

## Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **MongoDB Atlas Account** - [Sign up](https://www.mongodb.com/cloud/atlas/register)
- **Git** - [Download](https://git-scm.com/downloads)

### Required API Keys
1. **Google Gemini API Key** - [Get it here](https://aistudio.google.com/app/apikey)
2. **Groq API Key** - [Get it here](https://console.groq.com/keys)
3. **HuggingFace API Token** - [Get it here](https://huggingface.co/settings/tokens)

---

## Quick Start (Local Development)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd geca-chatbot
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
MONGODB_URI=your_mongodb_atlas_connection_string
PORT=5000
```

**MongoDB Atlas Setup:**
1. Create a cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database named `Second-Year-CSE`
3. Enable Vector Search in your cluster
4. Get connection string from "Connect" → "Drivers" → "Python"
5. Replace `<password>` with your database password

### Step 5: Prepare Data Files

Create a `Data/` directory and add required files:
```
Data/
├── NEP_SYCSE.pdf      # Syllabus PDF
├── timetable.csv       # Timetable CSV
└── Faculty.pdf         # Faculty PDF
```

### Step 6: Load Data into MongoDB

```bash
python load_data.py        # Load syllabus data
python load_data_csv.py    # Load timetable data
python load_data_pdf.py    # Load faculty data
```

### Step 7: Create Vector Indexes

```bash
python create_vector_index.py
```

### Step 8: Run the Application

```bash
python serve.py
```

Or directly with uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### Step 9: Access the Chatbot

Open your browser and navigate to:
```
http://localhost:5000
```

---

## Alternative Ways to Run

### 1. Production Mode (Without Reload)

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --workers 4
```

### 2. Using Environment Port

```bash
# Set PORT in .env file or as environment variable
python serve.py
```

### 3. Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

Build and run:
```bash
docker build -t geca-chatbot .
docker run -p 5000:5000 --env-file .env geca-chatbot
```

### 4. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    environment:
      - PORT=5000
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

### 5. Cloud Deployment

#### Vercel (Fixed Configuration)

**Issue:** Current `vercel.json` points to non-existent `api/index.py`

**Fix:** Update `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/main"
    }
  ]
}
```

Deploy:
```bash
vercel --prod
```

#### Render.com (Fixed Configuration)

**Issue:** Current `render.yaml` uses `gunicorn` which is not installed

**Fix:** Update `render.yaml`:
```yaml
services:
  - type: web
    name: geca-chatbot
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --bind 0.0.0.0:$PORT"
```

Deploy:
1. Connect your GitHub repository to Render
2. Add environment variables in Render dashboard
3. Deploy

---

## Data Loading Options

### Option 1: Load All Data at Once
```bash
python load_data.py && python load_data_csv.py && python load_data_pdf.py
```

### Option 2: Reset and Reload
```bash
python empty_collection.py   # Clear existing data
python load_data.py          # Reload syllabus
python load_data_csv.py      # Reload timetable
python load_data_pdf.py      # Reload faculty
python create_vector_index.py  # Recreate indexes
```

### Option 3: Load Individual Collections
```bash
# Only syllabus
python load_data.py

# Only timetable
python load_data_csv.py

# Only faculty
python load_data_pdf.py
```

---

## Testing the Setup

### Test MongoDB Connection
```bash
python -c "from rag import embeddings; print('MongoDB + Embeddings OK' if embeddings else 'FAILED')"
```

### Test API Endpoints
```bash
# Test home page
curl http://localhost:5000/

# Test chatbot response
curl -X POST http://localhost:5000/generate_response \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is the syllabus for SE CSE?\"}"
```

---

## Common Errors & Fixes

### Error 1: "Embedding error" / "HUGGINGFACEHUB_API_TOKEN not set"
**Fix:** Ensure your HuggingFace token is correct in `.env` file

### Error 2: "MongoDB connection error"
**Fix:** 
- Check `MONGODB_URI` in `.env`
- Ensure IP address is whitelisted in MongoDB Atlas (add 0.0.0.0/0 for testing)
- Verify database name is `Second-Year-CSE`

### Error 3: "RAG system failed to initialize"
**Fix:**
- Check all API keys are valid
- Ensure data is loaded: `python -c "from rag import retriever_syllabus; print(retriever_syllabus)"`
- Check MongoDB collections exist

### Error 4: "No vector index found"
**Fix:**
```bash
python create_vector_index.py
```
Or manually create vector index in MongoDB Atlas:
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    }
  ]
}
```

### Error 5: "Module not found" errors
**Fix:**
```bash
pip install --upgrade -r requirements.txt
```

### Error 6: Port already in use
**Fix:**
```bash
# Change port in .env file
PORT=8000

# Or kill existing process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key for response formatting |
| `GROQ_API_KEY` | Yes | - | Groq API key for RAG query processing |
| `HUGGINGFACEHUB_API_TOKEN` | Yes | - | HuggingFace token for embeddings |
| `MONGODB_URI` | Yes | - | MongoDB Atlas connection string |
| `PORT` | No | 5000 | Port for the web server |

---

## Project Structure

```
geca-chatbot/
├── main.py                 # FastAPI application entry point
├── index.py                # RAG orchestration with Gemini LLM
├── rag.py                  # Core RAG pipeline with MongoDB vector search
├── serve.py                # Server startup script
├── load_data.py            # Load syllabus data to MongoDB
├── load_data_csv.py        # Load timetable CSV data to MongoDB
├── load_data_pdf.py        # Load faculty PDF data to MongoDB
├── create_vector_index.py  # Create MongoDB vector search indexes
├── empty_collection.py     # Utility to clear MongoDB collections
├── templates/
│   └── index.html          # Frontend chat interface
├── static/
│   ├── css/style.css       # Styles with dark/light theme
│   └── js/script.js        # Frontend JavaScript
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment config (needs fix)
├── render.yaml             # Render.com config (needs fix)
└── .env                    # Environment variables (create this)
```

---

## Development Tips

### Enable Debug Mode
Add to `.env`:
```env
LOG_LEVEL=debug
```

### Hot Reload During Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

### Check Logs
The application prints detailed logs during startup:
- Embedding initialization
- MongoDB connection status
- Collection document counts
- Vector index status

### Clear Cache
```bash
# Windows
rmdir /s /q __pycache__
rmdir /s /q .venv

# Linux/Mac
rm -rf __pycache__
rm -rf .venv
```

---

## Known Issues to Fix

1. **Vercel config** (`vercel.json`): Points to non-existent `api/index.py` - update to use `main.py`
2. **Render config** (`render.yaml`): Uses `gunicorn` which is not installed - change to `uvicorn`
3. **LangChain imports**: Inconsistent between files (`langchain_huggingface` vs `langchain_community`)
4. **Module-level execution in `rag.py`**: MongoDB tests run at import time - may cause slow startup
5. **Missing Data directory**: PDF/CSV files not included in repo - need to be added manually
6. **`.gitignore` typo**: `__pychache__` should be `__pycache__`

---

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review server logs for detailed error messages
3. Ensure all API keys are valid and have sufficient quota
4. Verify MongoDB Atlas cluster is running and accessible

---

## License

[Add your license information here]
