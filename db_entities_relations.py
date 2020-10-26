from pony.orm import Database, PrimaryKey, Required, Optional, Set

db = Database()

# user entity


# lobby entity


# game entity


# player entity


# board entity


# log entity


# connect the object 'db' with data base
db.bind('sqlite', 'data_base.sqlite', create_db=True)
# generate the data base
db.generate_mapping(create_tables=True)
