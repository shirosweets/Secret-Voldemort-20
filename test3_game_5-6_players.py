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


             ######################################## GAME 2: 5 Players ########################################

def return_token_minister():
    if (dbf.is_imperius_active(2) == -1):
        player_number_actual_minister= dbf.get_actual_minister(2)
    else:
        player_number_actual_minister= dbf.is_imperius_active(2)
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
        
def return_token_NOT_minister():
    player_number_actual_minister= dbf.get_actual_minister(1)
    player_id_actual_minister = dbf.get_player_id_by_player_number(player_number_actual_minister + 1, 1)
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

def return_token_director():
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

def return_id_minister():
    player_number_actual_minister= dbf.get_actual_minister(2)
    player_id_actual_minister = dbf.get_player_id_by_player_number(player_number_actual_minister, 2)
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

def return_fenix_proclamations():
    return dbf.get_total_proclamations_phoenix(2)

def return_death_eater_proclamations():
    return dbf.get_total_proclamations_death_eater(2)

#?############################# START GAME 2 #############################¿#
#?############################# START GAME 2 #############################¿#
#?############################# START GAME 2 #############################¿#

    ################### Last Minister = -1, Director = -1 ###################
     ######################## Actual Minister = 0 ########################
#*############################# START TURN 1 #############################*#

def test_select_director_1():
    current_game= 2
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number,current_game)
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    assert response.status_code == 200

def test_vote_candidate_Amber_OK_1():
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

def test_vote_candidate_Benny_OK_1():
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

def test_vote_candidate_Candy_OK_1():
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

def test_vote_candidate_Denis_OK_1():
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

def test_vote_candidate_Ember_OK_1():
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


            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD*#
def test_discard_card_Minister_1():
    response= client.put(
        "/games/2/discard_card/",
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
        "/games/2/discard_card/",
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
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

#?############################# END TURN 1 #############################?#
#?############################# END TURN 1 #############################?#
#?############################# END TURN 1 #############################?#

                        #? TOTAL: 1 PROCLAMATION POSTED ¿#
            ################## Last Minister = 0 ##################
     ######################## Actual Minister = 1 ########################
#?############################# START TURN 2 #############################?#
#?############################# START TURN 2 #############################?#
#?############################# START TURN 2 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_2():
    current_game= 2
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number,current_game)
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    assert response.status_code == 200

def test_vote_candidate_Amber_OK_2():
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

def test_vote_candidate_Benny_OK_2():
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

def test_vote_candidate_Candy_OK_2():
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

def test_vote_candidate_Denis_OK_2():
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

def test_vote_candidate_Ember_OK_2():
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

        
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
def test_discard_card_Minister_2():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_minister()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200


            #* DIRECTOR DISCARD CARD *#
def test_discard_card_Director_2():
    response= client.put(
        "/games/2/discard_card/",
        headers= {
            "Authorization": return_token_director()
        },
        json= {
            "card_discarted": 1
        }
    )
    assert response.status_code == 200


            #* POST PROCLAMATION *#
def test_post_proclamation_2():
    response= client.put(
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.status_code == 200
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

#?############################# END TURN 2 #############################?#
#?############################# END TURN 2 #############################?#
#?############################# END TURN 2 #############################?#

                        #? TOTAL: 2 PROCLAMATION POSTED ¿#
            ################## Last Minister = 1 ##################
     ######################## Actual Minister = 2 ########################
#?############################# START TURN 3 #############################?#
#?############################# START TURN 3 #############################?#
#?############################# START TURN 3 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_3():
    current_game= 2
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number, current_game)
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    assert response.status_code == 200

def test_vote_candidate_Amber_OK_3():
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

def test_vote_candidate_Benny_OK_3():
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

def test_vote_candidate_Candy_OK_3():
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

def test_vote_candidate_Denis_OK_3():
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

def test_vote_candidate_Ember_OK_3():
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

            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
def test_discard_card_Minister_3():
    response= client.put(
        "/games/2/discard_card/",
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
        "/games/2/discard_card/",
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
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    assert response.status_code == 200

            #* CAST SPELL *#
def test_board_game_3():
    if (dbf.get_last_proclamation(2) == 1):
        if (dbf.get_spell(2) == "Prophecy"):
            minister = dbf.get_actual_minister(2)
            victim = not_dead_or_myself(minister, 2)
            response= client.get(
                "/games/2/spell/prophecy",
                headers= {
                    "Authorization": return_token_minister()
                }
            )
            cards = dbf.get_three_cards(2)
            assert response.json()["prophecy_card_0"] == cards.prophecy_card_0
            assert response.json()["prophecy_card_1"] == cards.prophecy_card_1
            assert response.json()["prophecy_card_2"] == cards.prophecy_card_2

#?############################# END TURN 3 #############################?#
#?############################# END TURN 3 #############################?#
#?############################# END TURN 3 #############################?#
                        #? TOTAL: 3 PROCLAMATION POSTED ¿#

            ################## Last Minister = 3 ##################
     ######################## Actual Minister = 4 ########################
#?############################# START TURN 4 #############################?#
#?############################# START TURN 4 #############################?#
#?############################# START TURN 4 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_4(): 
    current_game= 2
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number, current_game)
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    assert response.status_code == 200

