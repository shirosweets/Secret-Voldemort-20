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


             ######################################## GAME 1: 8 Players ########################################

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

def return_id_minister():
    player_number_actual_minister= dbf.get_actual_minister(1)
    player_id_actual_minister = dbf.get_player_id_by_player_number(player_number_actual_minister, 1)
    user_id_actual_minister = dbf.get_user_id_by_player_id(player_id_actual_minister)
    return user_id_actual_minister

def candidate_director(minister_number: int, game: int):
    player = 0
    player_id = dbf.get_player_id_by_player_number(player, game)
    while ((dbf.can_player_be_director(player, game)) or (not dbf.is_player_alive(player_id)) or (minister_number == player)):
        player = player +1
        player_id = dbf.get_player_id_by_player_number(player, game)
    return player

def not_dead_or_myself(myself: int, game: int):
    player = 0
    player_id = dbf.get_player_id_by_player_number(player, game)
    while ((not dbf.is_player_alive(player_id)) or (player == myself)):
        player = player +1
        player_id = dbf.get_player_id_by_player_number(player, game)
    return player

def return_fenix_proclamations_game_1():
    return dbf.get_total_proclamations_phoenix(1)

def return_death_eater_proclamations_game_1():
    return dbf.get_total_proclamations_death_eater(1)


#?############################# START GAME 1 #############################¿#
#?############################# START GAME 1 #############################¿#
#?############################# START GAME 1 #############################¿#

    ################### Last Minister = -1, Director = -1 ###################
     ######################## Actual Minister = 0 ########################
#*############################# START TURN 1 #############################*#

        #! START Exeptions !#
def test_select_director_myself():
    response= client.post(
                    "/games/1/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": 0
                    }) 
    assert response.status_code == 412
        #! END Exeptions !#


        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director():
    current_game= 1
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number,current_game)
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

            #*DIRECTOR NOT APROVED*#
            #*DIRECTOR NOT APROVED*#
            #*DIRECTOR NOT APROVED*#

#?############################# END TURN 1 #############################?#
#?############################# END TURN 1 #############################?#
#?############################# END TURN 1 #############################?#

    ################### Last Minister = -1, Director = -1 ###################
     ######################## Actual Minister = 1 ########################
#?############################# START TURN 2 #############################?#
#?############################# START TURN 2 #############################?#
#?############################# START TURN 2 #############################?#

        #! START Exeptions !#
        #! START Exeptions !#
        #! START Exeptions !#

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

        #! END Exeptions !#
        #! END Exeptions !#
        #! END Exeptions !#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_1():
    current_game= 1
    minister_number = dbf.get_actual_minister(1)
    director_candidate= candidate_director(minister_number,1)
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
    assert response.json()["voteOut_response"] == " Player Hugo has voted"
    assert response.status_code == 200

            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD*#
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
    assert response.status_code == 200

            #* DIRECTOR DISCARD CARD*#
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
    
            #* POST PROCLAMATION *#
def test_post_proclamation_1():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"



#?############################# END TURN 2 #############################?#
#?############################# END TURN 2 #############################?#
#?############################# END TURN 2 #############################?#
                        #? TOTAL: 1 PROCLAMATION POSTED ¿#

            ################## Last Minister = 1 ##################
     ######################## Actual Minister = 2 ########################
#?############################# START TURN 3 #############################?#
#?############################# START TURN 3 #############################?#
#?############################# START TURN 3 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_2(): 
    current_game= 1
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number, current_game)
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

            #*DIRECTOR NOT APROVED*#
            #*DIRECTOR NOT APROVED*#
            #*DIRECTOR NOT APROVED*#


#?############################# END TURN 3 #############################?#
#?############################# END TURN 3 #############################?#
#?############################# END TURN 3 #############################?#
                        #? TOTAL: 1 PROCLAMATION POSTED ¿#


            ################## Last Minister = 1 ##################
     ######################## Actual Minister = 3 ########################
#?############################# START TURN 4 #############################?#
#?############################# START TURN 4 #############################?#
#?############################# START TURN 4 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_3():
    current_game= 1
    minister_number = dbf.get_actual_minister(1)
    director_candidate= candidate_director(minister_number,1)
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
    assert response.json()["voteOut_response"] == " Player Argentina has voted"
    assert response.status_code == 200

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

            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
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
    assert response.status_code == 200


            #* DIRECTOR DISCARD CARD *#
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


            #* POST PROCLAMATION *#
def test_post_proclamation_3():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

            #* CAST SPELL *#
