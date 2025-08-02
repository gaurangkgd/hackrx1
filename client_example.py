"""
Python example for using the HackRX 5.0 file upload API
This script shows how to integrate the file upload functionality into your own applications
"""

import requests
import json
import os
from typing import List, Dict, Any

class HackRXClient:
    """Client class for interacting with HackRX 5.0 API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", bearer_token: str = None):
        self.base_url = base_url
        self.bearer_token = bearer_token
        self.session = requests.Session()
        
        if bearer_token:
            self.session.headers.update({
                "Authorization": f"Bearer {bearer_token}"
            })
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def process_url(self, document_url: str, questions: List[str]) -> Dict[str, Any]:
        """Process document from URL"""
        payload = {
            "documents": document_url,
            "questions": questions
        }
        
        response = self.session.post(
            f"{self.base_url}/hackrx/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    
    def process_file(self, file_path: str, questions: List[str]) -> Dict[str, Any]:
        """Process local file upload"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, self._get_content_type(file_path))
            }
            data = {
                'questions': json.dumps(questions)
            }
            
            response = self.session.post(
                f"{self.base_url}/hackrx/upload",
                files=files,
                data=data,
                timeout=300
            )
        
        response.raise_for_status()
        return response.json()
    
    def _get_content_type(self, file_path: str) -> str:
        """Get content type based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.eml': 'message/rfc822',
            '.msg': 'application/octet-stream'
        }
        return content_types.get(ext, 'application/octet-stream')

def example_usage():
    """Example usage of the HackRX client"""
    
    # Initialize client
    client = HackRXClient(
        base_url="http://localhost:8000",
        bearer_token="d23b6db093b3dce5948ae2389ba8db77a4847fa7c2990e66650a4cc6092d0042"
    )
    
    # Sample questions
    questions = [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?",
        "Does this policy cover maternity expenses?"
    ]
    
    try:
        # Check server health
        print("🏥 Checking server health...")
        health = client.health_check()
        print(f"✅ Server is healthy (device: {health.get('device', 'unknown')})")
        
        # Example 1: Process document from URL
        print("\n🌐 Processing document from URL...")
        url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
        
        try:
            url_result = client.process_url(url, questions)
            print("✅ URL processing successful!")
            print(f"Answers received: {len(url_result['answers'])}")
            
            for i, (q, a) in enumerate(zip(questions, url_result['answers']), 1):
                print(f"\nQ{i}: {q}")
                print(f"A{i}: {a}")
        
        except Exception as e:
            print(f"❌ URL processing failed: {e}")
        
        # Example 2: Process local file upload
        print("\n\n📁 Processing local file upload...")
        
        # Look for a sample file
        sample_files = ["sample.pdf", "test.pdf", "document.pdf", "policy.pdf"]
        sample_file = None
        
        for file_path in sample_files:
            if os.path.exists(file_path):
                sample_file = file_path
                break
        
        if sample_file:
            try:
                file_result = client.process_file(sample_file, questions)
                print("✅ File upload processing successful!")
                print(f"Processed file: {file_result.get('filename', 'N/A')}")
                print(f"Answers received: {len(file_result['answers'])}")
                
                for i, (q, a) in enumerate(zip(questions, file_result['answers']), 1):
                    print(f"\nQ{i}: {q}")
                    print(f"A{i}: {a}")
            
            except Exception as e:
                print(f"❌ File upload processing failed: {e}")
        else:
            print("⚠️  No sample PDF files found for testing file upload")
            print(f"   Place one of these files in the current directory: {', '.join(sample_files)}")
    
    except Exception as e:
        print(f"❌ Client error: {e}")

def batch_processing_example():
    """Example of processing multiple files in batch"""
    print("\n" + "="*60)
    print("📦 Batch Processing Example")
    print("="*60)
    
    client = HackRXClient(
        base_url="http://localhost:8000",
        bearer_token="d23b6db093b3dce5948ae2389ba8db77a4847fa7c2990e66650a4cc6092d0042"
    )
    
    # Sample questions for batch processing
    questions = ["What is the main topic of this document?", "What are the key terms?"]
    
    # Look for multiple files
    files_to_process = []
    for file_name in os.listdir("."):
        if file_name.endswith(('.pdf', '.doc', '.docx')):
            files_to_process.append(file_name)
    
    if not files_to_process:
        print("⚠️  No documents found for batch processing")
        return
    
    print(f"Found {len(files_to_process)} files to process:")
    for file_name in files_to_process:
        print(f"  • {file_name}")
    
    results = []
    for file_path in files_to_process:
        try:
            print(f"\n📄 Processing {file_path}...")
            result = client.process_file(file_path, questions)
            results.append({
                'file': file_path,
                'success': True,
                'answers': result['answers']
            })
            print(f"✅ {file_path} processed successfully")
        
        except Exception as e:
            print(f"❌ Failed to process {file_path}: {e}")
            results.append({
                'file': file_path,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n📊 Batch Processing Summary:")
    successful = len([r for r in results if r['success']])
    print(f"Processed: {successful}/{len(results)} files")
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['file']}")

if __name__ == "__main__":
    print("🚀 HackRX 5.0 Client Examples")
    print("="*60)
    
    # Basic usage example
    example_usage()
    
    # Batch processing example
    batch_processing_example()
    
    print("\n" + "="*60)
    print("💡 Integration Tips:")
    print("1. Always check server health before processing")
    print("2. Handle exceptions gracefully in production")
    print("3. Use appropriate timeouts for large files")
    print("4. Consider batching for multiple documents")
    print("5. Cache results when possible")
    print("="*60)
