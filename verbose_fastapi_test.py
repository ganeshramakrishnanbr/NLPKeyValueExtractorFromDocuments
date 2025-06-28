"""
Simple FastAPI server test with detailed logging
"""
import sys
import os
import socket
import uvicorn
import logging
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("fastapi_test")

# Create FastAPI application
app = FastAPI(title="FastAPI Test Server")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return {
        "message": "Hello World",
        "python_version": sys.version,
        "hostname": hostname,
        "local_ip": local_ip,
        "environment": dict(os.environ)
    }

@app.get("/health")
async def health():
    logger.info("Health check endpoint accessed")
    return {"status": "OK"}

if __name__ == "__main__":
    logger.info(f"Starting FastAPI server with Python {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    # Create a test socket to verify binding works
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = "127.0.0.1"
    server_port = 7600
    
    try:
        logger.info(f"Testing socket binding to {server_addr}:{server_port}")
        test_socket.bind((server_addr, server_port))
        logger.info("Socket binding successful")
        test_socket.close()
        
        # Start uvicorn with detailed logs
        logger.info(f"Starting uvicorn on {server_addr}:{server_port}")
        uvicorn.run(
            app, 
            host=server_addr, 
            port=server_port,
            log_level="debug"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        sys.exit(1)
