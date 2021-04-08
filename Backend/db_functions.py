from pony.orm import db_session, select, count, flush
import db_entities_relations as dbe 
import models as md
import helpers_functions as hf
from typing import Optional
from datetime import datetime
import random
import json

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
def get_user_by_id(id: int):
    return dbe.User.get(user_id = id)


@db_session
def get_user_id_by_player_id(player_id: int):
    return dbe.Player[player_id].player_user.user_id


@db_session
def get_user_by_player_id(player_id: int):
    return dbe.Player[player_id].player_user


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
    
    user = dbe.User(
                    user_email = email,
                    user_name = username,
                    user_password = password,
                    user_photo = photo, 
                    user_creation_dt = datetime.now(),
                    user_disabled = False,
                    user_default_icon_id = random.randint(0,28),
                    user_house = random.randint(0,3)
                    )
    flush()
    create_log(user)
    print(f" User {username} inserted")


@db_session
def update_user_profile(user_id: int, username: str, photo: str):
    if username is not None:
        dbe.User[user_id].user_name = username
    if photo is not None:
        dbe.User[user_id].user_photo = photo


@db_session
def change_password_user(user_id: int, password: str):
    dbe.User[user_id].user_password = password


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
def get_players_id_playing_with_player_id(player_id: int):
    """
    Returns [player_id] of players sharing the same lobby or game with player_id
    """
    player = dbe.Player[player_id]
    if (player.player_lobby != None):
        players = player.player_lobby.lobby_players
    else:
        players = player.player_game.game_players
    player_ids = [p.player_id for p in players]
    player_ids.remove(player_id)
    return player_ids


@db_session
def get_lobbies_dict(start_from: int, end_at: int):
    lobbies = dbe.Lobby.select()
    lobbies_dict = dict()
    actual = 1
    for lobby in lobbies:
        if actual >= start_from:
            lobby_creator = get_player_from_lobby(lobby.lobby_creator, lobby.lobby_id).player_nick
            lobby_dict= {
                "lobby_id": lobby.lobby_id,
                "min players": lobby.lobby_min_players, 
                "max players": lobby.lobby_max_players,
                "actual players": len(lobby.lobby_players),
                "lobby_creator": lobby_creator
            }
            lobbies_dict[lobby.lobby_name] = lobby_dict

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
def get_player_from_lobby(user_id: int, lobby_id: int):
    players_in_lobby = dbe.Lobby[lobby_id].lobby_players
    for player in players_in_lobby:
        if (player.player_user.user_id == user_id):
            return player
    return None


@db_session
def get_player_id_from_lobby(user_id: int, lobby_id: int):
    """
    Returns a player_id from  lobby_id
    Returns 0 if the user_id doesn't have a player in the lobby_id
    """
    user_players = dbe.User[user_id].user_player
    for player in user_players:
        try:
            this_lobby_id = player.player_lobby.lobby_id
        except AttributeError:
            continue 
        if (this_lobby_id == lobby_id):
            return player.player_id
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
def exist_lobby_name(lobbyIn_name: str):
    """
    Returns true if there is a lobby with that name
    """
    return dbe.Lobby.exists(lobby_name = lobbyIn_name)


@db_session
def check_max_players(lobbyIn_max_players: int):
    return not (5 <= lobbyIn_max_players <=10)


@db_session
def get_lobby_max_players(lobby_id: int):
    return dbe.Lobby[lobby_id].lobby_max_players


@db_session
def check_min_players(lobbyIn_min_players: int, lobbyIn_max_players: int):
    return not (5 <= lobbyIn_min_players <= lobbyIn_max_players <=10)


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
        player_is_candidate = False,
        player_has_voted = False, # True if the player has voted
        player_vote = False, # Actual vote
        player_director = False,
        player_minister = False
    )
    return  dbe.Lobby[lobby_id]


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


@db_session
def get_player_nicks_from_lobby(lobby_id: int):
    lobby = dbe.Lobby[lobby_id]
    return [p.player_nick for p in lobby.lobby_players]


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
        player_is_candidate = playerModelObj.player_is_candidate,
        player_has_voted = playerModelObj.player_has_voted,
        player_vote = playerModelObj.player_vote,
        player_director = playerModelObj.player_director,
        player_minister = playerModelObj.player_minister
    )
    print("-> Player Added! ≧◉ᴥ◉≦\n")


