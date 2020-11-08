from pony.orm import db_session, select, count, flush
import db_entities_relations as dbe 
import models as md
import helpers_functions as hf
from typing import Optional
from datetime import datetime
import random

##############################################################################################
######################################user functions##########################################
##############################################################################################


@db_session
def get_user_by_email(email):
    return dbe.User.get(user_email = email)


@db_session
def get_user_by_username(username):
    return dbe.User.get(user_name = username)


@db_session
def check_email_exists(new_email):
    return dbe.User.exists(user_email = new_email)


@db_session
def check_username_exists(new_uname):
    return dbe.User.exists(user_name = new_uname)


@db_session
def insert_user(email: str, username: str, password: str, photo: Optional[str]):
    """
    Adds a new user to the database
    """
    print(" Inserting User...")
    if photo is None:
        photo = "https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/"
    
    dbe.User(
        user_email = email,
        user_name = username,
        user_password = password,
        user_photo = photo, 
        user_creation_dt = datetime.now(),
        user_disabled = False
    )
    print(f" User {username} inserted")

##############################################################################################
######################################lobby functions#########################################
##############################################################################################


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


@db_session
def get_game_by_player_id(player_id: int):
    """
    Returns [Game] by player_id
    """
    return dbe.Player[player_id].player_game


@db_session
def get_players_lobby(lobby_id : int):
    """
    Get [PLAYERS] of the lobby from id
    """
    players = dbe.Lobby[lobby_id].lobby_players
    return [p for p in players]


@db_session
def get_players_game(game_id : int):
    """
    Get [PLAYERS] of the game from id
    """
    players = dbe.Game[game_id].game_players
    return [p for p in players]


@db_session
def get_lobbies_dict(start_from: int, end_at: int):
    lobbies = dbe.Lobby.select()
    lobbies_dict = dict()
    actual = 1
    for lobby in lobbies:
        if actual >= start_from:
            lobbies_dict[lobby.lobby_name] = lobby.lobby_id

        actual += 1
        if not (end_at is None):
            if actual > end_at:
                return lobbies_dict
    return lobbies_dict


@db_session
def get_number_of_players(lobby_id : int):
    """
    Returns total player of the Lobby from id
    """
    lobby = dbe.Lobby[lobby_id]
    return len(lobby.lobby_players)


@db_session
def get_player_id_from_lobby(user_id: int, lobby_id: int):
    """
    Returns a player_id from  lobby_id
    Returns 0 if the user_id doesn't have a player in the lobby_id
    """
    user_try = dbe.User[user_id].user_player
    for players in user_try:
        if (players.player_lobby.lobby_id == lobby_id):
            return players.player_id
    return 0


@db_session
def get_nick_points(player_id: int):
    return dbe.Player[player_id].player_nick_points


@db_session
def change_nick(player_id: int, new_nick: str):
    player = dbe.Player[player_id]
    player.player_nick = new_nick
    player.player_nick_points -= 1
    return player.player_nick_points


@db_session
def exist_lobby_name(lobbyIn_name):
    """
    Returns true if there is a lobby with that name
    """
    return dbe.Lobby.exists(lobby_name = lobbyIn_name)


@db_session
def check_max_players(lobbyIn_max_players):
    return not (5 <= lobbyIn_max_players <=10)


@db_session
def get_lobby_max_players(lobby_id: int):
    return dbe.Lobby[lobby_id].lobby_max_players


@db_session
def check_min_players(lobbyIn_min_players, lobbyIn_max_players):
    return not (5 <= lobbyIn_max_players <= lobbyIn_max_players <=10)


@db_session
def get_lobby_min_players(lobby_id: int):
    return dbe.Lobby[lobby_id].lobby_min_players


@db_session
def check_lobby_exists(lobby_id: int):
    for lobby in dbe.Lobby.select():
        if (lobby.lobby_id == lobby_id):
            return True
    return False


