from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

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


# lobby models
class LobbyInput(BaseModel):
    lobbyIn_creator : str
    lobbyIn_name: Optional[str]
    lobbyIn_max_players: Optional[int]
    lobbyIn_min_players: Optional[int]


# game models
class Game(BaseModel):
    game_is_started: bool = False               # Depends on Lobby
    game_next_minister: int                     #
    game_failed_elections: int = 0              # = 0 <= 3 then reset to 0
    game_step_turn: int = -1                    # = -1 No asigned
    game_last_director: int = -1                # = -1 No asigned
    game_last_minister: int = -1                # = -1 No asigned


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


# board models
class ViewActions(BaseModel):                   # class Actions(int, Enum): int or enum
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
    board_is_spell_active: int = False
    
class ViewActions(BaseModel):                   # Depends on ViewBoard if the board_is_spell_active= Tru # int or enum
    actions_select_director: int = 0
    actions_select_candidate: int = 1
    actions_inializate_proclamation: int = 2
    actions_select_card: int = 3
    actions_send_card: int = 4
    actions_discart_card: int = 5
    actions_end_proclamation: int = 6


# log models
class ViewLog(BaseModel):
    log_won_games_fenix: int = 0        
    log_won_games_death_eater: int = 0  
    log_lost_games_fenix: int = 0       
    log_lost_games_death_eater: int = 0 
