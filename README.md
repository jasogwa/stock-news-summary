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
```

Activate the virtual environment:

- Windows:

    ```bash
    source env/Scripts/activate
    ```

- Linux/Mac:

    ```bash
    source env/bin/activate
    ```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Compile the Frontend TypeScript
The frontend uses strict TypeScript that needs to be compiled to ES6 JavaScript before running.
```bash
npx -p typescript tsc static/main.ts --strict --target ES2022 --module ES6
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

## Summary of Tools & Techniques Used

- **Backend:** Python 3.10+ with **FastAPI** for a fast, modern, and asynchronous HTTP API.
- **Frontend:** HTML, CSS, and strict **TypeScript** (compiled to ES6) for a clean, single-page UI.
- **Data Validation:** **Pydantic** was used both for validating incoming API requests and mapping OpenAI's structured JSON outputs securely to internal data models.
- **Design Pattern (Dependency Inversion):** Used Python `Protocols` to create abstraction layers for the `NewsProvider` and `Summarizer`. This technique decouples the business logic from external dependencies (yfinance/OpenAI), keeping the app highly extensible and easily testable.
- **Testing:** **pytest** combined with mocked services to ensure deterministic tests that don't rely on live network access or real API keys.
- **Containerization:** **Docker** for isolated and consistent deployment environments.

## Design Decisions

- **Decoupled Architecture**: The system cleanly separates the HTTP API layer (`routers`), business orchestration (`services/stock_summary`), and external integrations (`news` and `summarizer`). This ensures that external dependencies (like the news source or AI model) can be swapped out with minimal impact.
- **Protocol-based Abstractions**: The `NewsProvider` and `Summarizer` interfaces use Python `Protocol`s. This makes it trivial to mock these dependencies for deterministic testing without needing live network access or real API keys.
- **Direct LLM Context vs RAG**: Given the scope is to summarize 5-10 recent articles for a single stock, the articles are injected directly into the prompt context rather than building a complex Vector DB / RAG setup. This keeps the application simple and fast while still fulfilling the requirements.
- **Pydantic Structured Output**: We use OpenAI's JSON schema output feature mapping directly to a Pydantic model (`StockSummary`) to ensure the AI always returns a rigorously typed and expected JSON format.

## Architecture & Documentation

For a deep dive into the System Requirements Specification (SRS), exception handling, and full execution flow diagrams, please read the comprehensive [Architecture Documentation](docs/ARCHITECTURE.md).