@db_session
def check_nick_exists(lobby_id: int, new_nick: str):
    lobby_players = dbe.Lobby[lobby_id].lobby_players
    for players in lobby_players:
        if (players.player_nick == new_nick):
            return True
    return False


@db_session
def is_player_lobby_owner(user_id : int, lobby_id : int):
    """
    Returns "True" if the player_id is a owner of lobby_id
    """
    current_lobby = dbe.Lobby[lobby_id]
    return current_lobby.lobby_creator == user_id


@db_session
def is_user_in_lobby(user_id : int, lobby_id: int):
    """
    Return True is the user_id is on lobby_id
    False if it does not find it 
    """
    user = dbe.User[user_id]
    lobby = dbe.Lobby[lobby_id]
    return (user in lobby.lobby_players.player_user)


@db_session
def create_lobby(
                lobbyIn_name: str,
                lobbyIn_creator: int,
                lobbyIn_max_players: int, 
                lobbyIn_min_players: int):

    lobby1 = dbe.Lobby(
                lobby_name = lobbyIn_name, 
                lobby_creator = dbe.User[lobbyIn_creator].user_id,
                lobby_max_players = lobbyIn_max_players, 
                lobby_min_players = lobbyIn_min_players
    )
    dbe.Lobby.select().show()
    return lobby1


@db_session
def join_lobby(current_user: int, lobby_id: int):
    """
    Adds a user to a lobby. Creates (and returns) a player
    """
    dbe.Player(
        player_user = dbe.User[current_user],
        player_lobby = dbe.Lobby[lobby_id],
        player_nick = dbe.User[current_user].user_name,
        player_nick_points = 10,
        player_role = -1,
        player_is_alive = True,
        player_chat_blocked = False,
        player_director = False,
        player_minister = False
    )
    return  dbe.Lobby[lobby_id].lobby_name


@db_session
def leave_lobby(player_id: int):
    """
    Removes current_user from a Lobby by id
    """
    print(f"Player {dbe.Player[player_id].player_nick} is leaving...")
    dbe.Player[player_id].delete()
    print("Player has left the lobby")

@db_session
def join_game(current_player: int, game_id : int):
    """
    Add current_player from a Game
    """
    game = dbe.Game[game_id]
    dbe.Player[current_player].player_game = game

##############################################################################################
#####################################player functions#########################################
##############################################################################################


@db_session
def createPlayer(playerModelObj: md.PlayerOut):
    """
    Creates a new Player
    """
    print(" Adding all players on the lobby")
    dbe.Player(
        player_game = 1,
        player_nick = playerModelObj.player_nick, 
        player_role = playerModelObj.player_role, 
        player_is_alive = playerModelObj.player_is_alive, 
        player_chat_blocked = playerModelObj.player_chat_blocked, 
        player_director = playerModelObj.player_director,
        player_minister = playerModelObj.player_minister
    )
    print("-> Player Added! ≧◉ᴥ◉≦\n")

##############################################################################################
#######################################game functions#########################################
##############################################################################################


@db_session
def get_player_id_from_game(user_id: int, game_id: int):
    """
    Returns a player_id from game_id
    
    Returns 0 if the user_id doesn't have a player in the game_id
    """
    # Queremos el player_id desde los parámetros...
    player_try = dbe.Game[game_id].game_players # PlayerSet([Players])
    for player in player_try:
        if (player.player_user.user_id == user_id):
            return player.player_id
    return 0


@db_session
def get_player_id_by_player_number(player_numbers: int, game_id: int): # Final its ok
    """
    Returns player_id from player_number (order)
    
    If returns "get_player_id_by_player_number" --> Error 0
    """
    select_player_game= dbe.Game[game_id].game_players # [Players]
    for p in select_player_game:            
        if (p.player_number == player_numbers):
            return p.player_id
    return 0


@db_session
def get_player_number_by_player_id(player_id: int):
    return dbe.Player[player_id].player_number
    

