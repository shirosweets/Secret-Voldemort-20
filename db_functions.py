from pony.orm import db_session, select, count, flush
import db_entities_relations as dbe 
import models as md
import helpers_functions as hf
from typing import Optional
from datetime import datetime

# user functions
@db_session
def check_email_exists(new_email):
    return dbe.User.exists(user_email=new_email)


@db_session
def check_username_exists(new_uname):
    return dbe.User.exists(user_name=new_uname)


@db_session
def get_user_by_email(email):
    return dbe.User.get(user_email=email)


@db_session
def get_user_by_username(username):
    return dbe.User.get(user_name=username)

@db_session
def create_user(email: str, username: str, password: str,
                photo: str = "https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/"):
    dbe.User(
        user_email=email,
        user_name=username,
        user_password=password,
        user_photo=photo, 
        user_creation_dt=datetime.now())


@db_session
def insert_user(email: str, username: str, password: str,
                photo: Optional[str]):
    if photo is None:
        dbe.User(
            user_email=email,
            user_name=username,
            user_password=password,
            user_photo="https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/",
            user_creation_dt=datetime.now())
    else:
        dbe.User(
            user_email=email,
            user_name=username,
            user_password=password,
            user_photo=photo, 
            user_creation_dt=datetime.now())


# lobby funtions

@db_session
def exist_lobby_name(lobbyIn_name):
    return dbe.Lobby.exists(lobby_name=lobbyIn_name)

@db_session
def check_max_players(lobbyIn_max_players):
    return not (5 <= lobbyIn_max_players <=10)

@db_session
def check_min_players(lobbyIn_min_players, lobbyIn_max_players):
    return not (5 <= lobbyIn_max_players <= lobbyIn_max_players <=10)

######

@db_session
def get_lobby_by_id(id: int):
    return dbe.Lobby.get(lobby_id=id)

"""
@db_session
def get_players_lobby(id: int):
    
    Get [PLAYERS] of the lobby from id
    

    # Obtener todos los player de Lobby
    return True # Retornar los player de Lobbyy
"""
######

@db_session
def create_lobby(
                 lobbyIn_name: str,
                 lobbyIn_creator: int, #str,
                 lobbyIn_max_players: int, 
                 lobbyIn_min_players: int):
    #lobby1= dbe.Lobby(
    dbe.Lobby(
                lobby_name = lobbyIn_name, 
                lobby_creator = dbe.User[lobbyIn_creator].user_name, #lobbyIn_creator,
                lobby_max_players = lobbyIn_max_players, 
                lobby_min_players = lobbyIn_min_players,
    )
    #dbe.Lobby.select().show()
#    return lobby1

# class Lobby(db.Entity):
#     lobby_id                = PrimaryKey(int, auto = True)
#     lobby_name              = Required(str, unique=True)
#     lobby_max_players       = Optional(int, default = 10)   # <=10
#     lobby_min_players       = Optional(int, default = 5)   # >=5
#     lobby_creator           = Required(int)   # user_name or user_id of the creator
#     #lobby_user              = Set('UserPresence') #Set(User)         # many to many relation with Lobby-User, we use '' because Player is declarated after this call
#     lobby_players           = Set('Player')     # one to many relation with Lobby-Player, we use '' because Player is declarated after this call

# class LobbyIn2(BaseModel):  #La agregue yo (Agus)
#     creator: int
#     lobby_name: str
#     max_player: int = 10
#     min_players: int = 5


@db_session
def join_lobby(current_user: int, lobby_id: int): # Review
    """
    Add current_user from a Lobby
    """
    # Crear modelo para devolver en el return
    player1= dbe.Player(
                    player_lobby = dbe.Lobby[lobby_id],
                    player_user = dbe.User[current_user],
                    player_nick = dbe.User[current_user].user_name,
                    player_role = -1,
                    player_is_alive = True,
                    player_chat_blocked = False,
                    player_director = False,
                    player_minister = False
    )
    #dbe.Player.select().show()
    return player1


@db_session
def create_lobby2(lobby: md.LobbyIn2):
    print(" Creando Lobby... :(")
    new_lobby = dbe.Lobby(
                lobby_name = lobby.lobby_name,
                lobby_creator = lobby.creator,
                lobby_max_players = lobby.max_players, 
                lobby_min_players = lobby.min_players
    )
    print(" Lobby creado :D")
    owner = new_lobby.lobby_creator # OK

    #owner = dbe.Lobby[new_lobby.lobby_id].lobby_creator
    # Adding owner as player
    #join_lobby(owner, dbe.Lobby[new_lobby.lobby_id])
    print(" Joining Owner...")
    flush() # saves objects created by this moment in the database
    new_lobby_id= new_lobby.lobby_id
    join_lobby(owner, new_lobby_id)
    print(f"Creador = {dbe.User[owner].user_name}")


"""
@db_session
def check_user_presence_in_lobby(lobby_id: int, current_user: int):
    
    #Checks if a current_user is on the Lobby from id
    
    presence = dbe.UserPresence.get(dbe.User[current_user], dbe.Lobby[lobby_id])
    return presence
"""

