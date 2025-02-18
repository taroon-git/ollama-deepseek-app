# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests

# app = FastAPI()

# class QueryRequest(BaseModel):
#     query: str

# def get_deepseek_response(query: str):
#     api_url = "http://localhost:11434/api/generate"

#     data = {
#         "model": "deepseek-r1",
#         "prompt": query,
#         "stream": False
#     }

#     try:
#         response = requests.post(api_url, json=data, timeout=30)
#         response.raise_for_status()

#         # Extract response
#         response_json = response.json()
#         formatted_response = response_json.get("response", "No response received.")

#         # Formatting the response properly
#         return {"response": formatted_response.strip()}  # Removes extra whitespace

#     except requests.exceptions.Timeout:
#         return {"error": "DeepSeek took too long to respond. Try again later."}
#     except requests.exceptions.RequestException as e:
#         return {"error": str(e)}

# @app.post("/query/")
# async def handle_query(request: QueryRequest):
#     response = get_deepseek_response(request.query)
#     return response

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()

# List to store conversation history
conversation_history = []

# Pydantic model to parse incoming queries
class QueryRequest(BaseModel):
    query: str

# Function to get response from the DeepSeek model
def get_deepseek_response(query: str):
    api_url = "http://localhost:11434/api/generate"

    data = {
        "model": "deepseek-r1",  # Ensure you're using the correct model name
        "prompt": query,
        "stream": False
    }

    try:
        response = requests.post(api_url, json=data, timeout=45)
        response.raise_for_status()
        return response.json().get("response", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Endpoint to serve the frontend (index.html)
@app.get("/")
async def serve_frontend():
    return FileResponse("templates/index.html")

# Endpoint to handle user queries and save history
@app.post("/query/")
async def handle_query(request: QueryRequest):
    # Get response from DeepSeek model
    response = get_deepseek_response(request.query)
    
    # Save the query and response in conversation history
    conversation_history.append({"query": request.query, "response": response})
    
    return {"response": response}

# Endpoint to get the conversation history
@app.get("/history/")
async def get_history():
    return {"history": conversation_history}


@app.delete("/clear_history/")
async def clear_history():
    global conversation_history
    conversation_history = []  # Clear the conversation history
    return {"message": "History cleared"}
