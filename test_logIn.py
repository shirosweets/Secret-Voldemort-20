from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import pytest

client = TestClient(app)

#################################################### Not Logged in Lobby Tests ####################################################
#################################################### Not Logged in Lobby Tests ####################################################
#################################################### Not Logged in Lobby Tests ####################################################

def test_NLI_create_new_lobby():
    response = client.post("/lobby/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_NLI_list_lobbies():
    response = client.get("/lobby/list_lobbies/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
def test_NLI_join_lobby():
    response = client.post("/lobby/{lobby_id}/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_NLI_change_nick():
    response = client.post("/lobby/{lobby_id}/change_nick")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_NLI_leave_lobby():
    response = client.delete("/lobby/{lobby_id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_NLI_start_game():
    response = client.delete("/lobby/{lobby_id}/start_game")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
