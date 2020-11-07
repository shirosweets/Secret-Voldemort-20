from pony.orm import Database, PrimaryKey, Required, Optional, Set
from datetime import datetime

db = Database()


# user entity
class User(db.Entity):
    user_id                 = PrimaryKey(int, auto=True)              # auto is auto-incremented
    user_email              = Required(str, unique=True)              # email can't change
    user_name               = Required(str, unique=True, max_len=16)  # user_name can't change
    user_password           = Required(str)
    user_photo              = Required(str)                           # photo is selected for default string
    user_creation_dt        = Required(datetime) #! FIXME Added for checks endpoint 'Login'
    user_disabled           = Required(bool)
    user_lobby              = Set('Lobby')                            # many to many relation with User-Lobby, we use '' because Player is declarated after this call
    user_player             = Set('Player')                           # one to many relation with User-Player, we use '' because Player is declarated after this call
    user_log                = Optional('Log')                         # one to one relation with User-Log, we use '' because Log is declarated after this call
    # For next sprint                     
    #user_default_icon_id         = Optional(int)                    # icon is selected for default = 0 | 1 | 2 | 3


# lobby entity
class Lobby(db.Entity):
    lobby_id                = PrimaryKey(int, auto = True)
    lobby_name              = Required(str, unique=True)
    lobby_max_players       = Optional(int, default = 10)   # <=10
    lobby_min_players       = Optional(int, default = 5)    # >=5
    lobby_creator           = Required(int)                 # user_id of the creator
    lobby_user              = Set(User)                     # many to many relation with Lobby-User, we use '' because Player is declarated after this call
    lobby_players           = Set('Player')                 # one to many relation with Lobby-Player, we use '' because Player is declarated after this call


# game entity
class Game(db.Entity):
    # Game iniciated when the creator of the Lobby start the game
    # All players at the Lobby 
    game_id                 = PrimaryKey(int, auto= True)
    game_is_started         = Required(bool)   # Depends on Lobby = False
    game_total_players      = Required(int)    # Depends on Lobby (<=10 a&& >=5)
    game_next_minister      = Required(int)    # Logical election
    game_failed_elections   = Required(int)    # = 0 <= 3 then reset to 0
    game_step_turn          = Required(int)    # = -1 No asigned
    game_last_director      = Required(int)    # = -1 No asigned
    game_last_minister      = Required(int)    # = -1 No asigned
    game_players            = Set('Player')    # Relation 1 Game to many Player
    game_board_game         = Optional('Board')    # Relation 1 Game to 1 Board


# player entity
class Player(db.Entity):
    player_id               = PrimaryKey(int, auto=True)
    player_number           = Optional(int)    # Definied order
    player_nick             = Required(str)    # = userName Depends on User
    player_role             = Required(int)    # = -1 No asigned
    player_is_alive         = Required(bool)   # = True
    player_chat_blocked     = Required(bool)   # = False
    player_director         = Required(bool)
    player_minister         = Required(bool)
    player_game             = Optional(Game)   # one to many relation with Player-Game
    player_lobby            = Optional(Lobby)  # one to many relation with Player-Game, is optional because the Lobby is deleted when game starts   
    player_user             = Required(User)   # one to many relation with Player-User {...}


# board entity Depends on Game
class Board(db.Entity):
    #board_id= 
    board_game                  = Required(Game)    # Depends on Game
    board_promulged_fenix       = Required(int)     # = 0
    board_promulged_death_eater = Required(int)     # = 0
    board_deck_codification     = Required(int)     # binarie
    board_is_spell_active       = Required(bool)    # = False


# log entity Depends on Game
class Log(db.Entity):
    log_user                     = Required(User)   # Depends on User
    log_won_games_fenix          = Required(int)    # = 0
    log_won_games_death_eater    = Required(int)    # = 0
    log_lost_games_fenix         = Required(int)    # = 0
    log_lost_games_death_eater   = Required(int)    # = 0
    

# 1) Connect the object 'db' with data base
db.bind('sqlite', 'data_base.sqlite', create_db=True) # 1)
# 2) Generate the data base
db.generate_mapping(create_tables=True) # 2)