from pony.orm import Database, PrimaryKey, Required, Optional, Set
from datetime import datetime

db = Database()

# user entity
class User(db.Entity):
    user_lobby              = Set('Lobby')       # many to many relation with User-Lobby, we use '' because Player is declarated after this call
    user_player             = Set('Player')      # one to many relation with User-Player, we use '' because Player is declarated after this call
    user_log                = Required('Log')    # one to one relation with User-Log, we use '' because Log is declarated after this call
    user_id                 = PrimaryKey(int, auto=True)   # auto is auto-incremented
    user_email              = Required(str, unique=True)   # email can't change
    user_name               = Required(str, unique=True, max_len=16)  # user_name can't change
    user_password           = Required(str, max_len= 32)
    user_photo              = Required(int)    # photo is selected for default = 0 | 1 | 2 | 3
    # For next sprint
    user_image              = Optional(str)    # image is selected from the computer
    user_create_dt          = datetime
    
# lobby entity
class Lobby(db.Entity):
    lobby_id                = PrimaryKey(int, auto = True)
    lobby_user              = Set(User)         # many to many relation with Lobby-User, we use '' because Player is declarated after this call
    lobby_players           = Set('Player')     # one to many relation with Lobby-Player, we use '' because Player is declarated after this call
    lobby_name              = Required(str, unique=True)
    lobby_max_players       = Required(int)   # <=10
    lobby_min_players       = Required(int)   # >=5
    lobby_creator           = Required(str)   # user_name or user_id of the creator
    
# game entity
class Game(db.Entity):
    # Game iniciated when the creator of the Lobby start the game
    # All players at the Lobby 
    game_players            = Set('Player')    # Relation 1 Game to many Player
    game_board_game         = Required('Board')    # Relation 1 Game to 1 Board
    game_is_started         = Required(bool)    # Depends on Lobby = False
    game_next_minister      = Required(int)    # Logical election
    game_failed_elections   = Required(int)    # = 0 <= 3 then reset to 0
    game_step_turn          = Required(int)    # = -1 No asigned
    game_last_director      = Required(int)    # = -1 No asigned
    game_last_minister      = Required(int)    # = -1 No asigned

# player entity
class Player(db.Entity):
    player_game             = Required(Game)   # one to many relation with Player-Game
    player_lobby            = Optional(Lobby)   # one to many relation with Player-Game, is optional because the Lobby is deleted
    player_user             = Required(User)    # one to many relation with Player-User {...}
    player_number           = Required(int, unique = True)    # Definied order
    player_nick             = Required(str)    # = userName Depends on User
    player_role             = Required(int)    # = -1 No asigned
    player_is_alive         = Required(bool)    # = True
    player_chat_blocked     = Required(bool)    # = False
    player_director         = Required(bool)
    player_minister         = Required(bool)
    
# board entity
class Board(db.Entity):
    board_game              = Required(Game)    # Depends on Game
    board_promulged_fenix   = Required(int)    # = 0
    board_promulged_death_eater= Required(int)    # = 0
    board_deck_codification = Required(int)    # binarie
    board_is_spell_active   = Required(bool)    # = False
    
# log entity Depends on Game
class Log(db.Entity):
    log_user                = Required(User)    # Depends on User
    log_won_games_fenix     = Required(int)    # = 0
    log_won_games_death_eater= Required(int)    # = 0
    log_lost_games_fenix    = Required(int)    # = 0
    log_lost_games_death_eater= Required(int)    # = 0


# 1) Connect the object 'db' with data base
db.bind('sqlite', 'data_base.sqlite', create_db=True) # 1)
# 2) Generate the data base
db.generate_mapping(create_tables=True) # 2)
