from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = "5becea4926a7daf6c72854463b1f0a27c400c81fe5ff28baf133af11642d1c88"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# user models
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserIn(BaseModel):
    userIn_email: EmailStr                      # API Request body    
    userIn_username: str                        # API Request body
    userIn_password: str                        # API Request body
    userIn_photo: Optional[str]
    #userIn_disabled: Optional[bool] = None

    def valid_format_username(self) -> bool:
        return 3 < len(self.userIn_username) < 17
      
    def valid_format_password(self) -> bool:
        return 7 < len(self.userIn_password) < 33

      
class UserOut(BaseModel):
    userOut_email: str                          # API response
    userOut_username: str                       # API response
    userOut_operation_result: str               # for Successful Operation


class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# lobby models
class LobbyIn(BaseModel):
    lobbyIn_name: str                           # API Request body
    lobbyIn_max_players: int = 10               # API Request body
    lobbyIn_min_players: int = 5                # API Request body


class LobbyOut(BaseModel):
    lobbyOut_name : str                         # API response
    lobbyOut_Id : int                           # API response
    lobbyOut_result : str                       # for Successful Operation


class JoinLobby(BaseModel):
    joinLobby_name : str
    joinLobby_result = str


# game models
class ViewGame(BaseModel):
    #game_board
    game_is_started: bool = False               # Depends on Lobby
    game_total_players : int                    # Depends on Lobby (<=10 a&& >=5)
    game_next_minister: int = 0                 # Depends on player_number
    game_failed_elections: int = 0              # = 0 <= 3 then reset to 0
    game_step_turn:         int = -1            # = -1 No asigned
    game_last_director:     int = -1            # = -1 No asigned
    game_last_minister:     int = -1            # = -1 No asigned


class GameOut(BaseModel):
    gameOut_result: str


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
    board_is_spell_active: int = False
    board_response: str

      
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
    log_won_games_fenix: int = 0                # = 0
    log_won_games_death_eater: int = 0          # = 0
    log_lost_games_fenix: int = 0               # = 0
    log_lost_games_death_eater: int = 0         # = 0