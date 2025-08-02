"""
Server startup script for HackRX 5.0
Run this file to start the FastAPI server locally
"""

import uvicorn
from config import Config

if __name__ == "__main__":
    print("🚀 Starting HackRX 5.0 Server...")
    print(f"📡 Server will run on: http://{Config.API_HOST}:{Config.API_PORT}")
    print(f"📖 API Documentation: http://{Config.API_HOST}:{Config.API_PORT}/docs")
    print(f"🔧 Health Check: http://{Config.API_HOST}:{Config.API_PORT}/health")
    print("=" * 60)
    
    uvicorn.run(
        "app:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.API_RELOAD,
        log_level="info"
    )
