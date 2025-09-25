from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def post_request(url, data=None):
    headers = {'Content-Type': 'application/json'}
    response = client.post(url, headers=headers, json=data)
    print(response.json())

def get_request(url):
    response = client.get(url)
    print(response.json())

if __name__ == '__main__':
    post_request('/items', {"text":"apple"})
    get_request('/items/0')
    get_request('/items/1')
    get_request('/items/2')
    get_request('/items')
    get_request('/items?limit=2')