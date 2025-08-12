from fastapi import FastAPI
from pydantic import BaseModel
from .llm_client import chat  # Import the chat function from llm_client.py

app = FastAPI()

class QueryRequest(BaseModel):
    question: str  # The user's question as input

@app.post("/query")
async def query(request: QueryRequest):
    # Get the question from the request
    query = request.question
    
    # Call the chat function (which talks to RunPod) and get the response
    answer = chat(query)
    
    # Return the answer received from RunPod's model
    return {"answer": answer.get("choices", [{}])[0].get("message", {}).get("content", "No answer")}
