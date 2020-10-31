from pony.orm import db_session, select, count, flush
import db_entities_relations as dbe 
import models as md
import helpers_functions as hf
from typing import Optional
from datetime import datetime

##############################################################################################
##############################################################################################
######################################user functions##########################################
##############################################################################################
##############################################################################################


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
def insert_user(email: str, username: str, password: str,
                photo: Optional[str]):
    """
    Adds a new user to the database
    """
    if photo is None:
        photo = "https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/"
    
    dbe.User(
        user_email=email,
        user_name=username,
        user_password=password,
        user_photo=photo, 
        user_creation_dt=datetime.now())


##############################################################################################
##############################################################################################
######################################lobby functions#########################################
##############################################################################################
##############################################################################################


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
def get_lobby_by_id(id: int):
    """
    Returns a Lobby from ID
    """
    return dbe.Lobby.get(lobby_id=id)


@db_session
def get_lobby_by_player_id(player_id: int):
    """
    Returns [Lobby] by player_id
    """
    return dbe.Player[player_id].player_lobby
    #return dbe.Lobby.get(playerSet[player_id=player_id]))

@db_session
def is_player_lobby_owner(player_id : int, lobby_id : int)
    """
    Returns "True" if the player_id is a owner of lobby_id
    """
    current_player = dbe.Player[player_id]
    return current_player.player_lobby.lobby_id == lobby_id

@db_session
def get_players_lobby(lobby_id : int):
    """
    Get [PLAYERS] of the lobby from id
    """
    players = dbe.Lobby[lobby_id].lobby_players
    return [p for p in players]

@db_session
def join_lobby(current_user: int, lobby_id: int): # Review
    """
    Adds a user to a lobby. Creates (and returns) a player
    PRE : This does not check or return an error if user is 
    """
    player1 = dbe.Player(
                    player_lobby = dbe.Lobby[lobby_id],
                    player_user = dbe.User[current_user],
                    player_nick = dbe.User[current_user].user_name,
                    player_role = -1,
                    player_is_alive = True,
                    player_chat_blocked = False,
                    player_director = False,
                    player_minister = False
    )
    return player1 # Does it need a model?

@db_session
def create_lobby(lobby: md.LobbyIn): # Final, its ok
    """
    Creates a Lobby
    """
    print(" Creating Lobby... :(")
    new_lobby = dbe.Lobby(
                lobby_creator =     lobby.lobbyIn_creator,
                lobby_name =        lobby.lobbyIn_name,
                lobby_max_players = lobby.lobbyIn_max_players, 
                lobby_min_players = lobby.lobbyIn_min_players
    )
    print(" Lobby created :D")
    """
    owner = new_lobby.lobby_creator # OK
    # Adding owner as player
    print(" Joining Owner...")
    flush() # saves objects created by this moment in the database
    new_lobby_id= new_lobby.lobby_id
    join_lobby(owner, new_lobby_id)
    """
    print(f" Lobby Owner = {dbe.User[new_lobby.lobby_creator].user_name}")


@db_session
def is_user_in_lobby(user_id : int, lobby_id: int):
    """
    Return True is the user_id is on lobby_id
    """
    user = dbe.User[user_id]
    lobby = dbe.Lobby[lobby_id]
    return (user in lobby.lobby_players.player_user)


## Terminar
@db_session
def leave_lobby(player_id: int): # Final, its ok
    """
    Removes current_user from a Lobby by id
    """
    print(f"Player {dbe.Player[player_id].player_nick} is leaving...")
    dbe.Player[player_id].delete()
    

# Pasar jugadores al Game
@db_session
def join_game(current_player: int, game_id : int): # ¿Final?
    """
    Add current_player from a Game
    """
    g = dbe.Game[game_id] # Game
    dbe.Player[current_player].player_game = g


@db_session
def get_number_of_players(lobby_id : int): # Final, its ok
    """
    Returns total player of the Lobby from id
    """
    total_players= 0
    l= dbe.Lobby[lobby_id] # Lobby
    total_players= l.lobby_players
    return len(total_players)