## Terminar
@db_session
def leave_lobby(player_id: int):
    """
    Removes current_user from a Lobby by id
    """
    #lobby_select= dbe.Lobby[lobby_id] # Lobby
    #p= dbe.Player[current_user].player_lobby # Player
    print(f"Player {dbe.Player[player_id].player_nick} is leaving...")
    dbe.Player[player_id].delete()
    #print(f"Player {dbe.Player[player_id].player_nick} is leaving...")
    # player = select(player for pla)
    # dbe.Player[]
    # dbe.Player[current_user].player_lobby.delete()
    # return True
    

# Pasar jugadores al Game
@db_session
def join_game(current_player: int, game_id : int): # Final
    """
    Add current_player from a Game
    """
    g = dbe.Game[game_id] # Game
    dbe.Player[current_player].player_game = g


@db_session
def get_number_of_players(lobby_id : int):
    """
    Returns total player of the Lobby from id
    """
    total_players= 1
    l= dbe.Lobby[lobby_id] # Lobby
    total_players= l.lobby_players # ????
    return total_players


# player functions
@db_session
def createPlayer(playerModelObj: md.PlayerOut):
    """
    Creates a new Player
    """
    print(" Adding all players on the lobby")
    # p= 
    dbe.Player(player_game= 1,
    #player_lobby= Optional(Lobby)    # Depends on Lobby
    #player_id= Required(User)    # Depends on User
    #player_number= checkNumber(p), # Change checkNumber(p) from
    player_nick= playerModelObj.player_nick, 
    player_role= playerModelObj.player_role, 
    player_is_alive= playerModelObj.player_is_alive, 
    player_chat_blocked= playerModelObj.player_chat_blocked, 
    player_director= playerModelObj.player_director,
    player_minister= playerModelObj.player_minister)
    print("-> Player Added! ≧◉ᴥ◉≦\n")

# game functions
## Esto lo hacemos para ver como construir a partir de modelos, no necesariamente va a ser asi...
@db_session
def createGame(gameModelObj: md.ViewGame):
    """
    Creates a new Game
    """
    print(" Creating a new game from ViewGame...")
    g= dbe.Game(game_is_started= hf.startGame(), 
    game_total_players= gameModelObj.game_total_players,
    game_next_minister= gameModelObj.game_next_minister, 
    game_failed_elections= gameModelObj.game_failed_elections, 
    game_step_turn= gameModelObj.game_step_turn, 
    game_last_director= gameModelObj.game_last_director, 
    game_last_minister= gameModelObj.game_last_minister)
    createBoardFromGame(g)
    print("-> Game Added! ≧◉ᴥ◉≦\n")


@db_session
def add_proclamation_card_on_board(is_fenix: bool, game_id: int):
    """
    Add card proclamation a Board from game_id 
    """
    print("Adding a new proclamation card o board...\n")
    b = dbe.Game[game_id].game_board_game
    # is_fenix: True
    if is_fenix:
        print("Adding fenix ploclamation...")
        b.board_promulged_fenix = b.board_promulged_fenix + 1
    # is_fenix: False
    else:
        print("Adding death eater ploclamation...")
        b.board_promulged_death_eater = b.board_promulged_death_eater + 1
    print("-> Proclamation card added on board ≧◉ᴥ◉≦\n")


# board functions
@db_session
def createBoardFromGame(vGame: md.ViewGame): # Final, its ok
    print(" Creating a new board from game...")
    dbe.Board(board_game = vGame, 
    board_promulged_fenix= 0, 
    board_promulged_death_eater= 0, 
    board_deck_codification= hf.generate_new_deck(),
    board_is_spell_active= 0)
    print("-> Board Added ≧◉ᴥ◉≦")


#@db_session
#def deck_order(proclamed_fenix: int = 0, proclamed_death_eater: int = 0): # board_id: in    

@db_session
def get_board_information(): # For endpoint
    return True


@db_session
def getFirstCardFromDeck(deckTry: list):
    card = deckTry[0]
    # Remove the card
    removeCard(deckTry)
    # Proclamar
    return card


@db_session
def removeCard(deck_try: list):
    """
    Return a list of deck without first card
    """
    #print(" Removing a card...")
    # [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
    # Add the card at discardedCards
    # discardedCards(deck_try[0])
    # Remove the card
    deck_try.pop(0)
    #print("-> Card removed OK ≧◉ᴥ◉≦\n")
    return deck_try


"""@db_session
def discardedCards(card: int):
    #print(" Adding a card to descartes deck...")
    deck_descartes: list
    # Add a card to the end of the list
    deck_descartes.append()   
    #print("-> Discarded Cards OK ≧◉ᴥ◉≦\n")
    #return ... (devuelve las cartas descartadas)"""

# log functions

# Data
@db_session
def testFunc():
    print(dbe.Game[1])


@db_session
def showDatabase():
    print("---|Users|---")
    dbe.User.select().show()
    print("\n---|Lobbies|---")
    dbe.Lobby.select().show()
    print("\n---|Games|---(id, game_board_game, game_is_started, game_total_players, game_next_minister, game_failed_elections, game_step_turn, game_last_director, game_last_minister)")
    dbe.Game.select().show()
    print("\n---|Boards|---(id, board_game, board_promulged_fenix, board_promulged_death_eater, board_deck_codification, board_is_spell_active)")
    dbe.Board.select().show()
    print("\n---|Players|---(id, player_game, player_lobby, player_number, player_nick, player_role, player_is_alive, player_chat_blocked, player_director, player_minister)")
    dbe.Player.select().show()
