import requests
import json

def test_file_upload():
    url = 'http://localhost:8000/hackrx/upload'
    headers = {'Authorization': 'Bearer d23b6db093b3dce5948ae2389ba8db77a4847fa7c2990e66650a4cc6092d0042'}
    questions = ['What is the grace period for premium payment?', 'What is the waiting period for pre-existing conditions?']

    with open('test_document.txt', 'rb') as f:
        files = {'file': ('test_document.txt', f, 'text/plain')}
        data = {'questions': json.dumps(questions)}
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            print(f'Status Code: {response.status_code}')
            if response.status_code == 200:
                result = response.json()
                print('✅ Success!')
                print(f'Filename: {result.get("filename", "N/A")}')
                for i, answer in enumerate(result.get("answers", []), 1):
                    print(f'Answer {i}: {answer}')
            else:
                print(f'❌ Error: {response.text}')
        except Exception as e:
            print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_file_upload()
