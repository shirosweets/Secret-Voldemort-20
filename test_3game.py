import config
config.database = "test_data_base.sqlite"

from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import test_1logIn as logIn
import test_2lobby as lobby
import db_functions as dbf
import db_entities_relations as dbe
import pytest

client = TestClient(app)

#################################################### Logged in Game Tests ####################################################
#################################################### Logged in Game Tests ####################################################
#################################################### Logged in Game Tests ####################################################


            ########################################       ########################################


# Game 1 has 8 players
#(player_number: md.PlayerNumber, game_id: int, user_id: int = Depends(auth.get_current_active_user)) -> int:

def return_token_minister():
    player_number_actual_minister= dbf.get_actual_minister(1)
    player_id_actual_minister = dbf.get_player_id_by_player_number(player_number_actual_minister, 1)
    user_id_actual_minister = dbf.get_user_id_by_player_id(player_id_actual_minister)

    if(user_id_actual_minister == 1): # Argentina
        return logIn.getToken_Argentina()
    elif(user_id_actual_minister == 2): # Brasil
        return logIn.getToken_Brasil()
    elif(user_id_actual_minister == 3):
        return logIn.getToken_Carol()
    elif(user_id_actual_minister == 4):
        return logIn.getToken_Dexter()
    elif(user_id_actual_minister == 5):
        return logIn.getToken_Esteban_quito()
    elif(user_id_actual_minister == 6):
        return logIn.getToken_FaMAF()
    elif(user_id_actual_minister == 7):
        return logIn.getToken_Ganzua()
    elif(user_id_actual_minister == 8):   
        return logIn.getToken_Hugo()

def return_token_NOT_minister():
    player_number_actual_minister= dbf.get_actual_minister(1)
    player_id_actual_minister = dbf.get_player_id_by_player_number(player_number_actual_minister + 1, 1)
    user_id_actual_minister = dbf.get_user_id_by_player_id(player_id_actual_minister)

    if(user_id_actual_minister == 1): # Argentina
        return logIn.getToken_Argentina()
    elif(user_id_actual_minister == 2): # Brasil
        return logIn.getToken_Brasil()
    elif(user_id_actual_minister == 3):
        return logIn.getToken_Carol()
    elif(user_id_actual_minister == 4):
        return logIn.getToken_Dexter()
    elif(user_id_actual_minister == 5):
        return logIn.getToken_Esteban_quito()
    elif(user_id_actual_minister == 6):
        return logIn.getToken_FaMAF()
    elif(user_id_actual_minister == 7):
        return logIn.getToken_Ganzua()
    elif(user_id_actual_minister == 8):   
        return logIn.getToken_Hugo()
        
def return_token_director():
    player_number_actual_director= dbf.get_actual_director(1)
    player_id_actual_director= dbf.get_player_id_by_player_number(player_number_actual_director, 1)
    user_id_actual_director= dbf.get_user_id_by_player_id(player_id_actual_director)

    if(user_id_actual_director == 1): # Argentina
        return logIn.getToken_Argentina()
    elif(user_id_actual_director == 2): # Brasil
        return logIn.getToken_Brasil()
    elif(user_id_actual_director == 3):
        return logIn.getToken_Carol()
    elif(user_id_actual_director == 4):
        return logIn.getToken_Dexter()
    elif(user_id_actual_director == 5):
        return logIn.getToken_Esteban_quito()
    elif(user_id_actual_director == 6):
        return logIn.getToken_FaMAF()
    elif(user_id_actual_director == 7):
        return logIn.getToken_Ganzua()
    elif(user_id_actual_director == 8):   
        return logIn.getToken_Hugo()

#?##################### START GAME #############################
#?##################### START GAME #############################
#?##################### START GAME #############################

# #! Game 1 Select director myself
def test_select_director_myself():
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": 0
                    }) 
    assert response.status_code == 412

        #! Game 1 Select director Ok
def test_select_director():
    current_game= 1
    director_candidate= 1
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.status_code == 200
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")

        #! Game 1 Vote candidate NO 4
def test_vote_candidate_Argentina():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Argentina has voted"

def test_vote_candidate_Brasil():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Brasil has voted"

