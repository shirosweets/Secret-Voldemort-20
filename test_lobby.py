from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import pytest

client = TestClient(app)


#################################################### LogIn ####################################################
#################################################### LogIn ####################################################
#################################################### LogIn ####################################################


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


def test_register_Brasil():
    response = client.post(
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


def test_register_Carol():
    response = client.post(
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


def test_register_Dexter():
    response = client.post(
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


def test_register_Esteban_quito():
    response = client.post(
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


def test_register_FaMAF():
    response = client.post(
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


def test_register_Ganzua():
    response = client.post(
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


def test_register_Hugo():
    response = client.post(
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


def test_register_Iatoy():
    response = client.post(
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


def test_register_Joker():
    response = client.post(
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


#################################################### Logged in Lobby Tests ####################################################
#################################################### Logged in Lobby Tests ####################################################
#################################################### Logged in Lobby Tests ####################################################


            ########################################    Create New Lobby   ########################################

# Test with all arguments
def test_create_new_lobby():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "lobby_All_arguments", 
                    "lobbyIn_max_players": 9, 
                    "lobbyIn_min_players": 5
                    }
                    )
    assert response.status_code == 201
    assert response.json()["lobbyOut_result"] == " Your new lobby has been succesfully created!"


# Test without min players
def test_create_new_lobby_WO_min_players():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "lobby_WO_min_players", 
                    "lobbyIn_max_players": 10
                    }
                    )
    assert response.status_code == 201
    assert response.json()["lobbyOut_result"] == " Your new lobby has been succesfully created!"


# Test without Max players
def test_create_new_lobby_WO_Max_players():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "lobby_WO_Max_players", 
                    "lobbyIn_min_players": 5
                    }
                    )
    assert response.status_code == 201
    assert response.json()["lobbyOut_result"] == " Your new lobby has been succesfully created!"


# Test without optional Arguments
def test_create_new_lobby_WO_Optionals():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "lobby_WO_Optionals"
                    }
                    )
    assert response.status_code == 201
    assert response.json()["lobbyOut_result"] == " Your new lobby has been succesfully created!"


# Test bad arguments
def test_create_new_lobby_BA():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "lobby_BA", 
                    "lobbyIn_max_players": 5,
                    "lobbyIn_min_players": 10
                    }
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The amount of players should be a number between 5 and 10"


# Test short name
def test_create_new_lobby_Short_name():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "l", 
                    "lobbyIn_max_players": 5,
                    "lobbyIn_min_players": 10
                    }
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The Lobby name you chose, is out of range (Should be between 4 and 20 characters)"


# Test long name
def test_create_new_lobby_Long_name():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": " AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA TOY RE LARGO", 
                    "lobbyIn_max_players": 5,
                    "lobbyIn_min_players": 10
                    }
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The Lobby name you chose, is out of range (Should be between 4 and 20 characters)"


