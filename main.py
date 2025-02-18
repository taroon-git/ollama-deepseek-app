import os
import requests
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# Store conversation history
conversation_history = []

# Pydantic model for requests
class QueryRequest(BaseModel):
    query: str

# Function to get response from OpenRouter DeepSeek model
def get_deepseek_response(query: str):
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",  # Optional
        "X-Title": "Your App Name"  # Optional
    }

    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": query}],
    }

    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=45)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Serve frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("templates/index.html")

# Handle queries and save history
@app.post("/query/")
async def handle_query(request: QueryRequest):
    response = get_deepseek_response(request.query)
    conversation_history.append({"query": request.query, "response": response})
    return {"response": response}

# Get conversation history
@app.get("/history/")
async def get_history():
    return {"history": conversation_history}

# Clear conversation history
@app.delete("/clear_history/")
async def clear_history():
    global conversation_history
    conversation_history = []
    return {"message": "History cleared"}
