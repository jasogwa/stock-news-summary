# Stock News Summary

A small FastAPI application that gives traders a concise, AI-generated briefing of the latest news for a stock ticker. It fetches recent ticker news, normalizes the provider-specific response, asks OpenAI to create a structured summary, and returns the source articles alongside the generated briefing.

The application features a clean, decoupled architecture with a strict TypeScript frontend and a Python backend.

---

## Prerequisites

Before you begin, ensure you have the following installed:
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js & npm](https://nodejs.org/) (for compiling frontend TypeScript)
- [Docker](https://www.docker.com/) (Optional, for containerized deployment)
- An active [OpenAI API Key](https://platform.openai.com/api-keys)

---

## Local Installation

### 1. Clone the repository
```bash
git clone https://github.com/jasogwa/stock-news-summary.git
cd stock-news-summary
```

### 2. Set up the Python Virtual Environment
```bash
python -m venv env

# On Windows:
.\env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Compile the Frontend TypeScript
The frontend uses strict TypeScript that needs to be compiled to ES6 JavaScript before running.
```bash
npx typescript tsc static/main.ts --strict --target ES2022 --module ES6
```

### 5. Configure Environment Variables
Create a `.env` file from the provided example and add your OpenAI API key:
```bash
cp .env.example .env
```
Open the `.env` file in your editor and replace `your_openai_api_key_here` with your actual key.

---

## Running the Application

### Option A: Running Locally (Uvicorn)
With your virtual environment activated, start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Open your browser and navigate to http://127.0.0.1:8000

### Option B: Running with Docker
You can easily build and run the application in an isolated Docker container.

**1. Build the Docker image:**
```bash
docker build -t stock-news-summary .
```

**2. Run the Docker container:**
*(This automatically mounts your `.env` file into the container)*
```bash
docker run -p 8000:8000 --env-file .env stock-news-summary
```
Open your browser and navigate to http://localhost:8000

---

## Testing

The application includes a comprehensive test suite using `pytest`. 

To run the tests, ensure your virtual environment is activated and simply run:
```bash
pytest
```

**What is tested:**
- **API Endpoints:** Ensures the `/api/stocks/{ticker}/summary` endpoint returns the correct 200/400/404 HTTP status codes and perfectly formatted JSON schemas.
- **News Provider (`app/services/news.py`):** Tests the robust normalization logic used to parse wildly different Yahoo Finance API payload shapes.
- **Summary Service (`app/services/stock_summary.py`):** Verifies the orchestration between the News Provider and the OpenAI Summarizer.

---

## Architecture & Documentation

For a deep dive into the System Requirements Specification (SRS), decoupled architecture, exception handling, and execution flow, please read the [Architecture Documentation](docs/ARCHITECTURE.md).
