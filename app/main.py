from fastapi import FastAPI, HTTPException
from .models import IngestRequest, QueryRequest
from .rag import ingest_paths, answer
import glob

# Create FastAPI instance
app = FastAPI(title="RAG API")

# Root endpoint to return a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API"}

# Ingest endpoint to process document files
@app.post("/ingest")
def ingest(req: IngestRequest):
    # Expand paths based on the given patterns
    expanded = []
    for pattern in req.paths:
        matches = glob.glob(pattern)
        if matches:
            expanded.extend(matches)
    # If no files match, return error
    if not expanded:
        raise HTTPException(400, "No files matched the given paths.")
    # Call the ingest function to process the files
    result = ingest_paths(req.tenant_id, expanded)
    return {"ok": True, **result}

# Query endpoint to process a user's question
@app.post("/query")
def query(req: QueryRequest):
    # Call the answer function to get the response to the query
    return answer(req.tenant_id, req.question)
