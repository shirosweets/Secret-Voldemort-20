# Add imports
import random
import db_functions as dbf
import websocket_manager as wsm
######################################################################################################################
################################################ USER FUNCTIONS #######################################################
######################################################################################################################


def valid_format_username(uname) -> bool:
    return 3 < len(uname) < 21
  
def valid_format_password(password) -> bool:
    return 7 < len(password) < 33


######################################################################################################################
################################################ GAME FUNCTIONS #######################################################
######################################################################################################################

# This function encodes the list "deck" and return an int
def encode_deck(deckList : list):
    """
    Returns a encoded deck as int
   
    First bit with 1 of deckInt point the size of deck. Doesn't encode a card
    """
    # deckList = [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
    # returns : 228805 = 0b110111110111000101
    # deckList [1,1,0,0] => deckInt 0b[1]1100 first bit with 1 points to start of deck
    deckInt = 1   # Represents an empty deck
    for card in deckList:
        if (card == 0):
            deckInt = (deckInt << 1)    # add phoenix card
        else:
            deckInt = (deckInt << 1) + 1    # add death_eater card
    return deckInt # Return encoded "deck" for database


def decode_deck(deckInt : int):
    """
    Returns a decoded deck as list
    """
    # deckInt = 228805 = 0b110111110111000101
    # returns: [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
    deckList = list(bin(deckInt))[3:]
    return [int(item) for item in deckList] # Return decoded "deck" for easy use with lists on functions


def generate_new_deck(proclaimed_fenix: int = 0, proclaimed_death_eater: int = 0):
    """
    generate_new_deck(): If the arguments are empty, so the function create a new deck as default
    
    Returns a shuffled deck based on the rules of the game, excluding the cards that were proclaimed
    17 Total cards : 6 phoenix (zero) and 11 death_eather (one) 
    Example: [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
    """
    print(" Generating a new deck...")
    decklist = list()
    for _ in range(11 - proclaimed_death_eater):
        decklist.append(1)
    for _ in range(6 - proclaimed_fenix):
        decklist.append(0)
    random.shuffle(decklist)    # Order
    #print(decklist)
    #print("-> Deck order OK ≧◉ᴥ◉≦\n")
    return encode_deck(decklist)

async def newMinister(wsManager, game_id : int):
    minister_player_number = dbf.get_actual_minister(game_id)
    minister_player_id = dbf.get_player_id_by_player_number(minister_player_number, game_id)
    response_ws = { "TYPE": "NEW_MINISTER", "PAYLOAD": dbf.get_player_nick_by_id(minister_player_id)}
    await wsManager.broadcastInGame(game_id, response_ws)
    minister_ws = { "TYPE": "REQUEST_CANDIDATE", "PAYLOAD": get_possible_candidates(minister_player_number,game_id)}
    minister_id = dbf.get_player_id_by_player_number(minister_player_number, game_id)
    await wsManager.sendMessage(minister_id, minister_ws)

def get_possible_candidates(minister_player_number: int, game: int):
    available_players = []
    for player in dbf.get_players_game(game):
        print("Player", player.player_nick)
        can_be_director = dbf.can_player_be_director_v2(player.player_id)
        is_alive  = dbf.is_player_alive(player.player_id)
        is_minister = player.player_number == minister_player_number
        if (can_be_director and is_alive and not is_minister):
            available_players.append(player.player_nick)
    return available_players