def test_vote_candidate_Carol():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Carol has voted"

def test_vote_candidate_Dexter():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Dexter has voted"

        #! Game 1 Vote candidate OK 4
def test_vote_candidate_Esteban_quito():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player FaMAF has voted"

def test_vote_candidate_Ganzua():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ganzua has voted"

def test_vote_candidate_Hugo():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Hugo has voted"

        #? NO APPROVE DIRECTOR !#

#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

#! Try to vote with candidate without candidate
def test_vote_candidate_412():
    token= return_token_NOT_minister()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 412

#! NOT Minister
def test_discard_card_NOT_Minister():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_NOT_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 412

#! Minister try discard card
def test_discard_card_Minister_412():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 412

#! Director try discard card
def test_discard_card_Director_412():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 412

        #? Game 1 Select candidate !#


# REVIEW go for 1 proclamation
def test_select_director_1(): # REVIEW test_select_director_1
    current_game= 1
    director_candidate= 2
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    #assert response.json() == "Algo"
    assert response.status_code == 200

        #! Game 1 Vote candidate OK 8
def test_vote_candidate_Argentina_OK_1():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " Player Argentina has voted"
    assert response.status_code == 200

def test_vote_candidate_Brasil_OK_1():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " Player Brasil has voted"
    assert response.status_code == 200

def test_vote_candidate_Carol_OK_1():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " Player Carol has voted"
    assert response.status_code == 200
    
def test_vote_candidate_Dexter_OK_1():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " Player Dexter has voted"
    assert response.status_code == 200   

def test_vote_candidate_Esteban_quito_OK_1():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF_OK_1():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " Player FaMAF has voted"
    assert response.status_code == 200

def test_vote_candidate_Ganzua_OK_1():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " Player Ganzua has voted"
    assert response.status_code == 200   

def test_vote_candidate_Hugo_OK_1():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    #assert response.json()["voteOut_response"] == " HOLA"
    assert response.json()["voteOut_response"] == " Player Hugo has voted"
    assert response.status_code == 200

        #? APPROVE DIRECTOR !#

#! Game 1 Discard card OK
#! Minister
def test_discard_card_Minister_1():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " Player Hugo has voted"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_1():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_director()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 1 Post proclamation OK
def test_post_proclamation_1():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 1 proclamation
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

#! Game 1 Select Director 2
def test_select_director_2(): # REVIEW test_select_director_2
    current_game= 1
    director_candidate= 3
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    assert response.status_code == 200

        #! Game 1 Vote candidate NO 8
def test_vote_candidate_Argentina_NO_2():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Argentina has voted"

def test_vote_candidate_Brasil_OK_2():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Brasil has voted"

def test_vote_candidate_Carol_NO_2():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Carol has voted"

def test_vote_candidate_Dexter_NO_2():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Dexter has voted"

def test_vote_candidate_Esteban_quito_NO_2():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF_NO_2():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player FaMAF has voted"

def test_vote_candidate_Ganzua_NO_2():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ganzua has voted"

def test_vote_candidate_Hugo_NO_2():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": False
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Hugo has voted"

        #? NO APPROVE DIRECTOR !#

#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 2 proclamations
#! Game 1 Select Director 3
def test_select_director_3(): # REVIEW test_select_director_3
    current_game= 1
    director_candidate= 0
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    #assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 1 Vote candidate OK 8
def test_vote_candidate_Argentina_OK_3():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Argentina has voted"

def test_vote_candidate_Brasil_OK_3():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Brasil has voted"

def test_vote_candidate_Carol_OK_3():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Carol has voted"

def test_vote_candidate_Dexter_OK_3():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Dexter has voted"

def test_vote_candidate_Esteban_quito_OK_3():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF_OK_3():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player FaMAF has voted"

def test_vote_candidate_Ganzua_OK_3():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ganzua has voted"

def test_vote_candidate_Hugo_OK_3():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Hugo has voted"

        #? APPROVE DIRECTOR !#

