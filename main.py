from fastapi import FastAPI, HTTPException, status
from fastapi import WebSocket, WebSocketDisconnect
import models as md
import db_entities_relations as dbentities
import db_functions as dbfunctions
import uvicorn

app = FastAPI()

#user endpoints
@app.post("/users/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=md.UserOut
)
async def create_user(new_user: md.UserIn) -> int:
    if not new_user.valid_format_username():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail="can't parse username"
        )
    if not new_user.valid_format_password():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail="can't parse password"
        )
    if check_email_exists(new_user.userIn_email):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, detail="email already registered"
        )
    if check_username_exists(new_user.userIn_name):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, detail="username already registered"
        )
    else:
        insert_user(new_user.userIn_email, new_user.userIn_name, new_user.userIn_password, new_user.userIn_photo)
        return md.UserOut(userOut_email=new_user.userIn_email, userOut_name=new_user.userIn_name, 
            userOut_operation_result="Succesfully created!")

# lobby endpoints

@app.post(
    "/lobby/", 
    status_code = status.HTTP_201_CREATED, 
    response_model = md.LobbyOut, 
    response_model_exclude_unset = True
)
async def create_new_lobby(
            new_lobby: md.LobbyIn) -> int: # Revisar :DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD

    name_check = dbfunctions.exist_lobby_name(new_lobby.lobbyIn_name)
    max_check = dbfunctions.check_max_players(new_lobby.lobbyIn_max_players)
    min_check = dbfunctions.check_min_players(new_lobby.lobbyIn_min_players, new_lobby.lobbyIn_max_players)

    if name_check:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "The Lobby name you chose, is already taken"
        ) 

    if (max_check or min_check):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "The amount of players should be a number between 5 and 10"
        )

    new_lobby_Id = dbfunctions.create_lobby(
                                new_lobby.lobbyIn_name,
                                new_lobby.lobbyIn_creator,
                                new_lobby.lobbyIn_max_players, 
                                new_lobby.lobbyIn_min_players
    )

    new_out : md.LobbyOut
    return md.LobbyOut(
        lobbyOut_Id = new_lobby_Id,
        lobbyOut_name = new_lobby.lobbyIn_name,
        lobbyOut_result = "Your new lobby has been succesfully created!"
    )

# game endpoints


# board endpoints


# log endpoints


# web socket



"""
lobby se crea           -> 1 jugador (0)
join lobby              -> 1 jugador (1) x4
start game              -> elimina lobby -> se inicia el juego (game = true) -> definir/seguir Orden de jugadores -> se selecciona el primer minstro
select_director         -> seleccionado director -> guardado como ultimo director -> brindar cartas de proclamacion a ministro 
seleccionar_proclamación-> ?????? ministro recibe tres cartas -> ministro selecciona dos cartas -> director recibe dos cartas
post_proclamation       -> agregar carta a tablero -> seguir el orden de jugadores


seguir el orden de jugadores = pasar a proximo ministro y decirle que seleccione al director

"""