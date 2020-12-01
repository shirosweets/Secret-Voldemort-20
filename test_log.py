import config
config.database = "test_data_base.sqlite"
#config.database = "data_base.sqlite"

from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import pytest

import test_1logIn as logIn

client = TestClient(app)

def test_log():
    response = client.get(
                    "/users/log",
                    headers= { 
                        "Authorization": logIn.getToken_Amber()}
                        ) 
    assert ((response.json()["log_won_games_fenix"] == 1) or (response.json()["log_lost_games_death_eater"] == 1) or (response.json()["log_won_games_death_eater"] == 1) or (response.json()["log_lost_games_fenix"] == 1))