#! Game 1 Discard card OK
#! Minister
def test_discard_card_Minister_3():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " Player Hugo has voted"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_3():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_director()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 1 Post proclamation OK
def test_post_proclamation_3():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 2 proclamations
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 3 proclamations
#! Game 1 Select Director 4
def test_select_director_4(): # REVIEW test_select_director_4
    current_game= 1
    director_candidate= 2
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    #assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 1 Vote candidate OK 8
def test_vote_candidate_Argentina_OK_4():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Argentina has voted"

def test_vote_candidate_Brasil_OK_4():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Brasil has voted"

def test_vote_candidate_Carol_OK_4():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Carol has voted"

def test_vote_candidate_Dexter_OK_4():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Dexter has voted"

def test_vote_candidate_Esteban_quito_OK_4():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF_OK_4():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player FaMAF has voted"

def test_vote_candidate_Ganzua_OK_4():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ganzua has voted"

def test_vote_candidate_Hugo_OK_4():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Hugo has voted"

        #? APPROVE DIRECTOR !#

#! Game 1 Discard card OK
#! Minister
def test_discard_card_Minister_4():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " Player Hugo has voted"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_4():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_director()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 1 Post proclamation OK
def test_post_proclamation_4():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 3 proclamations
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 4 proclamations
#! Game 1 Select Director 5
def test_select_director_5(): # REVIEW test_select_director_5
    current_game= 1
    director_candidate= 1
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    #assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 1 Vote candidate OK 8
def test_vote_candidate_Argentina_OK_5():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Argentina has voted"

def test_vote_candidate_Brasil_OK_5():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Brasil has voted"

def test_vote_candidate_Carol_OK_5():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Carol has voted"

def test_vote_candidate_Dexter_OK_5():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Dexter has voted"

def test_vote_candidate_Esteban_quito_OK_5():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF_OK_5():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player FaMAF has voted"

def test_vote_candidate_Ganzua_OK_5():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ganzua has voted"

def test_vote_candidate_Hugo_OK_5():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Hugo has voted"

        #? APPROVE DIRECTOR !#

#! Game 1 Discard card OK
#! Minister
def test_discard_card_Minister_5():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " Player Hugo has voted"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_5():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_director()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 1 Post proclamation OK
def test_post_proclamation_5():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 4 proclamations
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 5 proclamations

def return_fenix_proclamations_game_1():
    return dbf.get_total_proclamations_phoenix(1)

def return_death_eater_proclamations_game_1():
    return dbf.get_total_proclamations_death_eater(1)

#! Game 1 Select Director 6
def test_select_director_6(): # REVIEW test_select_director_6
    current_game= 1
    director_candidate= 3
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 1 Vote candidate OK 8
def test_vote_candidate_Argentina_OK_6():
    token= logIn.getToken_Argentina()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Argentina has voted"

def test_vote_candidate_Brasil_OK_6():
    token= logIn.getToken_Brasil()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Brasil has voted"

def test_vote_candidate_Carol_OK_6():
    token= logIn.getToken_Carol()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Carol has voted"

def test_vote_candidate_Dexter_OK_6():
    token= logIn.getToken_Dexter()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Dexter has voted"

def test_vote_candidate_Esteban_quito_OK_6():
    token= logIn.getToken_Esteban_quito()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

def test_vote_candidate_FaMAF_OK_6():
    token= logIn.getToken_FaMAF()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player FaMAF has voted"

def test_vote_candidate_Ganzua_OK_6():
    token= logIn.getToken_Ganzua()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ganzua has voted"

