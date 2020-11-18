from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class ResponseText(BaseModel):
    responseText: str


# user models
class UserIn(BaseModel):
    userIn_email: EmailStr                      # API Request body    
    userIn_username: str                        # API Request body
    userIn_password: str                        # API Request body
    userIn_photo: Optional[str]


class UserOut(BaseModel):
    userOut_email: str                          # API response
    userOut_username: str                       # API response
    userOut_operation_result: str               # for Successful Operation


class ChangeProfile(BaseModel):
    username: Optional[str] = None
    photo: Optional[str] = None


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


class ProfileInformation(BaseModel):
    profile_username: str
    profile_photo: str = ''


# authorization models
class Token(BaseModel):
    access_token: str
    token_type: str
  
class TokenData(BaseModel):
    email: Optional[str] = None

    
# lobby models
class LobbyIn(BaseModel):
    lobbyIn_name: str                           # API Request body
    lobbyIn_max_players: int = 10               # API Request body
    lobbyIn_min_players: int = 5                # API Request body


class LobbyOut(BaseModel):
    lobbyOut_name : str                         # API response
    lobbyOut_Id : int                           # API response
    lobbyOut_player_id : int                    
    lobbyOut_player_nick: str
    lobbyOut_result : str                       # for Successful Operation


class LobbyDict(BaseModel):
    lobbyDict: Dict


class JoinLobby(BaseModel):
    joinLobby_name : str
    joinLobby_player_id: int
    joinLobby_player_nick: str
    joinLobby_result : str
    joinLobby_nicks : list
    joinLobby_is_owner: bool


class Nick(BaseModel):
    nick: str


# game models
class ViewGame(BaseModel):
    #game_board
    game_is_started: bool = False           # Depends on Lobby
    game_total_players: int                 # Depends on Lobby (<=10 a&& >=5)
    game_actual_minister: int = 0           # Depends on player_number
    game_failed_elections: int = 0          # = 0 <= 3 then reset to 0
    game_step_turn: int = -1                # = -1 No asigned
    game_candidate_director: int = -1       #REVIEW # Player number
    game_votes: int = 0                     #REVIEW # Count players who have voted
    game_status_vote: int = 0               #REVIEW # Result votes [5 OK] [5 No] 
    game_last_director: int = -1            # = -1 No asigned
    game_last_minister: int = -1            # = -1 No asigned



class GameDict(BaseModel):
    gameDict: Dict


# This model is to recive Player Information
class SelectMYDirector(BaseModel):
    dir_game_id: int
    dir_player_number: int
    dir_game_response: str


class Vote(BaseModel):
    vote: bool


class VoteOut(BaseModel):
    voteOut: bool
    voteOut_game_id: int
    voteOut_response: str


# player models
class PlayerIn(BaseModel):
    player_nick: str                            # = userName Depends on User
    player_vote: bool                           # True = positive
    player_direct_select: str                   # = player_nick or player_number


class PlayerOut(BaseModel):
    player_nick: str                            # = userName Depends on User
    player_role: int = -1                       # = -1 No asigned
    player_is_alive: bool = True                # = True
    player_chat_blocked: bool = False           # = False
    player_is_candidate: bool = False #REVIEW
    player_has_voted: bool = False #REVIEW
    player_vote: bool = False #REVIEW
    player_director: bool = False
    player_minister: bool = False
    player_last_director: int = -1              # = -1 No asigned
    player_last_minister: int = -1              # = -1 No asigned
 

class PlayerNumber(BaseModel):
    playerNumber: int


class ViewPlayerGame(BaseModel):
    player_game_id : int                        # Depends on Game
    player_number: int                          # Defines order
    player_nick: str                            # = userName Depends on User
    player_role: int = -1                       # = -1 No asigned
    player_is_alive: bool = True                # = True
    player_chat_blocked: bool = False           # = False
    player_director: bool = False               # = False
    player_minister: bool = False               # = False
    player_last_director: int = -1              # = -1 No asigned
    player_last_minister: int = -1              # = -1 No asigned
      
 
# board models
# Usable for next sprint
class ViewActions(BaseModel): # Depends on ViewBoard if the board_is_spell_active= Tru # int or enum
    # int or enum
    actions_select_director: int = 0
    actions_select_candidate: int = 1
    actions_inializate_proclamation: int = 2
    actions_select_card: int = 3
    actions_send_card: int = 4
    actions_discart_card: int = 5
    actions_end_proclamation: int = 6

      
class ViewBoard(BaseModel):
    board_promulged_fenix: int = 0
    board_promulged_death_eater: int = 0
    board_response: str


# REVIEW
class Card(BaseModel):
    card_discarted: int = -1


class ProclamationCard(BaseModel):
    proclamationCard_phoenix: bool

      
class Prophecy(BaseModel):
    prophecy_card_0: int
    prophecy_card_1: int
    prophecy_card_2: int


class Victim(BaseModel):
    victim_number: int


#class ViewSpells(int, Enum): # Depends on ViewBoard if the board_is_spell_active= True
#    spell_caos = 0
#    spell_expelliarmus = 1
#    spell_avada_kedavra = 2
#    spell_prophecy = 3                         # adivinacion
#    spell_imperius = 4
#    spell_crucio = 5

   
# log models
# Usable for next sprint
class ViewLog(BaseModel):
    log_won_games_fenix: int = 0         
    log_won_games_death_eater: int = 0
    log_lost_games_fenix: int = 0     
    log_lost_games_death_eater: int = 0


#socket models
class Echo(BaseModel):
    player_id : int = None
    game_id: int = None
    message: dict
