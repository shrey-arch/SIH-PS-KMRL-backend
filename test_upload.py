import requests

# Test file upload
url = "http://127.0.0.1:8000/upload_doc/"
files = {'file': open('test.txt', 'rb')}
params = {'uploader': 'test_engineer'}

try:
    response = requests.post(url, files=files, params=params)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)