def test_vote_candidate_Hugo_OK_6():
    token= logIn.getToken_Hugo()
    response= client.put(
        "/games/1/select_director/vote",
        headers= {
            "Authorization":  token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Hugo has voted"

        #? APPROVE DIRECTOR !#

#! Tries to select director when you don't on the correct step_turn
def test_try_select_director_412():
            director_candidate= 1
            response= client.post(
                            "/games/1/select_director/",
                            headers= { 
                                "Authorization": return_token_minister()},
                            json= {
                                "playerNumber": director_candidate
                            })
            assert response.json()["detail"] == " Step turn is not START_GAME or POST_PROCLAMATION_ENDED. You are not in the stage of the corresponding turn."
            assert response.status_code == 412


#! Game 1 Discard card OK
#! Minister
def test_discard_card_Minister_6():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " Player Hugo has voted"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_6():
    response= client.put(
        "/games/1/discard_card/",
        headers= {
            "Authorization": return_token_director()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 1 Post proclamation OK
def test_post_proclamation_6():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    if(return_fenix_proclamations_game_1() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations_game_1() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 5 proclamations
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

#! FIXME I can't run this test, but need a conditional test
# REVIEW go for 6 proclamations if is necessary
def try_continue_game():
    if((return_fenix_proclamations_game_1() != 5) and (return_death_eater_proclamations_game_1 != 6)):
        #! Game 1 Select Director 7
        def test_select_director_7(): # REVIEW test_select_director_7
            current_game= 1
            director_candidate= 1
            response= client.post(
                            "/games/1/select_director/",
                            headers= { 
                                "Authorization": return_token_minister()},
                            json= {
                                "playerNumber": director_candidate
                            })
            player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
            player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
            assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
            # assert response.json()["detail"] == " ERROR"
            assert response.status_code == 200

                #! Game 1 Vote candidate OK 8
        def test_vote_candidate_Argentina_OK_7():
            token= logIn.getToken_Argentina()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization": token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Argentina has voted"

        def test_vote_candidate_Brasil_OK_7():
            token= logIn.getToken_Brasil()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization": token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Brasil has voted"

        def test_vote_candidate_Carol_OK_7():
            token= logIn.getToken_Carol()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization":  token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Carol has voted"

        def test_vote_candidate_Dexter_OK_7():
            token= logIn.getToken_Dexter()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization":  token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Dexter has voted"

        def test_vote_candidate_Esteban_quito_OK_7():
            token= logIn.getToken_Esteban_quito()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization":  token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Esteban_quito has voted"

        def test_vote_candidate_FaMAF_OK_7():
            token= logIn.getToken_FaMAF()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization":  token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player FaMAF has voted"

        def test_vote_candidate_Ganzua_OK_7():
            token= logIn.getToken_Ganzua()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization":  token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Ganzua has voted"

        def test_vote_candidate_Hugo_OK_7():
            token= logIn.getToken_Hugo()
            response= client.put(
                "/games/1/select_director/vote",
                headers= {
                    "Authorization":  token
                },
                json= {
                    "vote": True
                }
            )
            assert response.status_code == 200
            assert response.json()["voteOut_response"] == " Player Hugo has voted"

                #? APPROVE DIRECTOR !#

        #! Game 1 Discard card OK
        #! Minister
        def test_discard_card_Minister_7():
            response= client.put(
                "/games/1/discard_card/",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "card_discarted": 1
                }
            )
            # assert response.json()["detail"] == " Player Hugo has voted"
            assert response.status_code == 200

        #! Director
        def test_discard_card_Director_7():
            response= client.put(
                "/games/1/discard_card/",
                headers= {
                    "Authorization": return_token_director()
                },
                json= {
                    "card_discarted": 1
                }
            )
            assert response.status_code == 200
            #board_response=" "

        # def return_first_card_on_deck():
        #     board_deck_decoded= dbf.get_decoded_deck(1)
        #     return dbf.getFirstCardFromDeck(board_deck_decoded)

        #! Game 1 Post proclamation OK
        def test_post_proclamation_7():
            response= client.put(
                "/games/1/proclamation/",
                headers= {
                    "Authorization": return_token_director()
                },
                # json= {
                #     "proclamationCard_phoenix": return_first_card_on_deck()
                # }
            )
            if(return_fenix_proclamations_game_1() >= 5):
                assert response.status_code == 307
                assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
            elif(return_death_eater_proclamations_game_1() >= 6):
                assert response.status_code == 307
                assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
            else:
                assert response.status_code == 200
                assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

#REVIEW GAME 2

def return_fenix_proclamations_game_2():
    return dbf.get_total_proclamations_phoenix(2)

def return_death_eater_proclamations_game_2():
    return dbf.get_total_proclamations_death_eater(2)

def return_token_minister_game_2():
    player_number_actual_minister= dbf.get_actual_minister(2)
    player_id_actual_minister = dbf.get_player_id_by_player_number(player_number_actual_minister, 2)
    user_id_actual_minister = dbf.get_user_id_by_player_id(player_id_actual_minister)

    if(user_id_actual_minister == 11): # Amber
        return logIn.getToken_Amber()
    elif(user_id_actual_minister == 12): # Benny
        return logIn.getToken_Benny()
    elif(user_id_actual_minister == 13): # Candy
        return logIn.getToken_Candy()
    elif(user_id_actual_minister == 14): # Denis
        return logIn.getToken_Denis()
    elif(user_id_actual_minister == 15): # Ember
        return logIn.getToken_Ember()
        
def return_token_director_game_2():
    player_number_actual_director= dbf.get_actual_director(2)
    player_id_actual_director= dbf.get_player_id_by_player_number(player_number_actual_director, 2)
    user_id_actual_director= dbf.get_user_id_by_player_id(player_id_actual_director)

    if(user_id_actual_director == 11): # Amber
        return logIn.getToken_Amber()
    elif(user_id_actual_director == 12): # Benny
        return logIn.getToken_Benny()
    elif(user_id_actual_director == 13): # Candy
        return logIn.getToken_Candy()
    elif(user_id_actual_director == 14): # Denis
        return logIn.getToken_Denis()
    elif(user_id_actual_director == 15): # Ember
        return logIn.getToken_Ember()

#! Game 2 Select Director 1
# REVIEW go for 1 proclamation
def test_select_director_game_2_1(): # REVIEW test_select_director_game_2_1
    current_game= 2
    director_candidate= 1
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister_game_2()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 2 Vote candidate OK 5
def test_vote_candidate_Amber_game_2_OK_1():
    token= logIn.getToken_Amber()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Amber has voted"

def test_vote_candidate_Benny_game_2_OK_1():
    token= logIn.getToken_Benny()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Benny has voted"

def test_vote_candidate_Candy_game_2_OK_1():
    token= logIn.getToken_Candy()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Candy has voted"

def test_vote_candidate_Denis_game_2_OK_1():
    token= logIn.getToken_Denis()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Denis has voted"

def test_vote_candidate_Ember_game_2_OK_1():
    token= logIn.getToken_Ember()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ember has voted"

        #? APPROVE DIRECTOR !#

#! Game 2 Discard card OK 1
#! Minister
def test_discard_card_Minister_game_2_1():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_minister_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_game_2_1():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 2 Post proclamation OK
def test_post_proclamation_game_2_1():
    response= client.put(
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    if(return_fenix_proclamations_game_2() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations_game_2() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 1 proclamation G2
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 2 proclamations
def test_select_director_game_2_2(): # REVIEW test_select_director_game_2_2
    current_game= 2
    director_candidate= 4
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister_game_2()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 2 Vote candidate OK 5
def test_vote_candidate_Amber_game_2_OK_2():
    token= logIn.getToken_Amber()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Amber has voted"

def test_vote_candidate_Benny_game_2_OK_2():
    token= logIn.getToken_Benny()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Benny has voted"

def test_vote_candidate_Candy_game_2_OK_2():
    token= logIn.getToken_Candy()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Candy has voted"

def test_vote_candidate_Denis_game_2_OK_2():
    token= logIn.getToken_Denis()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Denis has voted"

def test_vote_candidate_Ember_game_2_OK_2():
    token= logIn.getToken_Ember()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ember has voted"

        #? APPROVE DIRECTOR !#

#! Game 2 Discard card OK 2
#! Minister
def test_discard_card_Minister_game_2_2():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_minister_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_game_2_2():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 2 Post proclamation OK
def test_post_proclamation_game_2_2():
    response= client.put(
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    if(return_fenix_proclamations_game_2() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations_game_2() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 2 proclamations G2
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 3 proclamations
def test_select_director_game_2_3(): # REVIEW test_select_director_game_2_3
    current_game= 2
    director_candidate= 3
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister_game_2()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 2 Vote candidate OK 5
def test_vote_candidate_Amber_game_2_OK_3():
    token= logIn.getToken_Amber()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Amber has voted"

def test_vote_candidate_Benny_game_2_OK_3():
    token= logIn.getToken_Benny()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Benny has voted"

def test_vote_candidate_Candy_game_2_OK_3():
    token= logIn.getToken_Candy()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Candy has voted"

def test_vote_candidate_Denis_game_2_OK_3():
    token= logIn.getToken_Denis()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Denis has voted"

def test_vote_candidate_Ember_game_2_OK_3():
    token= logIn.getToken_Ember()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ember has voted"

        #? APPROVE DIRECTOR !#

#! Game 2 Discard card OK 2
#! Minister
def test_discard_card_Minister_game_2_3():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_minister_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_game_2_3():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 2 Post proclamation OK
def test_post_proclamation_game_2_3():
    response= client.put(
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    if(return_fenix_proclamations_game_2() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations_game_2() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 3 proclamations G2

#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 4 proclamations
def test_select_director_game_2_4(): # REVIEW test_select_director_game_2_4
    current_game= 2
    director_candidate= 0
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister_game_2()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 2 Vote candidate OK 5
def test_vote_candidate_Amber_game_2_OK_4():
    token= logIn.getToken_Amber()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Amber has voted"

def test_vote_candidate_Benny_game_2_OK_4():
    token= logIn.getToken_Benny()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Benny has voted"

def test_vote_candidate_Candy_game_2_OK_4():
    token= logIn.getToken_Candy()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Candy has voted"

def test_vote_candidate_Denis_game_2_OK_4():
    token= logIn.getToken_Denis()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Denis has voted"

def test_vote_candidate_Ember_game_2_OK_4():
    token= logIn.getToken_Ember()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ember has voted"

        #? APPROVE DIRECTOR !#

#! Game 2 Discard card OK 4
#! Minister
def test_discard_card_Minister_game_2_4():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_minister_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_game_2_4():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 2 Post proclamation OK
def test_post_proclamation_game_2_4():
    response= client.put(
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    if(return_fenix_proclamations_game_2() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations_game_2() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 4 proclamations G2
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################
#?##################### NEW TURN #############################

# REVIEW go for 5 proclamations
def test_select_director_game_2_5(): # REVIEW test_select_director_game_2_5
    current_game= 2
    director_candidate= 1
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister_game_2()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

        #! Game 2 Vote candidate OK 5
def test_vote_candidate_Amber_game_2_OK_5():
    token= logIn.getToken_Amber()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Amber has voted"

def test_vote_candidate_Benny_game_2_OK_5():
    token= logIn.getToken_Benny()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Benny has voted"

def test_vote_candidate_Candy_game_2_OK_5():
    token= logIn.getToken_Candy()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Candy has voted"

def test_vote_candidate_Denis_game_2_OK_5():
    token= logIn.getToken_Denis()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Denis has voted"

def test_vote_candidate_Ember_game_2_OK_5():
    token= logIn.getToken_Ember()
    response= client.put(
        "/games/2/select_director/vote",
        headers= {
            "Authorization": token
        },
        json= {
            "vote": True
        }
    )
    assert response.status_code == 200
    assert response.json()["voteOut_response"] == " Player Ember has voted"

        #? APPROVE DIRECTOR !#

#! Game 2 Discard card OK 2
#! Minister
def test_discard_card_Minister_game_2_5():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_minister_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    # assert response.json()["detail"] == " ERROR"
    assert response.status_code == 200

#! Director
def test_discard_card_Director_game_2_5():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200
    #board_response=" "

# def return_first_card_on_deck():
#     board_deck_decoded= dbf.get_decoded_deck(1)
#     return dbf.getFirstCardFromDeck(board_deck_decoded)

#! Game 2 Post proclamation OK
def test_post_proclamation_game_2_5():
    response= client.put(
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director_game_2()
        },
        # json= {
        #     "proclamationCard_phoenix": return_first_card_on_deck()
        # }
    )
    if(return_fenix_proclamations_game_2() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations_game_2() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

# REVIEW 5 proclamations G2
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

#TODO Add your GAME 3 here

#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

#TODO Add your GAME 4 here

#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

#TODO Mostrar detalle error: assert response.json()["detail"] == " ERROR"