def test_board_game_1():
    if (dbf.get_last_proclamation(1) == 1):
        if (dbf.get_spell(1) == "Crucio"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister, 1)
            response= client.get(
                "/games/1/spell/crucio",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            if dbf.get_player_role(victim_id) == 0:
                victim_role = "Phoenix"
            else:
                victim_role = "Death Eater"

            assert ((response.json()["responseText"] == (f" {victim_nick} is a {victim_role}")) and (response.status_code == 200))

#?############################# END TURN 4 #############################?#
#?############################# END TURN 4 #############################?#
#?############################# END TURN 4 #############################?#
                        #? TOTAL: 2 PROCLAMATION POSTED ¿#


            ################## Last Minister = 3 ##################
     ######################## Actual Minister = 4 ########################
#?############################# START TURN 5 #############################?#
#?############################# START TURN 5 #############################?#
#?############################# START TURN 5 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_4():
    current_game= 1
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number, current_game)
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
    assert response.json()["voteOut_response"] == " Player Argentina has voted"
    assert response.status_code == 200

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

            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
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
    assert response.status_code == 200


            #* DIRECTOR DISCARD CARD *#
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

            #* POST PROCLAMATION *#
def test_post_proclamation_4():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    assert response.status_code == 200

            #* CAST SPELL *#
