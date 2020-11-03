#test for user db functions
import db_entities_relations as db
import db_functions as dbf


insert_user()

create_lobby(lobby_id, lobby_name, lobby_max_players,  lobby_min_players, lobby_creator, lobby_players )


"""
>>> from db_entities_relations import *
>>> from db_functions import *
>>> [u.user_email for u in User.select()]
['valevispo@gmail.com', 'laozoka@gmail.com', 'asesinodeabuelas@gmail.com', 'salchicacosmica@gmail.com', 'otravalentian@gmail.com']

[u.user_password for u in User.select()]
['passwordOP8', 'otrapasswordmuymala', 'pas22swordOP8', 'aseeswordOP8', 'passwordOP90']

{
  "logIn_email": "valevispo@gmail.com",
  "logIn_password": "passwordOP8"
}
"""