@db_session
def get_player_nick_by_id(player_id: int):
    """
    Returns player_nick by player_id
    """
    return dbe.Player[player_id].player_nick


@db_session
def get_game_total_players(game_id: int):
    """
    Returns total players by game
    """
    return dbe.Game[game_id].game_total_players


@db_session
def is_user_in_game(user_id: int, game_id:int):
    user = dbe.User[user_id]
    game_players = dbe.Game[game_id].game_players
    return (user in game_players.player_user)


@db_session
def is_player_director(player_id: int):
    return dbe.Player[player_id].player_director


@db_session
def is_player_minister(player_id: int):
    """
    Checks if the player says its the minister
    """
    return dbe.Player[player_id].player_minister

#! FIXME
@db_session
def is_player_last_minister(player_id: int, game_id: int):
    """
    Checks if the Game says "player" its the last minister
    """
    player_number = get_player_number_by_player_id(player_id)
    return dbe.Game[game_id].game_last_minister == player_number


@db_session
def is_player_next_minister(player_id: int, game_id: int):
    """
    Checks if the Game says "player" its the next minister
    """
    player_number = get_player_number_by_player_id(player_id)
    return dbe.Game[game_id].game_actual_minister == player_number
#! End FixMe

@db_session
def is_player_alive(player_id: int):
    """
    Returns True if the players is alive

    False if the player is death
    """
    return (dbe.Player[player_id].player_is_alive)


# Check functions
@db_session
def can_player_be_director(player_number: int, game_id: int):
    """
    Returns True if the player is avaliable to be director on the game

    False if the player is not avaliable to be director on the game
    """
    prec1 = dbe.Game[game_id].game_last_director == player_number 
    prec2 = dbe.Game[game_id].game_last_minister == player_number
    prec3 = dbe.Game[game_id].game_actual_minister == player_number
    return (prec1 or prec2 or prec3)
    
@db_session
def insert_game(gameModelObj: md.ViewGame, lobby_id: id):
    """
    Creates a new Game
    """
    print(" Creating a new game from ViewGame...")
    game = dbe.Game(
              game_is_started = False, 
              game_total_players = gameModelObj.game_total_players,
              game_actual_minister = gameModelObj.game_actual_minister, 
              game_failed_elections = gameModelObj.game_failed_elections, 
              game_step_turn = gameModelObj.game_step_turn, 
              game_last_director = gameModelObj.game_last_director, 
              game_last_minister = gameModelObj.game_last_minister
    )
    createBoardFromGame(game)
    print("-> Game Added! ≧◉ᴥ◉≦\n")
    
    # Pass players to al Game
    players = get_players_lobby(lobby_id)
    for p in players:
        p.player_game = game
    # Delete Lobby
    delete_lobby(lobby_id)
    #dbe.Lobby[lobby_id].delete()
    flush()
    game_p = dbe.Game[game.game_id].game_players
    amount_of_players = len(game_p)
    print(amount_of_players)

    # Select roles of the players
    print("\n ------")
    select_roles(game.game_total_players, game_p) ## select_roles(game_total_players, game_p)
    
    # Select orders of the players
    select_orders(game_p, amount_of_players, game.game_id) ## select_orders(game_total_players, game_p)
    print(" Starting a new game...")
    game.game_is_started = True
    print("-> Game Started! ≧◉ᴥ◉≦")
    

@db_session
def delete_lobby(lobby_id:int):
    """
    Deletes a Lobby from lobby_id
    """
    dbe.Lobby[lobby_id].delete()
    

