# 🎓 GECA Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0.3-orange.svg)](https://www.langchain.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/atlas)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> A modern, RAG-based (Retrieval-Augmented Generation) intelligent chatbot for Government College of Engineering, Aurangabad (GECA). Built with FastAPI, LangChain, and cutting-edge LLM technology.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Customization](#-customization)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Authors](#-authors)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

GECA Chatbot is an AI-powered academic assistant designed to help students, faculty, and visitors get instant answers about Government College of Engineering, Aurangabad. Using advanced RAG (Retrieval-Augmented Generation) architecture, the bot retrieves relevant information from a vector database and generates contextual responses using state-of-the-art LLMs.

### Key Capabilities

- **Syllabus Queries**: Get detailed information about course structures, subjects, and curriculum
- **Faculty Information**: Access details about professors, departments, and contact information
- **Timetable Management**: Check class schedules, timings, and room allocations
- **Exam & Lab Info**: Stay updated on examination schedules and laboratory sessions
- **Campus Guidance**: General information about college facilities and student life

---

## ✨ Features

### 🤖 Intelligent Conversational AI
- Natural language understanding with context awareness
- Multi-turn conversations with memory
- Intelligent fallback responses for out-of-scope queries

### 🔍 Advanced RAG Pipeline
- Vector similarity search with MongoDB Atlas
- Multi-collection retrieval (Syllabus, Faculty, Timetable)
- Configurable retrieval parameters (top-k, similarity thresholds)

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Beautiful frosted glass aesthetic
- **Dark/Light Themes**: Automatic and manual theme switching
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Typing Indicators**: Smooth animations and feedback
- **Message Bubbles**: WhatsApp/Telegram-style chat interface

### 🛠️ Developer Friendly
- Modular and extensible architecture
- Environment-based configuration
- Comprehensive logging and debugging
- Docker support for containerized deployment
- Detailed documentation (setup.md, reform.md)

### 🚀 Production Ready
- RESTful API with FastAPI
- Async request handling
- Error handling and graceful degradation
- Health check endpoints
- Scalable vector database backend