@db_session
def get_player_role(player_id: int):
    return dbe.Player[player_id].player_role


##############################################################################################
#######################################game functions#########################################
##############################################################################################


@db_session
def get_player_number_crucio(game_id: int):
    return dbe.Game[game_id].game_crucio


@db_session
def activate_crucio(victim_number: int, game_id: int):
    dbe.Game[game_id].game_crucio = victim_number


@db_session
def get_roles(game_id: int):
    players = dbe.Game[game_id].game_players
    roles_dict = dict()
    for player in players:
        player_nick = player.player_nick
        player_role = player.player_role
        roles_dict[player_nick] = player_role
    return roles_dict


@db_session
def get_games_dict(start_from: int, end_at: int, user_id: int):
    """
    Returns games of the user
    """
    set_player= dbe.User[user_id].user_player
    games= [player.player_game for player in set_player]
    games_dict = dict()
    actual = 1
    for game in games:
        if game == None:
            continue
        if actual >= start_from:
            current_player_id= get_player_id_from_game(user_id, game.game_id)
            g_player= dbe.Player[current_player_id]
            use_dict= {
                "total players": game.game_total_players, 
                "nick": g_player.player_nick,
                "role": g_player.player_role, 
                "is_alive": g_player.player_is_alive
            }
            games_dict[game.game_id] = use_dict

        actual += 1
        if not (end_at is None):
            if actual > end_at:
                return games_dict
    return games_dict


@db_session
def get_relative_game_information(user_id: int, game_id: int):
    current_player = get_player_from_game(user_id, game_id)
    current_game = dbe.Game[game_id]
    players = current_game.game_players
    playersDict = {}
    relative_roles = get_roles_relative_to_player(current_player.player_id, game_id)
    for player in players:
        playersDict[player.player_nick] = {
            "nick" : player.player_nick,
            "player_number" : player.player_number,
            "connected": None,
            "role": relative_roles[player.player_nick],
            "is_alive": player.player_is_alive,
            "is_candidate": player.player_is_candidate,
            "has_voted": player.player_has_voted,
            "vote": player.player_vote,
            "icon": player.player_user.user_default_icon_id,
            "house": player.player_user.user_house
        }
    
    strmessage = current_player.player_last_message
    if(strmessage != ''):
        last_message= json.loads()
    else:
        last_message= {}

    returnDict = {
        "game_id": game_id,
        "game_step_turn": current_game.game_step_turn,
        "player_id": current_player.player_id,
        "player_nick": current_player.player_nick,
        "chat_blocked": current_player.player_chat_blocked,
        "current_minister": current_game.game_actual_minister,
        "current_director": current_game.game_candidate_director,
        "player_array": playersDict,
        "election_counter": current_game.game_failed_elections,
        "cards_in_deck": len(hf.decode_deck(get_coded_deck(game_id))),
        "proclaimed_phoenix": current_game.game_board.board_promulged_fenix,
        "proclaimed_death_eater": current_game.game_board.board_promulged_death_eater,
        "last_message":  last_message
    }

    return returnDict


@db_session
def get_dead_players(game_id: int):
    players_in_game= dbe.Game[game_id].game_players
    total_dead= 0
    for player in players_in_game:
        if(player.player_is_alive == False):
            total_dead += 1
    return total_dead


@db_session
def get_player_from_game(user_id: int, game_id: int):
    players_in_game = dbe.Game[game_id].game_players
    for player in players_in_game:
        if (player.player_user.user_id == user_id):
            return player
    return None


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
def get_player_id_by_player_number(player_number: int, game_id: int):
    """
    Returns player_id from player_number (order)
    
    If returns "get_player_id_by_player_number" --> Error 0
    """
    select_player_game= dbe.Game[game_id].game_players # [Players]
    for p in select_player_game:            
        if (p.player_number == player_number):
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
def is_expeliarmus_active(game_id: int):
    return dbe.Game[game_id].game_expeliarmus