# Test repeated name
def test_create_new_lobby_RN():
    token = getToken_Argentina()
    response = client.post(
                    "/lobby/",
                    headers = { "Authorization": token },
                    json = { 
                    "lobbyIn_name": "lobby_All_arguments", 
                    "lobbyIn_max_players": 5,
                    "lobbyIn_min_players": 10
                    }
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The Lobby name you chose, is already taken"






            ########################################    List Lobbies   ########################################


# List lobbies All parameters
def test_list_lobbies():
    token = getToken_Argentina()
    response = client.get(
                    "/lobby/list_lobbies/?start_from=0&end_at=10",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 200


# List lobbies no parameters
def test_list_lobbies_NP():
    token = getToken_Argentina()
    response = client.get(
                    "/lobby/list_lobbies/",
                    headers = { "Authorization": token }
                    )
    assert response.status_code == 200


# List lobbies start parameter
def test_list_lobbies_SP():
    token = getToken_Argentina()
    response = client.get(
                    "/lobby/list_lobbies/?start_from=1",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 200

# List lobbies end parameters
def test_list_lobbies_EP():
    token = getToken_Argentina()
    response = client.get(
                    "/lobby/list_lobbies/?end_at=10",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 200


# List lobbies BAD parameters
def test_list_lobbies_BP():
    token = getToken_Argentina()
    response = client.get(
                    "/lobby/list_lobbies/?start_from=10&end_at=1",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 400
    assert response.json()["detail"] == "start_from value must be bigger than end_at value"



            ########################################    Join Lobby    ########################################


# Test join Lobby OK
def test_join_lobby():
    token = getToken_Brasil()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join Already in lobby
def test_join_lobby_AIL():
    token = getToken_Brasil()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join Lobby Doesnt exist
def test_join_lobby_DNE():
    token = getToken_Brasil()
    response = client.post(
                    "/lobby/0/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The lobby you selected does not exist"



# Test join 3
def test_join_lobby_3():
    token = getToken_Carol()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join 4
def test_join_lobby_4():
    token = getToken_Dexter()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join 5
def test_join_lobby_5():
    token = getToken_Esteban_quito()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join 6
def test_join_lobby_6():
    token = getToken_FaMAF()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join 7
def test_join_lobby_7():
    token = getToken_Ganzua()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join 8
def test_join_lobby_8():
    token = getToken_Hugo()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test join 9
def test_join_lobby_9():
    token = getToken_Iatoy()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_All_arguments"


# Test Lobby already full
def test_join_lobby_FULL():
    token = getToken_Joker()
    response = client.post(
                    "/lobby/1/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The lobby you selected is already full"


            ########################################    Change Nick    ########################################


# Test Change Nick, ok 1 
def test_change_nick_1():
    token = getToken_Iatoy()
    new_nick = "1xxx"
    puntos = 9
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 2
def test_change_nick_2():
    token = getToken_Iatoy()
    new_nick = "2xxx"
    puntos = 8
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 3
def test_change_nick_3():
    token = getToken_Iatoy()
    new_nick = "3xxx"
    puntos = 7
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 4
def test_change_nick_4():
    token = getToken_Iatoy()
    new_nick = "4xxx"
    puntos = 6
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 5
def test_change_nick_5():
    token = getToken_Iatoy()
    new_nick = "5xxx"
    puntos = 5
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 6
def test_change_nick_6():
    token = getToken_Iatoy()
    new_nick = "6xxx"
    puntos = 4
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 7
def test_change_nick_7():
    token = getToken_Iatoy()
    new_nick = "7xxx"
    puntos = 3
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 8
def test_change_nick_8():
    token = getToken_Iatoy()
    new_nick = "8xxx"
    puntos = 2
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")

# Test Change Nick, ok 9
def test_change_nick_9():
    token = getToken_Iatoy()
    new_nick = "9xxx"
    puntos = 1
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, ok 10
def test_change_nick_10():
    token = getToken_Iatoy()
    new_nick = "10xx"
    puntos = 0
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == (f" Your nick has been sucessfully changed to {new_nick}, you can change it {puntos} more times")


# Test Change Nick, player doesnt have enough points
def test_change_nick_points():
    token = getToken_Iatoy()
    new_nick = "9xxx"
    puntos = 1
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 412
    assert response.json()["detail"] == " You changed your nick too many times >:C"
    

# Test Change Nick, nick should have at least 4 char 
def test_change_nick_min():
    token = getToken_Iatoy()
    new_nick = "1"
    puntos = 9
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 412
    assert response.json()["detail"] == " Your Nick must have between 4 and 20 characters"


# Test Change Nick, nick exeeds max characters
def test_change_nick_Max():
    token = getToken_Iatoy()
    new_nick = "1xxxxxxxxxxxxxxxxxxxxxx"
    puntos = 9
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 412
    assert response.json()["detail"] == " Your Nick must have between 4 and 20 characters"


# Test Change Nick, Lobby does not exist
def test_change_nick_lobby_DE():
    token = getToken_Iatoy()
    new_nick = "1xxx"
    puntos = 9
    response = client.post(
                    "/lobby/0/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 412
    assert response.json()["detail"] == " The lobby you selected does not exist"


# Test Change Nick, user not in lobby
def test_change_nick_lobby_NIL():
    token = getToken_Iatoy()
    new_nick = "1xxx"
    puntos = 9
    response = client.post(
                    "/lobby/2/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 412
    assert response.json()["detail"] == " You are not in the lobby you selected (2)"


# Test Change Nick, Nick already taken
def test_change_nick_lobby_NAT():
    token = getToken_Argentina()
    new_nick = "10xx"
    puntos = 9
    response = client.post(
                    "/lobby/1/change_nick",
                    headers = { 
                        "Authorization": token},
                    json = {"nick": new_nick}
                    )
    assert response.status_code == 412
    assert response.json()["detail"] == " The nick you selected is already taken"



            ########################################    Leave Lobby    ########################################


# Leave Lobby OK
def test_leave_lobby():
    token = getToken_Iatoy()
    response = client.delete(
                    "/lobby/1",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == " You left lobby 1"


# Leave Lobby Does not exist
def test_leave_lobby_DNE():
    token = getToken_Iatoy()
    response = client.delete(
                    "/lobby/0",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 409
    assert response.json()["detail"] == " The lobby you selected does not exist"


# Leave Lobby User not in lobby
def test_leave_lobby_UNL():
    token = getToken_Iatoy()
    response = client.delete(
                    "/lobby/2",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 409
    assert response.json()["detail"] ==" You are not in the provided lobby"


# Join lobby 2
def test_join_leave_lobby():
    token = getToken_Brasil()
    response = client.post(
                    "/lobby/2/",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["joinLobby_name"] == "lobby_WO_min_players"


# Leave Lobby Creator
def test_leave_lobby_creator():
    token = getToken_Argentina()
    response = client.delete(
                    "/lobby/2",
                    headers = { 
                        "Authorization": token},
                    json = {}
                    )
    assert response.status_code == 202
    assert response.json()["responseText"] == " You closed lobby 2"



            ########################################    Start Game    ########################################

# Test start game lobby exist
def test_start_game_LNE():
    token = getToken_Argentina()
    response = client.delete(
                    "/lobby/0/start_game",
                    headers = { 
                        "Authorization": token},
                    json = {
                        
                    })
    assert response.status_code == 409
    assert response.json()["detail"] == " The lobby you selected does not exist"


# Test start game User In Lobby
def test_start_game_UIN():
    token = getToken_Brasil()
    response = client.delete(
                    "/lobby/3/start_game",
                    headers = { 
                        "Authorization": token},
                    json = {
                        
                    })
    assert response.status_code == 409
    assert response.json()["detail"] == " You are not in the provided lobby"


# Test start game min - max players
def test_start_game_MmP():
    token = getToken_Argentina()
    response = client.delete(
                    "/lobby/3/start_game",
                    headers = { 
                        "Authorization": token},
                    json = {
                        
                    })
    assert response.status_code == 412
    assert response.json()["detail"] == " List of players should be between 5 and 10"


# Test start game user is Owner
def test_start_game_UIO():
    token = getToken_Brasil()
    response = client.delete(
                    "/lobby/1/start_game",
                    headers = { 
                        "Authorization": token},
                    json = {
                        
                    })
    assert response.status_code == 401
    assert response.json()["detail"] == " User is not owner of the lobby"


# Test start game
def test_start_game():
    token = getToken_Argentina()
    response = client.delete(
                    "/lobby/1/start_game",
                    headers = { 
                        "Authorization": token},
                    json = {
                        
                    })
    assert response.status_code == 200
    assert response.json()["responseText"] == " Your game has been started"