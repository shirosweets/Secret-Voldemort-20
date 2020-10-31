from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

# # MODELO SACADO DE PYDANTIC
# class User(BaseModel):
#     id: int
#     name = 'Jane Doe'
#     size: float = None
"""
Here is a model with two fields id which is an integer and is required, and name which is a string 
and is not required (it has a default value). The type of name is inferred from the default value, and so 
a type annotation is not required (however note this warning about field order when some fields do not have
 type annotations).
"""

# user models
class UserIn(BaseModel):
    userIn_email: EmailStr                      # API Request body    
    userIn_username: str                        # API Request body
    userIn_password: str                        # API Request body
    userIn_photo: Optional[str]
      
    def valid_format_username(self) -> bool:
        return 3 < len(self.userIn_username) < 17
      
    def valid_format_password(self) -> bool:
        return 7 < len(self.userIn_password) < 33

      
class UserOut(BaseModel):
    userOut_email: str                          # API response
    userOut_username: str                       # API response
    userOut_operation_result: str               # for Successful Operation
      
      
class LogIn(BaseModel):
    logIn_email: str                            # API Request body
    logIn_password: str                         # API Request body

# lobby models
class LobbyIn(BaseModel):
    lobbyIn_creator: int
    lobbyIn_name: str
    lobbyIn_max_players: int = 10
    lobbyIn_min_players: int = 5

class LobbyOut(BaseModel):
    lobbyOut_name : str
    lobbyOut_Id : int
    lobbyOut_result : str

class JoinLobby(BaseModel):
    joinLobby_name : str


# game models
class ViewGame(BaseModel):
    #game_board
    game_is_started: bool = False               # Depends on Lobby
    game_total_players : int                    # Depends on Lobby (<=10 a&& >=5)
    game_next_minister: int = 0                 # Depends on player_number
    game_failed_elections: int = 0              # = 0 <= 3 then reset to 0
    game_step_turn:         int = -1                    # = -1 No asigned
    game_last_director:     int = -1                # = -1 No asigned
    game_last_minister:     int = -1                # = -1 No asigned


# This model is to recive Player Information
class SelectMYDirector(BaseModel):
    dir_game_id: Optional[int] 
    dir_player_number: Optional[int]
        
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
 

class ViewPlayerGame(BaseModel):
    player_game_id : int                        # Depends on Game
    player_number: int                          # Defines order
    player_nick: str                            # = userName Depends on User
    player_role: int = -1                       # = -1 No asigned
    player_is_alive: bool = True                # = True
    player_chat_blocked: bool = False           # = False
    player_director: bool = False
    player_minister: bool = False
    player_last_director: int = -1              # = -1 No asigned
    player_last_minister: int = -1              # = -1 No asigned
      
 
# board models
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
    board_promulged_fenix: Optional[int] = 0
    board_promulged_death_eater: Optional[int] = 0
    board_is_spell_active: int = False

      
#class ViewSpells(int, Enum): # Depends on ViewBoard if the board_is_spell_active= True
#    spell_caos = 0
#    spell_expelliarmus = 1
#    spell_avada_kedavra = 2
#    spell_prophecy = 3                         # adivinacion
#    spell_imperius = 4
#    spell_crucio = 5

   
# log models
class ViewLog(BaseModel):
    log_won_games_fenix: int = 0                # = 0
    log_won_games_death_eater: int = 0          # = 0
    log_lost_games_fenix: int = 0               # = 0
    log_lost_games_death_eater: int = 0         # = 0
