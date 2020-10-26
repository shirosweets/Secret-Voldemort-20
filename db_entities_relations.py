from pony.orm import Database, PrimaryKey, Required, Optional, Set
from datetime import datetime

db = Database()

# user entity
class User(db.Entity):
    user_id                 = PrimaryKey(int, auto=True) 
    user_email              = Required(str, unique=True)
    user_name               = Required(str, unique=True, max_len=16)
    user_password           = Required(str, max_len= 32)
    user_photo              = Optional(str)
    user_create_dt          = datetime
    user_lobby              = Set('Lobby')        # many to many relation with User-Lobby, we use '' because Player is declarated after this call
    user_player             = Set('Player')      # one to many relation with User-Player, we use '' because Player is declarated after this call
    
# lobby entity

class Lobby(db.Entity):
    lobby_id                = PrimaryKey(int, auto = True)
    lobby_creator           = Set(User)         # many to many relation with Lobby-User, we use '' because Player is declarated after this call
    lobby_players           = Set('Player')     # one to many relation with Lobby-Player, we use '' because Player is declarated after this call
    lobby_name              = Required(str, unique=True)
    lobby_max_players       = Required(int)
    lobby_min_players       = Required(int)
    
#game entity


# player entity

class Player(db.Entity):
    #player_game             = Required(Game)   # one to many relation with Player-Game
    player_lobby            = Required(Lobby)   # one to many relation with Player-Game
    player_id               = Required(User)    # one to many relation with Player-Game
    player_number           = Required(int, unique = True)
    player_nick             = Required(str) 
    player_role             = Required(int)
    player_is_alive         = Required(bool)
    player_chat_blocked     = Required(bool)
    player_director         = Required(bool)
    player_minister         = Required(bool)

#log entity


# connect the object 'db' with data base
db.bind('sqlite', 'data_base.sqlite', create_db=True)
# generate the data base
db.generate_mapping(create_tables=True)