@db_session # Review
def select_roles(game_total_players: int, game_p: set):
    """
    Selectes role of player
    
    role: 0 Phoenix, 1 DeathEater, 2 Voldemort
    """
    print("\n select_roles()")    
    if (game_total_players == 5):   # 5 players: three phoenix(0), one death eater(1) and voldemort(2)
        print("\n Game total players: 5")
        roles = [0, 0, 0, 1, 2]
    elif (game_total_players == 6): # 6 players: four phoenix(0), one death eater(1) and volvemort(2)
        print("\n Game total players: 6")
        roles = [0, 0, 0, 0, 1, 2]
    elif (game_total_players == 7): # 7 players: four phoenix(0), two death eater(1) and voldemort(2)
        print("\n Game total players: 7")
        roles = [0, 0, 0, 0, 1, 1, 2]
    elif (game_total_players == 8): # 8 players: five phoenix(0), two death eater(1) and voldemort(2)
        print("\n Game total players: 8")
        roles = [0, 0, 0, 0, 0, 1, 1, 2]
    elif (game_total_players == 9): # 9 players: five phoenix(0), three death eater(1) and voldemort(2)
        print("\n Game total players: 9")
        roles = [0, 0, 0, 0, 0, 1, 1, 1, 2]
    elif (game_total_players == 10): # 10 players: six phoenix(0), three death eater(1) and voldemort(2)
        print("\n Game total players: 10")
        roles = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2]
    else: # Debuger
        raise ValueError(" Error: Bad call. List of players should be between 5 and 10 >:C")
        
    random.shuffle(roles) # Asigned random order
    index = 0
    for player in game_p: # player[0] ... player[4]
        player.player_role = roles[index]
        index = index + 1

    print("\n select_roles() OK")
    

@db_session
def select_orders(game_players: set, total_players: int, game_id: int):
    """
    Selects the in game order of players
    """
    print("\n select_orders()...")
    print(f"\n Game total players: {total_players}")

    list_players = list(range(total_players))

    random.shuffle(list_players)
    for p in game_players:
        p.player_number = list_players[0]
        list_players.pop(0)
        if (p.player_number == 0):
            # Selects a player as minister
            p.player_minister = True
            # Change on db            
            dbe.Game[game_id].game_last_minister = -1 # Joker= True 0
            dbe.Game[game_id].game_actual_minister = 0 # Who is the next minister for the turn
    print("\n Order has been set")


@db_session
def select_director(player_id: int, player_number: int, game_id: int):
    """
    Change on db of the Game the last director
    """
    print("\n select_director() in")
    # Old director
    player_number_old_director = dbe.Game[game_id].game_last_director
    if not (player_number_old_director == -1): # All turns except the 1st
        player_id_old_director = get_player_id_by_player_number(player_number_old_director, game_id)
        dbe.Player[player_id_old_director].player_director = False    
        
    # New director
    dbe.Game[game_id].game_last_director = player_number
    dbe.Player[player_id].player_director = True
    
    
# REVIEW Set_next_minister adapted to Avada Kedavra
@db_session
def set_next_minister(game_id: int):
    """
    Called at the end of every turn. Changes next minister with number order
    
    Only valid for the cases: -A proclamation has been posted correctly (Except Avada Kedavra)
    - Avada Kedavra

    Not Valid for the cases: - Director votation was not aproved
    - Spell Imperius
    """
    game_total_players = get_game_total_players(game_id)

        # Old minister
    actual_minister = dbe.Game[game_id].game_actual_minister

    player_number_old_minister = dbe.Game[game_id].game_last_minister
    
    player_id_old_minister = get_player_id_by_player_number(actual_minister, game_id)
    dbe.Player[player_id_old_minister].player_minister = False 
    dbe.Game[game_id].game_last_minister = actual_minister                      # Save actual minister to last minister

    # New actual_minister
    dbe.Game[game_id].game_actual_minister += 1
    if ((dbe.Game[game_id].game_actual_minister) >= (game_total_players)): # Reset 
            dbe.Game[game_id].game_actual_minister = 0

    actual_minister = dbe.Game[game_id].game_actual_minister
    
    actual_minister_id = get_player_id_by_player_number(actual_minister, game_id)
    while not (is_player_alive(actual_minister_id)): # Checks if the Player by player_id is alive
        dbe.Game[game_id].game_actual_minister += 1 # OK

        if ((dbe.Game[game_id].game_actual_minister) >= (game_total_players)): # Reset    
            dbe.Game[game_id].game_actual_minister = 0

        actual_minister = dbe.Game[game_id].game_actual_minister

        actual_minister_id = get_player_id_by_player_number(actual_minister, game_id) 
        
    dbe.Player[actual_minister_id].player_minister = True



