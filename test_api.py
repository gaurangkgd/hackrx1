"""
API testing script for HackRX 5.0 URL endpoint
Tests the document processing API with sample data
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
BEARER_TOKEN = "d23b6db093b3dce5948ae2389ba8db77a4847fa7c2990e66650a4cc6092d0042"

# Test data
TEST_URL = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

QUESTIONS = [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?",
    "Does this policy cover maternity expenses?",
    "What are the age limits for this policy?"
]

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_url_endpoint():
    """Test the URL processing endpoint"""
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "documents": TEST_URL,
        "questions": QUESTIONS
    }
    
    try:
        print("🚀 Testing URL endpoint...")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            json=data,
            headers=headers,
            timeout=300
        )
        
        end_time = time.time()
        print(f"⏱️ Processing time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ URL Processing Successful!")
            print(f"📄 Document: {TEST_URL}")
            print(f"❓ Questions: {len(QUESTIONS)}")
            print(f"💬 Answers: {len(result['answers'])}")
            
            for i, (q, a) in enumerate(zip(QUESTIONS, result['answers']), 1):
                print(f"\nQ{i}: {q}")
                print(f"A{i}: {a}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ URL endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 HackRX 5.0 API Testing")
    print("=" * 50)
    
    # Test health endpoint
    if test_health_endpoint():
        print("\n" + "=" * 50)
        # Test URL endpoint
        test_url_endpoint()
    else:
        print("❌ Server not running. Start with: python start_server.py")
    
    print("\n" + "=" * 50)
    print("🏁 Testing Complete")
