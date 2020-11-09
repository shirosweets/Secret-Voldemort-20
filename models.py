from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


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
    lobbyOut_result : str                       # for Successful Operation


class WantedLobbies(BaseModel):
    WantedLobbies_from: int = 1
    WantedLobbies_end_at: Optional[int] = None


class LobbyDict(BaseModel):
    lobbyDict: Dict


class JoinLobby(BaseModel):
    joinLobby_name : str
    joinLobby_result : str


class Nick(BaseModel):
    nick: str


class ChangeNick(BaseModel):
    changeNick_result: str


class LeaveLobby(BaseModel):
    leaveLobby_response: str


# game models
class ViewGame(BaseModel):
    #game_board
    game_is_started: bool = False               # Depends on Lobby
    game_total_players : int                    # Depends on Lobby (<=10 a&& >=5)
    game_actual_minister: int = 0               # Depends on player_number
    game_failed_elections: int = 0              # = 0 <= 3 then reset to 0
    game_step_turn:         int = -1            # = -1 No asigned
    game_last_director:     int = -1            # = -1 No asigned
    game_last_minister:     int = -1            # = -1 No asigned


class GameOut(BaseModel):
    gameOut_result: str


class GameDict(BaseModel):
    gameDict: Dict


# This model is to recive Player Information
class SelectMYDirector(BaseModel):
    dir_game_id: int
    dir_player_number: int
    dir_game_response: str


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


class ProclamationCard(BaseModel):
    proclamationCard_phoenix: bool

      
class Prophecy(BaseModel):
    prophecy_card_0: int
    prophecy_card_1: int
    prophecy_card_2: int


# REVIEW Added Models
class AvadaKedavra(BaseModel):
    AvadaKedavra_response: str


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