@db_session
def is_imperius_active(game_id: int):
    return dbe.Game[game_id].game_imperius


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


@db_session
def is_player_alive(player_id: int):
    """
    Returns True if the players is alive

    False if the player is dead
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
def can_player_be_director_v2(player_id: int):
    game = dbe.Player[player_id].player_game
    player_number = dbe.Player[player_id].player_number
    prec1 = game.game_last_director == player_number 
    prec2 = game.game_last_minister == player_number
    prec3 = game.game_actual_minister == player_number
    return not (prec1 or prec2 or prec3)


@db_session
def get_actual_minister(game_id):
    """
    Returns actual minister's player number
    """
    if (is_imperius_active(game_id) == -1):
        actual_minister = dbe.Game[game_id].game_actual_minister
    else:
        actual_minister = is_imperius_active(game_id)
    return actual_minister


@db_session
def get_actual_director(game_id):
    """
    Returns actual directors's player number from players
    """
    players = dbe.Game[game_id].game_players
    for player in players:
        if (player.player_director == True):
            return player.player_number

        
@db_session
def check_game_exists(game_id: int):
    for game in dbe.Game.select():
        if (game.game_id == game_id):
            return True
    return False


@db_session
def activate_expeliarmus(game_id: int):
    dbe.Game[game_id].game_expeliarmus = 1


@db_session
def deactivate_expeliarmus(game_id: int):
    dbe.Game[game_id].game_expeliarmus = 0


@db_session
def rejected_expeliarmus(game_id: int):
    dbe.Game[game_id].game_expeliarmus = 2
    dbe.Game[game_id].game_failed_elections += 1


@db_session
def activate_imperius(victim_number: int, game_id: int):
    dbe.Game[game_id].game_imperius = victim_number


@db_session
def deactivate_imperius(game_id: int):
    dbe.Game[game_id].game_imperius = -1


@db_session
def finish_imperius(game_id: int):
    imperius_minister = is_imperius_active(game_id)
    imperius_minister_id = get_player_id_by_player_number(imperius_minister, game_id)
    deactivate_imperius(game_id)
    dbe.Player[imperius_minister_id].player_minister = False


@db_session
def insert_game(gameModelObj: md.ViewGame, lobby_id: id) -> int:
    """
    Creates a new Game
    """
    print(" Creating a new game from ViewGame...")
    game = dbe.Game(
              game_is_started = False, 
              game_imperius = gameModelObj.game_imperius,
              game_expeliarmus = gameModelObj.game_expeliarmus,
              game_total_players = gameModelObj.game_total_players,
              game_actual_minister = gameModelObj.game_actual_minister, 
              game_failed_elections = gameModelObj.game_failed_elections, 
              game_step_turn = gameModelObj.game_step_turn,
              game_candidate_director = gameModelObj.game_candidate_director,
              game_votes = gameModelObj.game_votes,
              game_status_vote = gameModelObj.game_status_vote,
              game_crucio = gameModelObj.game_crucio,
              game_last_director = gameModelObj.game_last_director, 
              game_last_minister = gameModelObj.game_last_minister,
              game_last_proclamation =gameModelObj.game_last_proclamation
    )
    createBoardFromGame(game)
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

    # Select roles of the players
    select_roles(game.game_total_players, game_p) ## select_roles(game_total_players, game_p)
    
    # Select orders of the players
    select_orders(game_p, amount_of_players, game.game_id) ## select_orders(game_total_players, game_p)
    print(" Starting a new game...")
    game.game_is_started = True
    print("-> Game Started! ≧◉ᴥ◉≦")
    return game.game_id
    

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
    print("\n Selecting roles...")    
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
    

@db_session
def select_orders(game_players: set, total_players: int, game_id: int):
    """
    Selects the in game order of players
    """
    print("\n Selecting order...")
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
    print("\n -> Order has been set\n")

@db_session
def get_roles_relative_to_player(player_id: int, game_id : int):
    """
    Returns [ {PLAYER_NICK : ROLE} ] according to what the game would reveal to player_id
    """    
    current_player = dbe.Player[player_id]
    current_nick = current_player.player_nick
    players = get_players_game(game_id)
    roles = {}
    is_phoenix = current_player.player_role == 0
    is_death_eater = current_player.player_role == 1
    is_voldemort = current_player.player_role == 2
    if (is_phoenix or (is_voldemort and len(players) > 6)):
        for player in players:
            nick = player.player_nick
            roles[player.player_nick] = player.player_role if (nick == current_nick) else -1 #* -1 Means Unknown

    elif (is_death_eater or (is_voldemort and len(players) < 7)):
        for player in players:
            roles[player.player_nick] = player.player_role
    else:
        raise ValueError(f"Error in get_roles_relative_to_player called with player_id={player_id} and game_id={game_id}")
    
    return roles


@db_session
def get_game_step_turn(game_id: int):
    return dbe.Game[game_id].game_step_turn


@db_session
def set_game_step_turn(step_turn: str, game_id: int):
    """
    step_turn: START_GAME, START_TURN, SELECT_CANDIDATE_ENDED, VOTATION_ENDED_OK, VOTATION_ENDED_NO, DISCARD_ENDED, POST_PROCLAMATION_ENDED
    
    if the step_turn are not correct, the function don't change the db
    """
    if(step_turn == "START_GAME" or 
        step_turn == "START_TURN" or 
        step_turn == "SELECT_CANDIDATE_ENDED" or 
        step_turn == "VOTATION_ENDED_OK" or
        step_turn == "VOTATION_ENDED_NO" or
        step_turn == "DISCARD_ENDED" or
        step_turn == "POST_PROCLAMATION_ENDED" or
        step_turn == "SPELL"):
        dbe.Game[game_id].game_step_turn = step_turn
    else:
        print(f" step_turn was not successfully set")


@db_session
def set_last_proclamation(last_proclamation: int, game_id: int):
    dbe.Game[game_id].game_last_proclamation = last_proclamation


@db_session
def get_last_proclamation(game_id: int):
    return dbe.Game[game_id].game_last_proclamation


@db_session
def get_spell(game_id: int):
    """
    Returns "No Spell" if there are not spells that should be called actually
    Returns "Crucio" if the spell that should be called is "Crucio"
    Returns "Imperius" if the spell that should be called is "Imperius"
    Returns "Prophecy" if the spell that should be called is "Prophecy"
    Returns "Avada Kedavra" if the spell that should be called is "Avada Kedavra"
    """
    game = dbe.Game[game_id]
    death_eater_proclamations = game.game_board.board_promulged_death_eater
    total_players = game.game_total_players
    if (9 <= total_players <= 10):
        if (death_eater_proclamations == 0):
            return "No Spell"
        if (1 <= death_eater_proclamations <= 2):
            return "Crucio"
        if (death_eater_proclamations == 3):
            return "Imperius"
        if (4 <= death_eater_proclamations <= 5):
            return "Avada Kedavra"
    if (7 <= total_players <= 8):
        if (0 <= death_eater_proclamations <= 1):
            return "No Spell"
        if (death_eater_proclamations == 2):
            return "Crucio"
        if (death_eater_proclamations == 3):
            return "Imperius"
        if (4 <= death_eater_proclamations <= 5):
            return "Avada Kedavra"
    if (5 <= total_players <= 6):
        if (0 <= death_eater_proclamations <= 2):
            return "No Spell"
        if (death_eater_proclamations == 3):
            return "Prophecy"
        if (4 <= death_eater_proclamations <= 5):
            return "Avada Kedavra"

@db_session
def select_candidate(player_id: int, player_number: int, game_id: int):
    """
    Change on db of the Game the candidate_director
    """
    dbe.Game[game_id].game_candidate_director = player_number
    dbe.Player[player_id].player_is_candidate = True


@db_session
def get_game_candidate_director(game_id: int):
    return dbe.Game[game_id].game_candidate_director


@db_session
def get_game_last_minister(game_id: int):
    return dbe.Game[game_id].game_last_minister


@db_session
def check_has_voted(player_id: int):
    return dbe.Player[player_id].player_has_voted


@db_session
def get_actual_vote_of_player(player_id: int):
    return dbe.Player[player_id].player_vote


@db_session
def set_has_voted(player_id: int):
    dbe.Player[player_id].player_has_voted = True


@db_session
def set_vote(player_id: int, state: bool):
    """
    Set vote of the player
    """
    dbe.Player[player_id].player_vote = state


@db_session
def player_vote(vote: bool, player_id: int, game_id: int):
    print(f" Player {dbe.Player[player_id].player_nick} has vote {vote}")
    if(vote):
        dbe.Game[game_id].game_status_vote += 1 # Status vote
    else:
        dbe.Game[game_id].game_status_vote -= 1 # Status vote
    set_vote(player_id, vote) # Set actual vote on db
    set_has_voted(player_id)
    dbe.Game[game_id].game_votes += 1 
    return dbe.Game[game_id].game_votes # Count if the player has voted on db
    

@db_session
def get_status_vote(game_id: int):
    return dbe.Game[game_id].game_status_vote


@db_session
def select_director(player_id: int, player_number: int, game_id: int):
    """
    Change on db of the Game the last director
    """
    # Old director
    player_number_old_director = dbe.Game[game_id].game_last_director
    if not (player_number_old_director == -1): # All turns except the 1st
        player_id_old_director = get_player_id_by_player_number(player_number_old_director, game_id)
        dbe.Player[player_id_old_director].player_director = False    
        
    # New director
    dbe.Game[game_id].game_last_director = player_number
    dbe.Player[player_id].player_director = True
    dbe.Player[player_id].player_is_candidate = False


@db_session
def clean_director(player_id: int, game_id: int):
    dbe.Game[game_id].game_last_director = -1
    dbe.Player[player_id].player_director = False
    dbe.Player[player_id].player_is_candidate = False


# @db_session #! REVIEW
# def reset_candidate_fail_election(player_id: int, game_id: int):
#     actual_minister = dbe.Game[game_id].game_last_minister
#     dbe.Game[game_id].game_last_minister = actual_minister + 1 
#     dbe.Game[game_id].game_candidate_director = -1
#     dbe.Player[player_id].player_is_candidate = False

    
@db_session
def set_next_minister_failed_election(game_id: int):
    """
    Called when the election has failed
    """
    game_total_players= get_game_total_players(game_id)

   # Old minister
    actual_minister = dbe.Game[game_id].game_actual_minister

    id_actual_minister = get_player_id_by_player_number(actual_minister, game_id)
    dbe.Player[id_actual_minister].player_minister = False # The old Minister now is not the Minister
    
    # New actual_minister
    dbe.Game[game_id].game_actual_minister += 1
    if ((dbe.Game[game_id].game_actual_minister) >= (game_total_players)): # Reset 
        dbe.Game[game_id].game_actual_minister = 0

    actual_minister = dbe.Game[game_id].game_actual_minister # Get the new Minister
    actual_minister_id = get_player_id_by_player_number(actual_minister, game_id)

    while not (is_player_alive(actual_minister_id)): # Checks if the Player who is Minister is alive
        dbe.Game[game_id].game_actual_minister += 1 # OK

        if ((dbe.Game[game_id].game_actual_minister) >= (game_total_players)): # Reset    
            dbe.Game[game_id].game_actual_minister = 0

        actual_minister = dbe.Game[game_id].game_actual_minister
        actual_minister_id = get_player_id_by_player_number(actual_minister, game_id) 
        
    dbe.Player[actual_minister_id].player_minister = True


@db_session
def set_next_minister_imperius(victim_number: int, game_id: int):

    """
    Called when Imperius become active
    """
   # Old minister
    actual_minister = dbe.Game[game_id].game_actual_minister

    id_actual_minister = get_player_id_by_player_number(actual_minister, game_id)
    dbe.Player[id_actual_minister].player_minister = False # The old Minister now is not the Minister
    
    dbe.Game[game_id].game_last_minister = actual_minister # Save actual minister to last minister
    
    # New actual_minister
    actual_minister = victim_number # Get the new Minister
    actual_minister_id = get_player_id_by_player_number(actual_minister, game_id)
        
    dbe.Player[actual_minister_id].player_minister = True # Game does not know who the new minister is



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

    id_actual_minister = get_player_id_by_player_number(actual_minister, game_id)
    dbe.Player[id_actual_minister].player_minister = False # The old Minister now is not the Minister
    
    dbe.Game[game_id].game_last_minister = actual_minister # Save actual minister to last minister

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
def add_proclamation_card_on_board(is_phoenix: int, game_id: int):
    """
    Add card proclamation a Board from game_id 
    """
    print(" Adding a new proclamation card o board...\n")
    b = dbe.Game[game_id].game_board
    # is_fenix: True
    if not is_phoenix:
        print(" Adding fenix ploclamation...")
        b.board_promulged_fenix = b.board_promulged_fenix + 1
    # is_fenix: False
    else:
        print(" Adding death eater ploclamation...")
        b.board_promulged_death_eater = b.board_promulged_death_eater + 1
    print("-> Proclamation card added on board ≧◉ᴥ◉≦\n")
    return (b.board_promulged_fenix, b.board_promulged_death_eater)


@db_session
def reset_votes(game_id: int):
    game_players= dbe.Game[game_id].game_players
    for p in game_players:
        p.player_has_voted= False


@db_session
def reset_game_status_votes(game_id: int):
    """
    Reset game_status_votes on db of the game

    game_status_votes: Result votes [5 OK] [5 No]
    """
    dbe.Game[game_id].game_status_vote = 0


@db_session
def reset_game_votes(game_id: int):
    """
    Reset game_votes on db of the game
    
    game_votes: Count players who have voted
    """
    dbe.Game[game_id].game_votes = 0


@db_session
def reset_candidate(player_id: int, game_id: int):
    dbe.Game[game_id].game_candidate_director = -1
    dbe.Player[player_id].player_is_candidate = False


@db_session
def reset_old_minister_db_player(game_id: int):
    number_old_minister= dbe.Game[game_id].game_last_minister
    id_old_minister= get_player_id_by_player_number(number_old_minister, game_id)
    dbe.Player[id_old_minister].player_minister = False


@db_session
def kill_player(player_id: int):
    dbe.Player[player_id].player_is_alive = False


##############################################################################################
######################################board functions#########################################
##############################################################################################

@db_session
def get_amount_deck(game_id: int):
    coded_deck = dbe.Game[game_id].game_board.board_deck_codification
    return len(hf.decode_deck(coded_deck))

@db_session
def get_coded_deck(game_id: int):
    # print(dbe.Game[game_id].game_board.board_deck_codification)
    return dbe.Game[game_id].game_board.board_deck_codification


@db_session #! Using db_session for something that does not access the database
def get_decoded_deck(coded_game_deck: int):
    return hf.decode_deck(coded_game_deck)    


@db_session
def set_new_deck(coded_game_deck: int, game_id: int):
    dbe.Game[game_id].game_board.board_deck_codification = coded_game_deck


@db_session
def get_board_information(): 
    """
    
    """
    return True


@db_session
def get_three_cards(game_id: int):
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
    #removeCard(deckTry)
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
        board_deck_codification = hf.generate_new_deck() #TODO Test with: 254779
    )
    print("-> Board Added ≧◉ᴥ◉≦")


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


@db_session
def get_total_proclamations_phoenix(game_id: int):
    board= dbe.Game[game_id].game_board
    return board.board_promulged_fenix


@db_session
def get_total_proclamations_death_eater(game_id: int):
    """
    Gets the exact amount of proclamations posted by death eaters team
    """
    board= dbe.Game[game_id].game_board
    return board.board_promulged_death_eater


@db_session
def get_game_failed_elections(game_id: int):
    return dbe.Game[game_id].game_failed_elections 


@db_session
def add_failed_elections(game_id: int):
    dbe.Game[game_id].game_failed_elections += 1



@db_session
def reset_failed_elections(game_id: int):
    dbe.Game[game_id].game_failed_elections = 0


@db_session
def discardCard(index: int, game_id: int, is_minister: bool, is_director: bool):
    """
    Return a list of deck without index card
    """
    coded_game_deck = dbe.Game[game_id].game_board.board_deck_codification
    decoded_game_deck = hf.decode_deck(coded_game_deck)
    discarted_deck= decoded_game_deck
    discarted_deck.pop(index-1) # Isnt it + 1?

    # Coded new board_deck for db
    coded_game_deck = hf.encode_deck(discarted_deck)
    dbe.Game[game_id].game_board.board_deck_codification = coded_game_deck

    if(is_minister):
        print(f"-> Minister: Card removed OK ≧◉ᴥ◉≦\n")
        return discarted_deck[:2]
    if(is_director):
        print(f"-> Director: Card removed OK ≧◉ᴥ◉≦\n")
        return discarted_deck[:1]


@db_session
def remove_card_for_proclamation(game_id: int):
    """
    Sets the new deck (discards de first card)
    """
    coded_game_deck = dbe.Game[game_id].game_board.board_deck_codification
    decoded_game_deck = hf.decode_deck(coded_game_deck)
    discarted_deck= decoded_game_deck
    upper_card = discarted_deck.pop(0)
    # Coded new board_deck for db
    coded_game_deck = hf.encode_deck(discarted_deck)
    dbe.Game[game_id].game_board.board_deck_codification = coded_game_deck     
    return upper_card

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

@db_session
def show_log(user_id: int):
    log = dbe.User[user_id].user_log
    log_model = md.ViewLog(
                    log_won_games_fenix = log.log_won_games_fenix,
                    log_won_games_death_eater = log.log_won_games_death_eater,
                    log_lost_games_fenix = log.log_lost_games_fenix,
                    log_lost_games_death_eater = log.log_lost_games_death_eater)
    return log_model

@db_session
def create_log(user):
    dbe.Log(log_user = user,
            log_won_games_fenix = 0,
            log_won_games_death_eater = 0,
            log_lost_games_fenix = 0,
            log_lost_games_death_eater = 0
            )

@db_session
def add_to_log(winner_team: str, game_id: int):
    players = dbe.Game[game_id].game_players
    for player in players:
        user = player.player_user
        if (winner_team == "Death Eaters"):
            if player.player_role == 0:
                user.user_log.log_lost_games_fenix += 1
            else:
                user.user_log.log_won_games_death_eater += 1
        elif (winner_team == "Phoenix"):
            if player.player_role == 0:
                user.user_log.log_won_games_fenix += 1
            else:
                user.user_log.log_lost_games_death_eater += 1


##############################################################################################
######################################log functions#########################################
##############################################################################################


@db_session
def save_last_message_ws(player_id: int, dict_message: dict):
    str_message = json.dumps(dict_message)
    dbe.Player[player_id].player_last_message = str_message
    

##############################################################################################
######################################test functions#########################################
##############################################################################################

@db_session #TODO Re-order
def showDatabase(): # NO TOCAR
    """
    Shows database
    """
    print("---|Users|---\n(user_id, user_email, user_name, user_password, user_photo, user_creation_dt, user_lobby, user_player, user_log, user_defau)")
    dbe.User.select().show()
    
    print("\n---|Lobbies|---\n(lobby_id, lobby_name, lobby_max_players, lobby_min_players, lobby_creator, lobby_user, lobby_players)")
    dbe.Lobby.select().show()
    
    print("\n---|Players|---\n(player_id, player_number, player_nick, player_nick_amount, player_role, player_is_alive, player_chat_blocked, player_is_candidate, player_has_voted, player_vote,player_director, player_minister, player_game, player_lobby, player_user, player_last_message)")
    dbe.Player.select().show()
    
    print("\n---|Games|---\n(game_id, game_is_started, game_imperius, game_expeliarmus, game_total_players, game_actual_minister, game_failed_elections, game_step_turn, game_candidate_director, game_votes, game_status_vote, game_last_director, game_last_minister, game_last_proclamation, game_board)")
    dbe.Game.select().show()
    
    print("\n---|Boards|---\n(id, board_game, board_promulged_fenix, board_promulged_death_eater, board_deck_codification)")
    dbe.Board.select().show()

    print("\n---|Log|---(id, log_user, log_won_games_fenix, log_won_games_death_eater, log_lost_games_fenix, log_lost_games_death_eater)")
    dbe.Log.select().show()
