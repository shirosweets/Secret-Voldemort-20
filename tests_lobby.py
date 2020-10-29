#test for user db functions
import db_entities_relations as db
import db_functions as dbf


diego = dbf.create_lobby(lobbyIn_creator = "pippiipiipii",
    lobbyIn_name = "puipui",
    lobbyIn_max_players = 10,
    lobbyIn_min_players = 5)

db.Lobby.select().show()

# in terminal
#venv activated
#python
#from db_entities_relations import *
#from db_functions import * 
# Lobby.select().show()