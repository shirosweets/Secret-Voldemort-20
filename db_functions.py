from pony.orm import db_session, select, count
import db_entities_relations as dbe
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
def insert_user(email: str, username: str, password: str,
                photo: Optional[str]):
    if photo is None:
        dbe.User(
            user_email=email,
            user_name=username,
            user_password=password,
            user_image="https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/",
            user_creation_dt=datetime.now())
    else:
        dbe.User(
            user_email=email,
            user_name=username,
            user_password=password,
            user_image=photo, 
            user_creation_dt=datetime.now())


# lobby funtions


# player functions


# game functions


# board functions


# log functions