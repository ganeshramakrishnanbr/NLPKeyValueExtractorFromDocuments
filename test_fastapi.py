"""
Simplified FastAPI test server that just responds with "Hello World"
"""
from fastapi import FastAPI
import uvicorn

# Create FastAPI application
app = FastAPI(title="Test FastAPI Server")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7500)