##############################################################################################
##############################################################################################
#####################################player functions#########################################
##############################################################################################
##############################################################################################


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

##############################################################################################
##############################################################################################
#######################################game functions#########################################
##############################################################################################
##############################################################################################

# class ViewGame(BaseModel):
#     #game_board
#     game_is_started: bool = False               # Depends on Lobby
#     game_total_players : int                    # Depends on Lobby (<=10 a&& >=5)
#     game_next_minister: int = 0                 # Depends on player_number
#     game_failed_elections: int = 0              # = 0 <= 3 then reset to 0
#     game_step_turn:         int = -1                    # = -1 No asigned
#     game_last_director:     int = -1                # = -1 No asigned
#     game_last_minister:     int = -1                # = -1 No asigned


## Esto lo hacemos para ver como construir a partir de modelos, no necesariamente va a ser asi...
@db_session
def insert_game(gameModelObj: md.ViewGame, lobby_id: id): # Final, its ok
    """
    Creates a new Game
    """
    print(" Creating a new game from ViewGame...")
    g= dbe.Game(game_is_started= False, 
    game_total_players= gameModelObj.game_total_players,
    game_next_minister= gameModelObj.game_next_minister, 
    game_failed_elections= gameModelObj.game_failed_elections, 
    game_step_turn= gameModelObj.game_step_turn, 
    game_last_director= gameModelObj.game_last_director, 
    game_last_minister= gameModelObj.game_last_minister)
    createBoardFromGame(g)
    print("-> Game Added! ≧◉ᴥ◉≦\n")
    # Pass players to al Game
    players = get_players_lobby(lobby_id)
    for p in players:
        p.player_game = g
    # Delete Lobby
    dbe.Lobby[lobby_id].delete()
    # Select the roles of the players DIEGO >:DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD:<
    game = dbe.Game[game_id].game_players
    for players in game # next
    # Seleccionar el orden de los jugadores
    # Creo lobby A id= 1--> Creo Lobby B id=2--> Inicio Game B id=--> Inicio Game A
    #  
    # game_started == True
    hf.startGame()

@db_session
def add_proclamation_card_on_board(is_fenix: bool, game_id: int): # Final, its ok
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



##############################################################################################
##############################################################################################
######################################board functions#########################################
##############################################################################################
##############################################################################################


@db_session
def createBoardFromGame(vGame: md.ViewGame): # Final, its ok
    """
    Creates a Board from Game
    """
    print(" Creating a new board from game...")
    dbe.Board(board_game= vGame, 
    board_promulged_fenix= 0, 
    board_promulged_death_eater= 0, 
    board_deck_codification= hf.generate_new_deck(),
    board_is_spell_active= 0)
    print("-> Board Added ≧◉ᴥ◉≦")


#@db_session
#def deck_order(proclamed_fenix: int = 0, proclamed_death_eater: int = 0): # board_id: in    

@db_session
def get_board_information(): # For endpoint
    """
    
    """
    return True


@db_session
def getFirstCardFromDeck(deckTry: list):
    """
    Returns the first card of the deck
    """
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
    print(" Removing a card...")
    # [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
    # Add the card at discardedCards
    # discardedCards(deck_try[0])
    # Remove the card
    deck_try.pop(0)
    print("-> Card removed OK ≧◉ᴥ◉≦\n")
    return deck_try


"""@db_session
def discardedCards(card: int):
    #print(" Adding a card to descartes deck...")
    deck_descartes: list
    # Add a card to the end of the list
    deck_descartes.append()   
    #print("-> Discarded Cards OK ≧◉ᴥ◉≦\n")
    #return ... (devuelve las cartas descartadas)"""


##############################################################################################
##############################################################################################
######################################log functions#########################################
##############################################################################################
##############################################################################################

#@db_sesion
#def add():

##############################################################################################
##############################################################################################
######################################data functions#########################################
##############################################################################################
##############################################################################################
@db_session
def testFunc():
    print(dbe.Game[1])


@db_session
def showDatabase():
    """
    Shows database
    """
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
    #dbe.Log.select().show()
