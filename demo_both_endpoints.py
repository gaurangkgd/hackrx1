"""
Demo script showing both URL and file upload capabilities of HackRX 5.0
This script demonstrates how to use both endpoints programmatically
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
BEARER_TOKEN = "d23b6db093b3dce5948ae2389ba8db77a4847fa7c2990e66650a4cc6092d0042"

# Sample questions
SAMPLE_QUESTIONS = [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?",
    "Does this policy cover maternity expenses?"
]

def test_url_endpoint():
    """Test the URL-based endpoint"""
    print("🌐 Testing URL-based Document Processing")
    print("-" * 50)
    
    url_request = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": SAMPLE_QUESTIONS
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    try:
        print("📡 Sending request to /hackrx/run...")
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=headers,
            json=url_request,
            timeout=300
        )
        
        if response.status_code == 200:
            print("✅ URL endpoint successful!")
            result = response.json()
            
            print(f"\n📋 Results from URL endpoint:")
            for i, (q, a) in enumerate(zip(SAMPLE_QUESTIONS, result['answers']), 1):
                print(f"\nQ{i}: {q}")
                print(f"A{i}: {a}")
            
            return True
        else:
            print(f"❌ URL endpoint failed: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ URL endpoint error: {e}")
        return False

def test_file_upload_endpoint(file_path):
    """Test the file upload endpoint"""
    print(f"\n📁 Testing File Upload Processing")
    print("-" * 50)
    print(f"File: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, 'application/pdf')
            }
            data = {
                'questions': json.dumps(SAMPLE_QUESTIONS)
            }
            
            print("📤 Uploading file to /hackrx/upload...")
            response = requests.post(
                f"{BASE_URL}/hackrx/upload",
                headers=headers,
                files=files,
                data=data,
                timeout=300
            )
        
        if response.status_code == 200:
            print("✅ File upload successful!")
            result = response.json()
            
            print(f"\n📋 Results from file upload:")
            print(f"Filename: {result.get('filename', 'N/A')}")
            
            for i, (q, a) in enumerate(zip(SAMPLE_QUESTIONS, result['answers']), 1):
                print(f"\nQ{i}: {q}")
                print(f"A{i}: {a}")
            
            return True
        else:
            print(f"❌ File upload failed: {response.status_code}")
            try:
                error = response.json()
                print(f"Error: {error}")
            except:
                print(f"Error text: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return False

def check_server_health():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server is healthy")
            print(f"   Device: {health_data.get('device', 'unknown')}")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running: python start_server.py")
        return False

def main():
    """Main demonstration function"""
    print("=" * 80)
    print("🚀 HackRX 5.0 - Dual Processing Demo (URL + File Upload)")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Server: {BASE_URL}")
    print(f"Questions: {len(SAMPLE_QUESTIONS)}")
    print()
    
    # Check server health first
    if not check_server_health():
        return
    
    print("\n" + "=" * 80)
    
    # Test URL endpoint
    url_success = test_url_endpoint()
    
    print("\n" + "=" * 80)
    
    # Look for a sample PDF file to test file upload
    test_files = [
        "sample.pdf",
        "test.pdf", 
        "document.pdf",
        "policy.pdf"
    ]
    
    sample_file = None
    for file_path in test_files:
        if os.path.exists(file_path):
            sample_file = file_path
            break
    
    if sample_file:
        file_success = test_file_upload_endpoint(sample_file)
    else:
        print(f"📁 Testing File Upload Processing")
        print("-" * 50)
        print(f"⚠️  No sample PDF files found")
        print(f"   Looking for: {', '.join(test_files)}")
        print(f"   Please place a PDF file in the current directory to test file upload")
        file_success = False
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DEMO SUMMARY")
    print("=" * 80)
    print(f"URL Endpoint:      {'✅ Working' if url_success else '❌ Failed'}")
    print(f"File Upload:       {'✅ Working' if file_success else '⚠️  No test file' if sample_file is None else '❌ Failed'}")
    
    if url_success or file_success:
        print("\n🎉 Demo completed successfully!")
        print("💡 Both endpoints are ready for production use")
    else:
        print("\n⚠️  Some endpoints need attention")
    
    print("\n🔗 Available Endpoints:")
    print(f"   • Health Check:    GET  {BASE_URL}/health")
    print(f"   • URL Processing:  POST {BASE_URL}/hackrx/run")
    print(f"   • File Upload:     POST {BASE_URL}/hackrx/upload")
    print(f"   • Documentation:   GET  {BASE_URL}/docs")
    print("=" * 80)

if __name__ == "__main__":
    main()
