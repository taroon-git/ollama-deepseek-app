# Ollama DeepSeek API

## Overview
This project is a FastAPI-based application that interacts with the **DeepSeek** LLM model using **Ollama**. The API takes user queries and returns AI-generated responses. Additionally, it maintains conversation history and provides a clear history feature.

## Features
- Accepts user queries and returns AI-generated responses.
- Maintains a conversation history.
- Provides an endpoint to clear the conversation history.
- Can be deployed using **Render** for free hosting.

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **FastAPI & Uvicorn**
- **Git**
- **Ollama installed and running**

### Clone the Repository
```bash
git clone https://github.com/taroon-git/ollama-deepseek-app.git
cd ollama-deepseek-app
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Pull the DeepSeek Model for Ollama
```bash
ollama pull deepseek-r1
```

### Run the API Locally
```bash
uvicorn main:app --reload
```
The API will be available at **http://127.0.0.1:8000/**

## API Endpoints

### 1. Query the Model
- **URL:** `/query/`
- **Method:** `POST`
- **Request Body:**
```json
{
  "query": "What is DeepSeek?"
}
```
- **Response:**
```json
{
  "response": "DeepSeek is an AI language model..."
}
```

### 2. Get Conversation History
- **URL:** `/history/`
- **Method:** `GET`
- **Response:**
```json
{
  "history": [
    { "query": "Hello", "response": "Hi! How can I help you?" },
    { "query": "Tell me about AI", "response": "AI stands for Artificial Intelligence..." }
  ]
}
```

### 3. Clear Conversation History
- **URL:** `/clear_history/`
- **Method:** `DELETE`
- **Response:**
```json
{ "message": "History cleared" }
```

## Deployment on Render

### Steps:
1. **Push your code to GitHub.**
2. **Login to [Render](https://dashboard.render.com/).**
3. **Create a new Web Service and connect your GitHub repository.**
4. **Set the Start Command:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```
5. **Deploy and access your API via Render's provided URL.**

## Troubleshooting
- **If port is busy:** Run `pkill -f uvicorn` and restart.
- **If API key is needed for DeepSeek:** Store it in `.env` file and load using `dotenv`.
- **If deployment fails:** Check logs in Render and verify `requirements.txt`.

## Author
Developed by **Tarun** 🚀