def test_board_game_2():
    if (dbf.get_last_proclamation(1) == 1):
        if (dbf.get_spell(1) == "Crucio"):
            victim = not_dead_or_myself(5,1)
            response= client.get(
                "/games/1/spell/crucio",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            if dbf.get_player_role(victim_id) == 0:
                victim_role = "Phoenix"
            else:
                victim_role = "Death Eater"

            assert ((response.json()["responseText"] == (f" {victim_nick} is a {victim_role}")) and (response.status_code == 200))

        elif (dbf.get_spell(1) == "Imperius"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister,1)
            response= client.put(
                "/games/1/spell/imperius",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            assert ((response.json()["responseText"] == (f"spell imperius has been casted to {victim_nick}")) and (response.status_code == 200) )

#?############################# END TURN 5 #############################?#
#?############################# END TURN 5 #############################?#
#?############################# END TURN 5 #############################?#
                        #? TOTAL: 3 PROCLAMATION POSTED ¿#


            ################## Last Minister = 4 ##################
     ######################## Actual Minister = 5 ########################
#?############################# START TURN 6 #############################?#
#?############################# START TURN 6 #############################?#
#?############################# START TURN 6 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
def test_select_director_5():
    current_game= 1
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number, current_game)
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
    assert response.json()["voteOut_response"] == " Player Argentina has voted"
    assert response.status_code == 200

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


            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
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
    assert response.status_code == 200

            #* DIRECTOR DISCARD CARD *#
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
    
            #* POST PROCLAMATION *#
def test_post_proclamation_5():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    assert response.status_code == 200

            #* CAST SPELL *#
def test_board_game_3():
    if (dbf.get_last_proclamation(1) == 1):
        if (dbf.get_spell(1) == "Crucio"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister, 1)
            response= client.get(
                "/games/1/spell/crucio",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            if dbf.get_player_role(victim_id) == 0:
                victim_role = "Phoenix"
            else:
                victim_role = "Death Eater"

            assert ((response.json()["responseText"] == (f" {victim_nick} is a {victim_role}")) and (response.status_code == 200))

        elif (dbf.get_spell(1) == "Imperius"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister, 1)
            response= client.put(
                "/games/1/spell/imperius",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            assert ((response.json()["responseText"] == (f"spell imperius has been casted to {victim_nick}") and (response.status_code == 200)))

        elif (dbf.get_spell(1) == "Avada Kedavra"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister, 1)
            response= client.put(
                "/games/1/spell/avada_kedavra",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_name = dbf.get_player_nick_by_id(victim_id)
            minister_id = dbf.get_player_id_by_player_number(minister, 1)
            minister_name = dbf.get_player_nick_by_id(minister_id)
            assert ((response.json()["responseText"] == (f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")) and (response.status_code == 200))

#?############################# END TURN 6 #############################?#
#?############################# END TURN 6 #############################?#
#?############################# END TURN 6 #############################?#
                        #? TOTAL: 4 PROCLAMATION POSTED ¿#


            ################## Last Minister = 5 ##################
     ######################## Actual Minister = 6 ########################
#?############################# START TURN 7 #############################?#
#?############################# START TURN 7 #############################?#
#?############################# START TURN 7 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_6():
    current_game= 1
    minister_number = dbf.get_actual_minister(1)
    director_candidate= candidate_director(minister_number,1)
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
    
def test_vote_candidate_Argentina_OK_6():
    token= logIn.getToken_Argentina()
    player_number = dbf.get_player_id_from_game(1,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(2,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(3,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(4,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(5,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(6,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(7,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(8,1)
    if dbf.is_player_alive(player_number):
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


            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#

        #! START Exeptions !#
        #! START Exeptions !#
        #! START Exeptions !#

def test_try_select_director_wrong_step_turn():
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

        #! END Exeptions !#
        #! END Exeptions !#
        #! END Exeptions !#


            #* MINISTER DISCARD CARD *#
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
    assert response.status_code == 200


            #* DIRECTOR DISCARD CARD *#
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
    
            #* POST PROCLAMATION *#
def test_post_proclamation_6():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
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

            #* CAST SPELL *#
def test_board_game_4():
    if (dbf.get_last_proclamation(1) == 1):
        if (dbf.get_spell(1) == "Crucio"):
            victim = not_dead_or_myself(5,1)
            response= client.get(
                "/games/1/spell/crucio",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            if dbf.get_player_role(victim_id) == 0:
                victim_role = "Phoenix"
            else:
                victim_role = "Death Eater"

            assert ((response.json()["responseText"] == (f" {victim_nick} is a {victim_role}")) and (response.status_code == 200))

        elif (dbf.get_spell(1) == "Imperius"):
            victim = not_dead_or_myself(5,1)
            response= client.put(
                "/games/1/spell/imperius",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            assert ((response.json()["responseText"] == (f"spell imperius has been casted to {victim_nick}") and (response.status_code == 200)))

        elif (dbf.get_spell(1) == "Avada Kedavra"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister, 1)
            response= client.put(
                "/games/1/spell/avada_kedavra",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_name = dbf.get_player_nick_by_id(victim_id)
            minister_id = dbf.get_player_id_by_player_number(minister, 1)
            minister_name = dbf.get_player_nick_by_id(minister_id)
            assert ((response.json()["responseText"] == (f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")) and (response.status_code == 200))

#?############################# END TURN 7 #############################?#
#?############################# END TURN 7 #############################?#
#?############################# END TURN 7 #############################?#
                        #? TOTAL: 5 PROCLAMATION POSTED ¿#



            ################## Last Minister = 6 ##################
     ######################## Actual Minister = 7 ########################
#?############################# START TURN 8 #############################?#
#?############################# START TURN 8 #############################?#
#?############################# START TURN 8 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

    #if((return_fenix_proclamations_game_1() != 5) and (return_death_eater_proclamations_game_1 != 6)):
def test_select_director_7(): 
    current_game= 1
    minister_number = dbf.get_actual_minister(1)
    director_candidate= candidate_director(minister_number,1)
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

def test_vote_candidate_Argentina_OK_7():
    token= logIn.getToken_Argentina()
    player_number = dbf.get_player_id_from_game(1,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(2,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(3,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(4,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(5,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(6,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(7,1)
    if dbf.is_player_alive(player_number):
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
    player_number = dbf.get_player_id_from_game(8,1)
    if dbf.is_player_alive(player_number):
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

            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
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
    assert response.status_code == 200


            #* DIRECTOR DISCARD CARD *#
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

            #* POST PROCLAMATION *#
def test_post_proclamation_7():
    response= client.put(
        "/games/1/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
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


            #* CAST SPELL *#
def test_board_game_5():
    if (dbf.get_last_proclamation(1) == 1):
        if (dbf.get_spell(1) == "Crucio"):
            victim = not_dead_or_myself(5,1)
            response= client.get(
                "/games/1/spell/crucio",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            if dbf.get_player_role(victim_id) == 0:
                victim_role = "Phoenix"
            else:
                victim_role = "Death Eater"

            assert ((response.json()["responseText"] == (f" {victim_nick} is a {victim_role}")) and (response.status_code == 200))

        elif (dbf.get_spell(1) == "Imperius"):
            victim = not_dead_or_myself(5,1)
            response= client.put(
                "/games/1/spell/imperius",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_nick = dbf.get_player_nick_by_id(victim_id)
            assert ((response.json()["responseText"] == (f"spell imperius has been casted to {victim_nick}") and (response.status_code == 200)))

        elif (dbf.get_spell(1) == "Avada Kedavra"):
            minister = dbf.get_actual_minister(1)
            victim = not_dead_or_myself(minister, 1)
            response= client.put(
                "/games/1/spell/avada_kedavra",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 1)
            victim_name = dbf.get_player_nick_by_id(victim_id)
            minister_id = dbf.get_player_id_by_player_number(minister, 1)
            minister_name = dbf.get_player_nick_by_id(minister_id)
            assert ((response.json()["responseText"] == (f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")) and (response.status_code == 200))
