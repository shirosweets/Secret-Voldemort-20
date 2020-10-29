from pony.orm import db_session, select, count
import db_entities_relations as dbe 
from typing import Optional


@db_session
def getEmails():
    print(dbe.User.select().show())

# some users functions
@db_session
def check_email_exists(new_email):
    return dbe.User.exists(user_email=new_email)

@db_session
def check_username_exists(new_uname):
    return dbe.User.exists(user_name=new_uname)

@db_session
def insert_user(email:str, username:str, password:str, photo: Optional[str]):
    if photo is None:
        dbe.User(user_email=email, user_name=username, user_password=password, user_image = 1, user_photo="https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/")
    else: 
        dbe.User(user_email=email, user_name=username, user_password=password, user_image = 1, user_photo=photo)

@db_session
def exist_user_email(userIn_email):
    return dbe.User.exists(user_email=userIn_email)

@db_session
def get_user_by_email(email):
    return dbe.User.get(user_email=email)

# some lobby funtions

@db_session
def exist_lobby_name(lobbyIn_name):
    return dbe.Lobby.exists(lobby_name=lobbyIn_name)

@db_session
def check_max_players(lobbyIn_max_players):
    return not (5 <= lobbyIn_max_players <=10)

@db_session
def check_min_players(lobbyIn_min_players, lobbyIn_max_players):
    return not (5 <= lobbyIn_max_players <= lobbyIn_max_players <=10)


@db_session
def create_lobby(
                 lobbyIn_name: str,
                 lobbyIn_creator: int, #str,
                 lobbyIn_max_players: int, 
                 lobbyIn_min_players: int):
    lobby1= dbe.Lobby(
                    lobby_name = lobbyIn_name, 
                    lobby_creator = dbe.User[lobbyIn_creator].user_name, #lobbyIn_creator,
                    lobby_max_players = lobbyIn_max_players, 
                    lobby_min_players = lobbyIn_min_players)
    dbe.Lobby.select().show()
    return lobby1

@db_session
def check_user_presence_in_lobby(lobby_id: int, current_user: int):

    presence = dbe.UserPresence.get(dbe.User[current_user], dbe.Lobby[lobby_id])
    return presence
     
@db_session
def join_game(current_user: int, lobby_id: int):
    player1= dbe.Player(
                    player_user = dbe.User[current_user],
                    player_lobby = dbe.Lobby[lobby_id],
                    player_nick = dbe.User[current_user].user_name,
                    player_role = -1,
                    player_is_alive = True,
                    player_chat_blocked = False,
                    player_director = False,
                    player_minister = False
                    )
    dbe.Player.select().show()
    return player1


# some player functions


# some game functions


# some board functions


# some log functions
