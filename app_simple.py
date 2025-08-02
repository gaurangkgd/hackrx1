"""
HackRX 5.0 - Simplified LLM-Powered Query-Retrieval System
FastAPI application for processing documents and answering questions (Railway optimized)
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import tempfile
import shutil
from urllib.parse import urlparse
import requests

# FastAPI imports
from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Document processing imports
from docx import Document
import PyPDF2
import google.generativeai as genai

# Import configuration
from config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Validate configuration on startup
Config.validate_config()

# Initialize FastAPI app
app = FastAPI(
    title="HackRX 5.0 - Intelligent Query-Retrieval System",
    description="LLM-Powered system for processing documents and answering contextual queries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Gemini API configuration
genai.configure(api_key=Config.GEMINI_API_KEY)

# Pydantic models
class QueryRequest(BaseModel):
    documents: str = Field(..., description="URL to the document blob")
    questions: List[str] = Field(..., min_items=1, description="List of questions to answer")

class QueryResponse(BaseModel):
    answers: List[str] = Field(..., description="List of answers corresponding to the questions")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class FileUploadResponse(BaseModel):
    answers: List[str] = Field(..., description="List of answers corresponding to the questions")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    filename: str = Field(..., description="Name of the uploaded file")

# Helper functions
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify bearer token"""
    if credentials.credentials != Config.BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing DOCX: {str(e)}")

def download_document(url: str) -> str:
    """Download document from URL"""
    try:
        response = requests.get(url, timeout=Config.DOWNLOAD_TIMEOUT)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(response.content)
            return tmp_file.name
    except Exception as e:
        logger.error(f"Error downloading document: {e}")
        raise HTTPException(status_code=400, detail=f"Error downloading document: {str(e)}")

def process_with_gemini(text: str, questions: List[str]) -> List[str]:
    """Process questions using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        answers = []
        
        for question in questions:
            prompt = f"""
            Document Text:
            {text[:8000]}  # Limit text to avoid token limits
            
            Question: {question}
            
            Please provide a clear, concise answer based on the document content. If the answer is not found in the document, say "Information not found in the document."
            """
            
            response = model.generate_content(prompt)
            answers.append(response.text.strip())
        
        return answers
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing with AI: {str(e)}")

# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HackRX 5.0 Query-Retrieval System"
    }

@app.post("/hackrx/run", response_model=QueryResponse)
async def process_document_url(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """Process document from URL and answer questions"""
    try:
        logger.info(f"Processing document from URL: {request.documents}")
        
        # Download document
        temp_file = download_document(request.documents)
        
        try:
            # Extract text based on file type
            if temp_file.lower().endswith('.pdf'):
                text = extract_text_from_pdf(temp_file)
            else:
                text = extract_text_from_pdf(temp_file)  # Assume PDF for URL
            
            # Process with Gemini
            answers = process_with_gemini(text, request.questions)
            
            metadata = {
                "document_url": request.documents,
                "total_questions": len(request.questions),
                "processing_timestamp": datetime.now().isoformat(),
                "model_info": {
                    "llm": "gemini-pro",
                    "text_length": len(text)
                }
            }
            
            return QueryResponse(answers=answers, metadata=metadata)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in process_document_url: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/hackrx/upload", response_model=FileUploadResponse)
async def process_file_upload(
    file: UploadFile = File(...),
    questions: str = Form(...),
    token: str = Depends(verify_token)
):
    """Process uploaded file and answer questions"""
    try:
        # Parse questions from JSON string
        questions_list = json.loads(questions)
        
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Validate file type
        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            temp_file_path = tmp_file.name
        
        try:
            # Extract text based on file type
            if file_ext == '.pdf':
                text = extract_text_from_pdf(temp_file_path)
            elif file_ext in ['.doc', '.docx']:
                text = extract_text_from_docx(temp_file_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            # Process with Gemini
            answers = process_with_gemini(text, questions_list)
            
            metadata = {
                "total_questions": len(questions_list),
                "processing_timestamp": datetime.now().isoformat(),
                "file_size": len(content),
                "model_info": {
                    "llm": "gemini-pro",
                    "text_length": len(text)
                }
            }
            
            return FileUploadResponse(
                answers=answers,
                metadata=metadata,
                filename=file.filename
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for questions")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in process_file_upload: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.API_RELOAD
    )
