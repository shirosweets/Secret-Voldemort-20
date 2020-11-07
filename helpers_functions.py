# Add imports
import random
import models as md
import db_functions as dbf
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, status, Header, Depends
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta

import db_entities_relations as dbe
import db_functions as dbf

app = FastAPI()


######################################################################################################################
############################################### Register FUNTIONS ####################################################
######################################################################################################################


def valid_format_username(username: str) -> bool:
    return 3 < len(username) < 17
      
def valid_format_password(password: str) -> bool:
    return 7 < len(password) < 33


######################################################################################################################
################################################ LogIn FUNTIONS #######################################################
######################################################################################################################

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #!FIXME
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


def verify_password(plain_password: str, hashed_password: str):
    print(hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str): 
    user = dbf.get_user_by_email(username)
    user_password = user.user_password
    if not user:
        return False
    if not verify_password(password, user_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = md.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = dbf.get_user_by_username(token_data.username)
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: md.User = Depends(get_current_user)):
    if current_user.user_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user.user_id

######################################################################################################################
################################################ GAME FUNTIONS #######################################################
######################################################################################################################

# This function encodes the list "deck" and return an int
def encode_deck(deckList : list):
    """
    Returns a encoded deck as int
    deckList = [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
    returns : 228805 = 0b110111110111000101
    deckList [1,1,0,0] => deckInt 0b[1]1100 first bit with 1 points to start of deck
    First bit with 1 of deckInt point the size of deck. Doesn't encode a card
    """
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


def generate_new_deck(proclaimed_fenix: int = 0, proclaimed_death_eater: int = 0): # board_id: in
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
    for _ in range(6 - proclaimed_death_eater):
        decklist.append(0)
    random.shuffle(decklist)    # Order
    #print(decklist)
    #print("-> Deck order OK ≧◉ᴥ◉≦\n")
    return encode_deck(decklist)


# <<<Testing>>>
# <Encoding and decoding>
# lis = [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
# print(encode_deck(lis))
# print(decode_deck(encode_deck(lis)))
# print(lis, "<<deberia dar")
#print(encode_deck([1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]))
#print(bin(encode_deck([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0])))
# <generating new decks>
# print(" Starting a new game...")
# deck = generate_new_deck() # 0, 0
# print(f"{deck} == {decode_deck(deck)}")
# print(" Checking a game started...")
# deck = generate_new_deck(2,3)
# print(f"{deck} == {decode_deck(deck)}")# Add imports