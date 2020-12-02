import requests
import json

baseURL = "http://localhost:8000"

def responseToJson(resp):
    return json.dumps(json.loads(resp.text), indent=1)

def post(headers, body, endpoint):
    return requests.post(baseURL+endpoint, data=body, headers=headers)

def get(headers, endpoint):
    return requests.get(baseURL+endpoint)

def test_01():
    # headers = {}
    # endpoint = ''
    # response = get(headers, endpoint)
    # print(responseToJson(response))

    headers = {'X-API-TOKEN': ''}
    body = {
    "userIn_email": "user@example.com",
    "userIn_name": "AUser",
    "userIn_password": "someLongPassword",
    "userIn_photo": "string"
    }
    endpoint = ''
    response = post(headers, body, endpoint)
    print(responseToJson(response))

test_01()
