import unittest
import db_functions as dbf
import helpers_functions as hf
from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import pytest

# run with $ python3 unittest_deck.py

client = TestClient(app)

def getTokenUser(n):
    response = client.post("/login/", data={"username":f"user{n}@mail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


def registerUser(n):
    response = client.post(
                    "/users/",
                    json = { 
                    "userIn_email": f"user{n}@mail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": f"user{n}"
                    }
                    )
    return response

def main_non_test():
    tokens = {}
    for user_n in range(1,11):
        registerUser(user_n)
        tokens[user_n] = getTokenUser(user_n)
    
    for number_players in range(5,11):
        client.post("/lobby/",
                    headers = { "Authorization": tokens[1] },
                    json = { 
                    "lobbyIn_name": f"lobby{number_players}", 
                    "lobbyIn_max_players": number_players, 
                    "lobbyIn_min_players": number_players
                    }
                    )
        for user in range(1,number_players+1):
            client.post(
                f"/lobby/{number_players-4}/",
                headers = { 
                    "Authorization": tokens[user]},
                json = {}
                )
        
        client.delete(
                f"/lobby/{number_players-4}/start_game",
                headers = { 
                    "Authorization": tokens[1]},
                json = {})
    
    for number_players in range(5,11):
        response = client.post("/lobby/",
                    headers = { "Authorization": tokens[1] },
                    json = { 
                    "lobbyIn_name": f"tostart_{number_players}", 
                    "lobbyIn_max_players": number_players, 
                    "lobbyIn_min_players": number_players
                    }
                    )
        lobby_id = response.json()["lobbyOut_Id"]
        for user in range(1,number_players+1):
            client.post(
                f"/lobby/{lobby_id}/",
                headers = { 
                    "Authorization": tokens[user]},
                json = {}
                )
    print("Done")


main_non_test()