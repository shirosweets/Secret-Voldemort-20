from pony.orm import db_session, select, count
import db_entities_relations as dbentities 
from typing import Optional

# some users functions
@db_session
def check_email_exists(new_email):
    return dbentities.User.exists(user_email=new_email)

@db_session
def check_username_exists(new_uname):
    return dbentities.User.exists(user_name=new_uname)

@db_session
def insert_user(user_email:str, user_name:str, user_password:str, user_photo: Optional[str]):
    if photo is None:
        dbentities.User(user_email=email, user_name=username, user_password=password, user_photo="https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/")
    else: 
        dbentities.User(user_email=email, user_name=username, user_password=password, user_photo=photo)

# some lobby funtions

@db_session
def exist_lobby_name(lobbyIn_name):
    return dbentities.Lobby.exists(lobby_name=lobbyIn_name)

@db_session
def check_max_players(lobbyIn_max_players):
    return (5 <= lobbyIn_max_players <=10)

@db_session
def check_min_players(lobbyIn_min_players, lobbyIn_max_players):
    return (5 <= lobbyIn_max_players <= lobbyIn_max_players <=10)


@db_session
def create_lobby(
                 lobbyIn_name: str,
                 lobbyIn_creator: str,
                 lobbyIn_max_players: int, 
                 lobbyIn_min_players: int):
    dbentities.Lobby(
                    lobby_name = lobbyIn_name, 
                    lobby_creator = lobbyIn_creator,
                    lobby_max_players = lobbyIn_max_players, 
                    lobby_min_players = lobbyIn_min_players
                    )
    return int(dbentities.Lobby.lobby_id)
# some player functions


# some game functions


# some board functions


# some log functions