@db_session
def add_proclamation_card_on_board(is_phoenix: bool, game_id: int):
    """
    Add card proclamation a Board from game_id 
    """
    print(" Adding a new proclamation card o board...\n")
    b = dbe.Game[game_id].game_board
    # is_fenix: True
    if is_phoenix:
        print(" Adding fenix ploclamation...")
        b.board_promulged_fenix = b.board_promulged_fenix + 1
    # is_fenix: False
    else:
        print(" Adding death eater ploclamation...")
        b.board_promulged_death_eater = b.board_promulged_death_eater + 1
    print("-> Proclamation card added on board ≧◉ᴥ◉≦\n")
    return (b.board_promulged_fenix, b.board_promulged_death_eater)


@db_session
def get_death_eaters_proclamations(game_id: int):
    """
    Gets the exact amount of proclamations posted by death eaters team
    """
    game_board = dbe.Game[game_id].game_board
    return game_board.board_promulged_death_eater


@db_session
def kill_player(player_id: int):
    dbe.Player[player_id].player_is_alive = False


##############################################################################################
######################################board functions#########################################
##############################################################################################


@db_session
def get_board_information(): # For endpoint
    """
    
    """
    return True


@db_session
def get_three_cards(game_id: int): # For endpoint
    """
    Returns the three first cards of the deck
    """
    coded_game_deck = dbe.Game[game_id].game_board.board_deck_codification
    decoded_game_deck = hf.decode_deck(coded_game_deck)
    prophecy_cards = md.Prophecy(
                    prophecy_card_0 = decoded_game_deck[0],
                    prophecy_card_1 = decoded_game_deck[1],
                    prophecy_card_2 = decoded_game_deck[2])
    return prophecy_cards


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
def createBoardFromGame(vGame: md.ViewGame):
    """
    Creates a Board from Game
    """
    print(" Creating a new board from game...")
    dbe.Board(
        board_game = vGame, 
        board_promulged_fenix = 0, 
        board_promulged_death_eater = 0, 
        board_deck_codification = hf.generate_new_deck()
    )
    print("-> Board Added ≧◉ᴥ◉≦")


#@db_session
#def deck_order(proclamed_fenix: int = 0, proclamed_death_eater: int = 0): # board_id: in    


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
######################################log functions#########################################
##############################################################################################


#@db_sesion
#def add():


##############################################################################################
######################################test functions#########################################
##############################################################################################


@db_session
def testFunc():
    print(dbe.Game[1])


@db_session
def showDatabase(): # NO TOCAR
    """
    Shows database
    """
    print("---|Users|---\n(user_id, user_email, user_name, user_password, user_photo, user_creation_dt, user_lobby, user_player, user_log, user_defau)")
    dbe.User.select().show()
    
    print("\n---|Lobbies|---\n(lobby_id, lobby_name, lobby_max_players, lobby_min_players, lobby_creator, lobby_user, lobby_players)")
    dbe.Lobby.select().show()
    
    print("\n---|Players|---\n(player_id, player_number, player_nick, player_nick_amount, player_role, player_is_alive, player_chat_blocked, player_director, player_minister, player_game, player_lobby, player_user)")
    dbe.Player.select().show()
    
    print("\n---|Games|---\n(game_id, game_is_started, game_total_players, game_actual_minister, game_failed_elections, game_step_turn, game_last_director, game_last_minister, game_board)")
    dbe.Game.select().show()
    
    print("\n---|Boards|---\n(id, board_game, board_promulged_fenix, board_promulged_death_eater, board_deck_codification)")
    dbe.Board.select().show()
    #....show() board_game
    print("\n")
    #dbe.Log.select().show()