def test_vote_candidate_Amber_OK_4():
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

def test_vote_candidate_Benny_OK_4():
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

def test_vote_candidate_Candy_OK_4():
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

def test_vote_candidate_Denis_OK_4():
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

def test_vote_candidate_Ember_OK_4():
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

        
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
def test_discard_card_Minister_4():
    response= client.put(
        "/games/2/discard_card/",
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
        "/games/2/discard_card/",
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
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    assert response.status_code == 200

            #* CAST SPELL *#
def test_board_game_4():
    if (dbf.get_last_proclamation(2) == 1):
        if (dbf.get_spell(2) == "Prophecy"):
            minister = dbf.get_actual_minister(2)
            victim = not_dead_or_myself(minister, 2)
            response= client.get(
                "/games/2/spell/prophecy",
                headers= {
                    "Authorization": return_token_minister()
                }
            )
            cards = dbf.get_three_cards(2)
            assert response.json()["prophecy_card_0"] == cards.prophecy_card_0
            assert response.json()["prophecy_card_1"] == cards.prophecy_card_1
            assert response.json()["prophecy_card_2"] == cards.prophecy_card_2

        elif (dbf.get_spell(2) == "Avada Kedavra"):
            minister = dbf.get_actual_minister(2)
            victim = not_dead_or_myself(minister, 2)
            response= client.put(
                "/games/2/spell/avada_kedavra",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 2)
            victim_name = dbf.get_player_nick_by_id(victim_id)
            minister_id = dbf.get_player_id_by_player_number(minister, 2)
            minister_name = dbf.get_player_nick_by_id(minister_id)
            assert ((response.json()["responseText"] == (f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")) and (response.status_code == 200))

#?############################# END TURN 4 #############################?#
#?############################# END TURN 4 #############################?#
#?############################# END TURN 4 #############################?#
                        #? TOTAL: 4 PROCLAMATION POSTED ¿#

            ################## Last Minister = 4 ##################
     ######################## Actual Minister = 5 ########################
#?############################# START TURN 5 #############################?#
#?############################# START TURN 5 #############################?#
#?############################# START TURN 5 #############################?#

        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#
        #* SELECT DIRECTOR AND VOTE IT *#

def test_select_director_5():
    current_game= 2
    minister_number = dbf.get_actual_minister(current_game)
    director_candidate= candidate_director(minister_number, current_game)
    response= client.post(
                    "/games/2/select_director/",
                    headers= { 
                        "Authorization": return_token_minister()},
                    json= {
                        "playerNumber": director_candidate
                    })
    player_id_selected_candidate= dbf.get_player_id_by_player_number(director_candidate, current_game)
    player_nick_selected_candidate= dbf.get_player_nick_by_id(player_id_selected_candidate)
    assert response.json()["dir_game_response"] == (f" Player {player_nick_selected_candidate} is now director candidate")
    assert response.status_code == 200

def test_vote_candidate_Amber_OK_5():
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

def test_vote_candidate_Benny_OK_5():
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

def test_vote_candidate_Candy_OK_5():
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

def test_vote_candidate_Denis_OK_5():
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

def test_vote_candidate_Ember_OK_5():
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
        
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#
            #*DIRECTOR APROVED*#


            #* MINISTER DISCARD CARD *#
def test_discard_card_Minister_5():
    response= client.put(
        "/games/2/discard_card/",
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
        "/games/2/discard_card/",
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
        "/games/2/proclamation/",
        headers= {
            "Authorization": return_token_director()
        }
    )
    if(return_fenix_proclamations() >= 5):
        assert response.status_code == 307
        assert response.json()["detail"] == " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
    elif(return_death_eater_proclamations() >= 6):
        assert response.status_code == 307
        assert response.json()["detail"] == " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
    else:
        assert response.status_code == 200
        assert response.json()["board_response"] == " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"

            #* CAST SPELL *#
def test_board_game_5():
    if (dbf.get_last_proclamation(2) == 1):
        if (dbf.get_spell(2) == "Prophecy"):
            minister = dbf.get_actual_minister(2)
            victim = not_dead_or_myself(minister, 2)
            response= client.get(
                "/games/2/spell/prophecy",
                headers= {
                    "Authorization": return_token_minister()
                }
            )
            cards = dbf.get_three_cards(2)
            assert response.json()["prophecy_card_0"] == cards.prophecy_card_0
            assert response.json()["prophecy_card_1"] == cards.prophecy_card_1
            assert response.json()["prophecy_card_2"] == cards.prophecy_card_2

        elif (dbf.get_spell(2) == "Avada Kedavra"):
            minister = dbf.get_actual_minister(2)
            victim = not_dead_or_myself(minister, 2)
            response= client.put(
                "/games/2/spell/avada_kedavra",
                headers= {
                    "Authorization": return_token_minister()
                },
                json= {
                    "victim_number": victim
                }
            )
            victim_id = dbf.get_player_id_by_player_number(victim, 2)
            victim_name = dbf.get_player_nick_by_id(victim_id)
            minister_id = dbf.get_player_id_by_player_number(minister, 2)
            minister_name = dbf.get_player_nick_by_id(minister_id)
            assert ((response.json()["responseText"] == (f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")) and (response.status_code == 200))
            