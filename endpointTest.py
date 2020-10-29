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

    # HAGA LOGIN

    # HAGA NO C QUE 


test_01()

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
# eyJpYXQiOjE2MDM5MjI1NjIsIm5iZiI6MTYwMzkyMjU2MiwianRpIjoiNjJjOWFiNTMtMTUzMC00ZmQ0LThjZmUtODZhOGRlYzllOTBlIiwiZXhwIjoxNjAzOTIzN
# DYyLCJpZGVudGl0eSI6MSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.
# AprJq9wO8Yr8J4fAJx-Ja9wXaLpUI6-lZm5zi6Pf1E8