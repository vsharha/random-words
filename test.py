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
    get_request("/")
    get_request("/?lang=ukr")
    get_request("/?lang=rus")