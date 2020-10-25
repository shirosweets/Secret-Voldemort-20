from pony.orm import db_session, select, count
from db_entities_relations import User 
from typing import Optional

#some users functions
@db_session
def check_email_exists(new_email):
    return User.exists(email=new_email)

@db_session
def check_username_exists(new_uname):
    return User.exists(username=new_uname)

@db_session
def insert_user(email:str, username:str, password:str, photo: Optional[str]):
    if photo is None:
        User(email=email, username=username, password=password, photo="https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/")
    else: 
        User(email=email, username=username, password=password, photo=photo)


#some lobby funtions


#some player functions


#some game functions


#some board functions


#some history functions