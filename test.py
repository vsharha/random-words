from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def post_request(url, data=None):
    headers = {'Content-Type': 'application/json'}
    response = client.post(url, headers=headers, json=data)
    print(response.json())

def get_request(url):
    response = client.get(url)
    print(response.json())

if __name__ == '__main__':
    get_request("/words?lang=ukr&length=100")
    for i in range(3):
        get_request("/?min_len=5&max_len=5&max_index=1000")
    print()
    for i in range(3):
        get_request("/?min_len=5&max_len=5&max_index=1000&lang=ukr")
    print()
    for i in range(3):
        get_request("/?min_len=5&max_len=5&max_index=1000&lang=rus")