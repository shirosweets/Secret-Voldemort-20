from pony.orm import Database, PrimaryKey, Required, Optional, Set

db = Database()

#user entity
class User(db.Entity):
    id = PrimaryKey(int, auto=True) 
    email = Required(str, unique=True)
    username = Required(str, unique=True, max_len=16)
    password = Required(str, max_len= 32)
    photo = Optional(str)


#lobby entity


#game entity


#player entity


#board entity


#log entity


# connect the object 'db' with data base
db.bind('sqlite', 'data_base.sqlite', create_db=True)
# generate the data base
db.generate_mapping(create_tables=True)

