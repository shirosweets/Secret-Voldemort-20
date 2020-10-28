from fastapi import FastAPI, HTTPException, status
from fastapi import WebSocket, WebSocketDisconnect
import models as md
import db_entities_relations as dbe
import db_functions as dbf
from datetime import datetime


app = FastAPI()


# users endpoints
@app.post("/users/",
          status_code=status.HTTP_201_CREATED,
          response_model=md.UserOut
          )
async def create_user(new_user: md.UserIn) -> int:
    if not new_user.valid_format_username():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="can't parse username"
        )
    if not new_user.valid_format_password():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="can't parse password"
        )
    if dbf.check_email_exists(new_user.userIn_email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="email already registered"
        )
    if dbf.check_username_exists(new_user.userIn_username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already registered"
        )
    else:
        dbf.insert_user(
            new_user.userIn_email,
            new_user.userIn_username,
            new_user.userIn_password,
            new_user.userIn_photo)
        return md.UserOut(
            userOut_username=new_user.userIn_username, userOut_email=new_user.userIn_email,
            userOut_operation_result="Succesfully created!")


# lobby endpoints


# game endpoints


# board endpoints


# log endpoints


# web socket
