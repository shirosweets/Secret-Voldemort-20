import config
config.database = "test_data_base.sqlite"
#config.database = "data_base.sqlite"

from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import pytest
client = TestClient(app)

#################################################### Not Logged in Tests ####################################################
#################################################### Not Logged in Tests ####################################################
#################################################### Not Logged in Tests ####################################################


                #################################### NLI Lobby ####################################
                
# def test_NLI_create_new_lobby():
#     response = client.post("/lobby/")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}

# def test_NLI_list_lobbies():
#     response = client.get("/lobby/list_lobbies/")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}
    
# def test_NLI_join_lobby():
#     response = client.post("/lobby/{lobby_id}/")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}

# def test_NLI_change_nick():
#     response = client.post("/lobby/{lobby_id}/change_nick")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}

# def test_NLI_leave_lobby():
#     response = client.delete("/lobby/{lobby_id}")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}

# def test_NLI_start_game():
#     response = client.delete("/lobby/{lobby_id}/start_game")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}


                #################################### NLI Game ####################################

#################################################### Register / LogIn ####################################################
#################################################### Register / LogIn ####################################################
#################################################### Register / LogIn ####################################################

#! USER 1 Argentina
def test_register_Argentina():
    response = client.post(
            "/users/",
             json = { 
                    "userIn_email": "A@a.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Argentina"
                    }
            )
    assert response.status_code == 201
    assert response.json() == {"userOut_username":"Argentina",
                            "userOut_email": "A@a.com",
                            "userOut_operation_result": " Succesfully created!"}


def getToken_Argentina():
    response = client.post("/login/", data={"username":"A@a.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 2 Brasil
def test_register_Brasil():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "B@b.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Brasil"
                    }
            )


def getToken_Brasil():
    response = client.post("/login/", data={"username":"B@b.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 3 Carol
def test_register_Carol():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "C@c.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Carol"
                    }
            )
            
def getToken_Carol():
    response = client.post("/login/", data={"username":"C@c.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 4 Dexter
def test_register_Dexter():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "D@d.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Dexter"
                    }
            )

def getToken_Dexter():
    response = client.post("/login/", data={"username":"D@d.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 5 Esteban_quito
def test_register_Esteban_quito():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "E@e.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Esteban_quito"
                    }
            )


def getToken_Esteban_quito():
    response = client.post("/login/", data={"username":"E@e.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 6 FaMAF
def test_register_FaMAF():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "F@f.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "FaMAF"
                    }
            )


def getToken_FaMAF():
    response = client.post("/login/", data={"username":"F@f.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 7 Ganzua
def test_register_Ganzua():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "G@g.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Ganzua"
                    }
            )


def getToken_Ganzua():
    response = client.post("/login/", data={"username":"G@g.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 8 Hugo
def test_register_Hugo():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "H@h.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Hugo"
                    }
            )


def getToken_Hugo():
    response = client.post("/login/", data={"username":"H@h.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 9 Iatoy
def test_register_Iatoy():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "I@i.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Iatoy"
                    }
            )


def getToken_Iatoy():
    response = client.post("/login/", data={"username":"I@i.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 10 Joker
def test_register_Joker():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "J@j.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Joker"
                    }
            )


def getToken_Joker():
    response = client.post("/login/", data={"username":"J@j.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token

#? GAME 2 #
#! USER 11 Amber
def test_register_Amber():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "amber@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Amber"
                    }
            )


def getToken_Amber():
    response = client.post("/login/", data={"username":"amber@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 12 Benny
def test_register_Benny():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "benny@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Benny"
                    }
            )


def getToken_Benny():
    response = client.post("/login/", data={"username":"benny@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 13 Candy
def test_register_Candy():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "candy@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Candy"
                    }
            )


def getToken_Candy():
    response = client.post("/login/", data={"username":"candy@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 14 Denis
def test_register_Denis():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "denis@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Denis"
                    }
            )


def getToken_Denis():
    response = client.post("/login/", data={"username":"denis@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


#! USER 15 Ember
def test_register_Ember():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "ember@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": "Ember"
                    }
            )


def getToken_Ember():
    response = client.post("/login/", data={"username":"ember@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token


# #! USER 16 Fiora
# def test_register_Fiora():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "fiora@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Fiora"
#                     }
#             )


# def getToken_Fiora():
#     response = client.post("/login/", data={"username":"fiora@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 17 Gian
# def test_register_Gian():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "gian@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Gian"
#                     }
#             )


# def getToken_Gian():
#     response = client.post("/login/", data={"username":"gian@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 18 Hyal
# def test_register_Hyal():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "hyal@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Hyal"
#                     }
#             )

# def getToken_Hyal():
#     response = client.post("/login/", data={"username":"hyal@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 19 Innes
# def test_register_Innes():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "innes@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Innes"
#                     }
#             )

# def getToken_Innes():
#     response = client.post("/login/", data={"username":"innes@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 20 Jeep
# def test_register_Jeep():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "jeep@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Jeep"
#                     }
#             )

# def getToken_Jeep():
#     response = client.post("/login/", data={"username":"jeep@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 21 Kahu
# def test_register_Kahu():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "kahu@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Kahu"
#                     }
#             )

# def getToken_Kahu():
#     response = client.post("/login/", data={"username":"kahu@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 22 Lyan
# def test_register_Lyan():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "lyan@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Lyan"
#                     }
#             )

# def getToken_Lyan():
#     response = client.post("/login/", data={"username":"lyan@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 23 Moon
# def test_register_Moon():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "moon@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Moon"
#                     }
#             )

# def getToken_Moon():
#     response = client.post("/login/", data={"username":"moon@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 24 Nyuku
# def test_register_Nyuku():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "nyuku@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Nyuku"
#                     }
#             )

# def getToken_Nyuku():
#     response = client.post("/login/", data={"username":"nyuku@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 25 Oveja_Oscar
# def test_register_Oveja_Oscar():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "oveja_oscar@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Oveja_Oscar"
#                     }
#             )

# def getToken_Oveja_Oscar():
#     response = client.post("/login/", data={"username":"oveja_oscar@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 26 Piumpium
# def test_register_Piumpium():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "piumpium@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Piumpium"
#                     }
#             )

# def getToken_Piumpium():
#     response = client.post("/login/", data={"username":"piumpium@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token


# #! USER 27 Qhuy
# def test_register_Qhuy():
#     client.post(
#             "/users/",
#              json = { 
#                     "userIn_email": "qhuy@gmail.com", 
#                     "userIn_password": "12345678", 
#                     "userIn_username": "Qhuy"
#                     }
#             )

# def getToken_Qhuy():
#     response = client.post("/login/", data={"username":"qhuy@gmail.com", "password":"12345678" })
#     token = "Bearer " + response.json()["access_token"]
#     return token
"""
#! USER 28
def test_register_():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": ""
                    }
            )
def getToken_():
    response = client.post("/login/", data={"username":"@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token
#! USER 29
def test_register_():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": ""
                    }
            )
def getToken_():
    response = client.post("/login/", data={"username":"@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token
#! USER 30
def test_register_():
    client.post(
            "/users/",
             json = { 
                    "userIn_email": "@gmail.com", 
                    "userIn_password": "12345678", 
                    "userIn_username": ""
                    }
            )
def getToken_():
    response = client.post("/login/", data={"username":"@gmail.com", "password":"12345678" })
    token = "Bearer " + response.json()["access_token"]
    return token
"""