---

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **RAG Framework**: [LangChain](https://www.langchain.com/) - Framework for LLM applications
- **Vector Database**: [MongoDB Atlas](https://www.mongodb.com/atlas) with Vector Search
- **Server**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

### AI/ML Components
- **LLMs**: 
  - [Google Gemini](https://ai.google.dev/) (gemini-2.5-flash-lite) - Response generation
  - [Groq](https://groq.com/) (llama-3.1-8b-instant) - RAG query processing
- **Embeddings**: [HuggingFace](https://huggingface.co/) (all-MiniLM-L6-v2) - Text vectorization

### Frontend
- **HTML5/CSS3**: Semantic markup with modern CSS features
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Fonts**: [Inter](https://fonts.google.com/specimen/Inter) - Professional typography
- **Icons**: [Font Awesome](https://fontawesome.com/) - Comprehensive icon set

### Deployment
- **Containerization**: Docker & Docker Compose ready
- **Cloud Platforms**: Vercel, Render.com compatible
- **Environment**: Python 3.8+ virtual environment

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (UI)                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  HTML5 + CSS3 + JavaScript (Glassmorphism UI)       │    │
│  └───────────────────┬─────────────────────────────────┘    │
└───────────────────────┼─────────────────────────────────────┘
                        │ HTTP/REST
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI (main.py)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  / (Home)  │  /generate_response (POST)             │    │
│  └───────────────────┬─────────────────────────────────┘    │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              RAG Orchestration (index.py)                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Gemini LLM  │  Prompt Templates  │  Response       │    │
│  └───────────────────┬─────────────────────────────────┘    │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                RAG Pipeline (rag.py)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Query → Multi-Retriever → Context → Groq LLM       │    │
│  └───────────────────┬─────────────────────────────────┘    │
└───────────────────────┼─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Syllabus   │ │   Faculty    │ │  Timetable   │
│  Collection  │ │  Collection  │ │  Collection  │
└──────────────┘ └──────────────┘ └──────────────┘
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ MongoDB Atlas + Vector Search │
        └───────────────────────────────┘
```

---

## 📁 Project Structure

```
geca-chatbot/
├── 📄 main.py                    # FastAPI application entry point
├── 📄 index.py                   # RAG orchestration with Gemini LLM
├── 📄 rag.py                     # Core RAG pipeline with vector search
├── 📄 serve.py                   # Server startup script
├── 📄 load_data.py               # Load syllabus PDF to MongoDB
├── 📄 load_data_csv.py           # Load timetable CSV to MongoDB
├── 📄 load_data_pdf.py           # Load faculty PDF to MongoDB
├── 📄 create_vector_index.py     # Create MongoDB vector search indexes
├── 📄 empty_collection.py       # Utility to clear MongoDB collections
├── 📁 templates/
│   └── index.html                # Frontend chat interface
├── 📁 static/
│   ├── 📁 css/
│   │   └── style.css             # Modern glassmorphism styles
│   ├── 📁 js/
│   │   └── script.js             # Frontend JavaScript logic
│   └── 📁 icons/
│       └── logoacsn.png          # College logo
├── 📁 Data/                      # Data directory (not in repo)
│   ├── NEP_SYCSE.pdf             # Syllabus PDF
│   ├── timetable.csv             # Timetable CSV
│   └── Faculty.pdf               # Faculty PDF
├── 📄 requirements.txt           # Python dependencies
├── 📄 setup.md                   # Detailed setup instructions
├── 📄 reform.md                  # Customization guide
├── 📄 vercel.json                # Vercel deployment config
├── 📄 render.yaml                # Render.com deployment config
├── 📄 .env.example               # Environment variables template
├── 📄 .gitignore                 # Git ignore rules
└── 📄 README.md                  # This file
```

---

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB for dependencies + data

### Accounts & API Keys
1. **MongoDB Atlas Account** - [Sign up free](https://www.mongodb.com/cloud/atlas/register)
2. **Google Gemini API Key** - [Get it here](https://aistudio.google.com/app/apikey)
3. **Groq API Key** - [Get it here](https://console.groq.com/keys)
4. **HuggingFace API Token** - [Get it here](https://huggingface.co/settings/tokens)

---

## 🚀 Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Meeran-Dev/geca-chatbot.git
cd geca-chatbot

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys (see Configuration section)

# Load data into MongoDB
python load_data.py
python load_data_csv.py
python load_data_pdf.py

# Create vector indexes
python create_vector_index.py

# Run the application
python serve.py
```

### Detailed Setup

For comprehensive setup instructions, troubleshooting, and alternative installation methods, see **[setup.md](setup.md)**.

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required: LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# Required: Database
MONGODB_URI=mongodb+srv://username:password@cluster-url/?retryWrites=true&w=majority

# Optional: Server Configuration
PORT=5000
LOG_LEVEL=info
```

### MongoDB Atlas Setup

1. Create a cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create database: `Second-Year-CSE`
3. Create collections: `Syllabus`, `Faculty`, `Time-Table`
4. Enable Vector Search in cluster settings
5. Whitelist your IP (or use `0.0.0.0/0` for development)

---

## 💡 Usage

### Starting the Chatbot

```bash
python serve.py
```

Or directly with uvicorn:

```bash
uvicorn main:app --reload
```

### Accessing the Interface

Open your browser and navigate to:

```
http://localhost:5000
```

### Example Queries

**Syllabus:**
- "What subjects are in SEM 3 CSE?"
- "Tell me about the Mathematics syllabus"
- "What are the electives available?"

**Faculty:**
- "Who teaches Database Management?"
- "Tell me about the CSE department faculty"
- "How to contact the HOD?"

**Timetable:**
- "What's my schedule for Monday?"
- "When is the Database lab?"
- "Show me the timetable for SE CSE"

**General:**
- "How to apply for leave?"
- "What are the library timings?"
- "Tell me about college fest"

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### `GET /`
Serves the chat interface.

**Response**: HTML page

---

#### `POST /generate_response`
Generate chatbot response for user message.

**Request Body:**
```json
{
  "message": "What is the syllabus for SEM 3?"
}
```

**Success Response (200):**
```json
{
  "response": "For SEM 3 CSE, the subjects are..."
}
```

**Error Response (400):**
```json
{
  "error": "No message provided"
}
```

**Error Response (503):**
```json
{
  "response": "GECA-Bot is offline. RAG system failed to initialize."
}
```

### Interactive API Docs

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

---

## 🌐 Deployment

### Docker Deployment

```bash
# Build the image
docker build -t geca-chatbot .

# Run the container
docker run -p 5000:5000 --env-file .env geca-chatbot
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
```

Run:
```bash
docker-compose up -d
```

### Cloud Platforms

#### Vercel
```bash
vercel --prod
```

#### Render.com
1. Connect GitHub repository
2. Add environment variables
3. Auto-deploy on push

For detailed deployment guides, see **[setup.md](setup.md)**.

---

## 🎨 Customization

Want to replace the data with your own and customize the chatbot for your institution?

See **[reform.md](reform.md)** for comprehensive guides on:
- Setting up your own MongoDB database
- Adding new data sources (PDF, CSV, JSON)
- Modifying the RAG pipeline
- Extending with new collections
- Updating UI themes and prompts

---

## 🧪 Testing

### Test MongoDB Connection
```bash
python -c "from rag import embeddings; print('OK' if embeddings else 'FAILED')"
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/

# Test chatbot
curl -X POST http://localhost:5000/generate_response \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello\"}"
```

### Run Tests
```bash
# (If you have test files)
pytest tests/
```

---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add comments for complex logic
- Update documentation as needed
- Test your changes thoroughly

---

## 🔍 Troubleshooting

### Common Issues

#### "Embedding error" / "HUGGINGFACEHUB_API_TOKEN not set"
- Verify your HuggingFace token in `.env`
- Ensure token has proper permissions

#### "MongoDB connection error"
- Check `MONGODB_URI` format
- Verify IP whitelist in MongoDB Atlas
- Test connection: `mongosh "<your-connection-string>"`

#### "RAG system failed to initialize"
- Ensure data is loaded: `python -c "from rag import retriever_syllabus; print(retriever_syllabus)"`
- Check all API keys are valid
- Review server logs for details

#### "No vector index found"
```bash
python create_vector_index.py
```

For more issues and solutions, see **[setup.md](setup.md)**.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 👨‍💻 Authors

- **Meeran**  - [GitHub Profile](https://github.com/Meeran-Dev)
- **Adarsh** - [GitHub Profile](https://github.com/adarsh-singh106)
- **Aditya** - [GitHub Profile](https://github.com/username)
- **chaitanya**  - [GitHub Profile](https://github.com/username)

---

## 🙏 Acknowledgments

- **GECA (Government College of Engineering, Aurangabad)** for the opportunity
- **LangChain** team for the excellent RAG framework
- **MongoDB Atlas** for the powerful vector search capabilities
- **Google Gemini & Groq** for providing cutting-edge LLMs
- **HuggingFace** for the embedding models

---

## 📞 Contact

For questions, issues, or collaborations:

- **Email**: mdmeeran.86684@gmail.com
- **GitHub Issues**: [Report a bug](https://github.com/Meeran-Dev/geca-chatbot/issues)
- **Project Link**: [https://github.com/Meeran-Dev/geca-chatbot](https://github.com/Meeran-Dev/geca-chatbot)

---

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

<div align="center">
  <p>Built with ❤️ for GECA</p>
  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python">
    </a>
    <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
    </a>
  </p>
</div>
