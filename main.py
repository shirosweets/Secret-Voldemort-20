from fastapi import FastAPI, HTTPException, status
from fastapi import WebSocket, WebSocketDisconnect
import models as md
import db_entities_relations as dbe
import db_functions as dbf


app = FastAPI()


#users endpoints
@app.post("/users/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=md.UserOut, response_model_exclude_unset=True
)
async def create_user(new_user: md.UserIn) -> int:
    if dbf.check_email_exists(new_user.email):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, detail="email already exists"
        )
    if dbf.check_username_exists(new_user.username):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, detail="username already exists"
        )
    dbf.insert_user(new_user.email, new_user.username, new_user.password, new_user.photo)
    return md.UserOut(
        username=new_user.username, email=new_user.email,
        operation_result="Succesfully created!")


# lobby endpoints


# game endpoints


# board endpoints


# log endpoints


# web socket
