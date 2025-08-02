"""
Test script for file upload functionality in HackRX 5.0 API
Tests the /hackrx/upload endpoint with local file uploads
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
BASE_URL = "http://localhost:8000"
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "your-bearer-token-here")

# Headers for authentication
headers = {
    "Accept": "application/json", 
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# Sample questions for testing
sample_questions = [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?",
    "Does this policy cover maternity expenses?",
    "What is the waiting period for cataract surgery?",
    "Are medical expenses for organ donors covered?"
]

def test_file_upload_endpoint(file_path: str):
    """Test the file upload endpoint with a local file"""
    print(f"\nTesting file upload endpoint with: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        # Prepare files and data for upload
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, 'application/pdf')
            }
            data = {
                'questions': json.dumps(sample_questions)
            }
            
            print(f"📤 Uploading file: {os.path.basename(file_path)}")
            print(f"📝 Questions: {len(sample_questions)}")
            
            response = requests.post(
                f"{BASE_URL}/hackrx/upload",
                headers=headers,
                files=files,
                data=data,
                timeout=300  # 5 minutes timeout
            )
        
        if response.status_code == 200:
            print("✅ File upload successful!")
            result = response.json()
            
            print(f"\n📄 Processed file: {result.get('filename', 'Unknown')}")
            print(f"📊 Received {len(result['answers'])} answers:")
            
            for i, (question, answer) in enumerate(zip(sample_questions, result['answers']), 1):
                print(f"\n🔍 Q{i}: {question}")
                print(f"💡 A{i}: {answer}")
            
            if 'metadata' in result:
                metadata = result['metadata']
                print(f"\n📋 File Metadata:")
                print(f"   • Filename: {metadata.get('filename', 'N/A')}")
                print(f"   • File Size: {metadata.get('file_size', 'N/A')} bytes")
                print(f"   • Content Type: {metadata.get('content_type', 'N/A')}")
                print(f"   • Processing Time: {metadata.get('processing_timestamp', 'N/A')}")
            
            return True
            
        else:
            print(f"❌ File upload failed: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return False
                
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return False

def test_invalid_file_upload():
    """Test upload with invalid file type"""
    print("\n🧪 Testing invalid file type...")
    
    # Create a temporary text file
    temp_file = "temp_test.txt"
    with open(temp_file, 'w') as f:
        f.write("This is a test text file")
    
    try:
        with open(temp_file, 'rb') as f:
            files = {
                'file': (temp_file, f, 'text/plain')
            }
            data = {
                'questions': json.dumps(["What is this document about?"])
            }
            
            response = requests.post(
                f"{BASE_URL}/hackrx/upload",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 400:
            print("✅ Invalid file type correctly rejected")
        else:
            print(f"❌ Expected 400 error, got: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error in invalid file test: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_both_endpoints():
    """Test both URL and file upload endpoints for comparison"""
    print("\n🔄 Comparing URL vs File Upload endpoints...")
    
    # Test URL endpoint
    url_request = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": sample_questions[:2]  # Use fewer questions for comparison
    }
    
    try:
        print("📡 Testing URL endpoint...")
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {BEARER_TOKEN}"},
            json=url_request,
            timeout=300
        )
        
        if response.status_code == 200:
            print("✅ URL endpoint works")
            url_result = response.json()
            print(f"URL answers: {len(url_result['answers'])}")
        else:
            print(f"❌ URL endpoint failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ URL endpoint error: {str(e)}")

def main():
    """Run file upload tests"""
    print("=" * 70)
    print("HackRX 5.0 - File Upload Test Suite")
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    
    # Test health endpoint first
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is healthy")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running: python start_server.py")
        return
    
    # Look for PDF files in common locations
    test_files = [
        "sample.pdf",
        "test.pdf", 
        "document.pdf",
        "policy.pdf"
    ]
    
    # Check if any test files exist
    available_files = [f for f in test_files if os.path.exists(f)]
    
    if available_files:
        print(f"\n📁 Found test files: {available_files}")
        for file_path in available_files:
            test_file_upload_endpoint(file_path)
    else:
        print(f"\n⚠️  No test PDF files found in current directory")
        print(f"   Looking for: {', '.join(test_files)}")
        print(f"   Please place a PDF file in the current directory to test file upload")
    
    # Test invalid file type
    test_invalid_file_upload()
    
    # Test both endpoints for comparison
    test_both_endpoints()
    
    print("\n" + "=" * 70)
    print("File Upload Test Suite Completed")
    print("💡 To test with your own file:")
    print("   1. Place a PDF file in the current directory")
    print("   2. Update the test_files list in this script")
    print("   3. Run this script again")
    print("=" * 70)

if __name__ == "__main__":
    main()
