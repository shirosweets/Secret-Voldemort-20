from fastapi import FastAPI, HTTPException, status, Depends
from fastapi import WebSocket, WebSocketDisconnect
from fastapi_jwt_auth import AuthJWT
import models as md
import db_functions as dbf
import helpers_functions as hf
from datetime import datetime
#import db_entities_relations as dbe
import uvicorn
#import basic


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
            userOut_username=new_user.userIn_username, 
            userOut_email=new_user.userIn_email,
            userOut_operation_result="Succesfully created!")


"""@app.post("/login/", 
    status_code=status.HTTP_200_OK
)
async def login(user: md.UserLogIn, Authorize: AuthJWT = Depends()):
    u = dbf.get_user_by_email(user.logIn_email) ##
    try:
        if u.user_password == user.logIn_password:
            # identity must be between string or integer    
            access_token = Authorize.create_access_token(identity=u.user_id) # u.user_name
            return access_token
        else:
            raise HTTPException(status_code=401, detail='Bad password')
    except:
        raise HTTPException(status_code=401, detail='Email does not exist')
"""
@app.post("/login/", 
    status_code=status.HTTP_200_OK
)
async def login(user: md.UserLogIn, Authorize: AuthJWT = Depends()):
    if dbf.check_email_exists(user.logIn_email):
        u = dbf.get_user_by_email(user.logIn_email)
        print(u.user_email, u.user_password, user.logIn_password)
    else:
        raise HTTPException(status_code=401, detail='Email does not exist')

    print(u.user_email, u.user_password)
    print(user.logIn_password)
    if u.user_password == user.logIn_password:  # cambiar por is
            # identity must be between string or integer    
        access_token = Authorize.create_access_token(identity=u.user_name)
        print(access_token)
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail='Bad password')
    
# lobby endpoints

@app.post(
    "/lobby/", 
    status_code = status.HTTP_201_CREATED, 
    response_model = md.LobbyOut, 
    response_model_exclude_unset = True
)
async def create_new_lobby(lobby_data: md.LobbyIn,
            Authorize: AuthJWT = Depends()) -> int: # Espera devolver un Int
    
    Authorize.jwt_optional()    #Authorize.jwt_required()
    current_user = 1            #Authorize.get_jwt_identity()
    name_check = dbf.exist_lobby_name(lobby_data.lobbyIn_name)
    max_check = dbf.check_max_players(lobby_data.lobbyIn_max_players)
    min_check = dbf.check_min_players(lobby_data.lobbyIn_min_players, lobby_data.lobbyIn_max_players)

    if name_check:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "The Lobby name you chose, is already taken"
        ) 
#
    if ((max_check or min_check )):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "The amount of players should be a number between 5 and 10"
        )

    new_lobby = dbf.create_lobby(
                                lobby_data.lobbyIn_name,
                                current_user,    #lobby_data.lobbyIn_creator,
                                lobby_data.lobbyIn_max_players, 
                                lobby_data.lobbyIn_min_players
    )

    dbf.join_game(current_user, new_lobby.lobby_id)

    new_out : md.LobbyOut
    return md.LobbyOut(
        lobbyOut_Id = new_lobby.lobby_id,
        lobbyOut_name = lobby_data.lobbyIn_name,
        lobbyOut_result = "Your new lobby has been succesfully created!"
    )

""" AUTH NEXT SPRINT
async def join_lobby(lobby_id: int,
            lobby_data: md.JoinLobby,
            Authorize: AuthJWT = Depends()) -> int:

    Authorize.jwt_optional()    #Authorize.jwt_required()
    current_user = 2            #Authorize.get_jwt_identity()
"""
@app.post(
    "/lobby/{lobby_id}", 
    status_code = status.HTTP_202_ACCEPTED, 
    response_model = md.JoinLobby,
    response_model_exclude_unset = True
)
async def join_lobby(user_id: int, lobby_id: int):
    # Review
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    #is_present =dbf.check_user_presence_in_lobby(lobby_id, current_user)
    # return <- join_lobby {player}
    dbf.join_lobby(user_id, lobby_id)

    if is_present:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "You already are in the provided lobby"
        )
    
    dbf.join_game(user_id, lobby_id)
    # dbf.change_nick(lobby_data.JoinLobby_name)

"""
| start game | DELETE | `/rooms/<lobby_id>/start_game` | | 200 - Ok | PRE: Player is the creator. 
A new game is created with players that joined in the lobby, and the lobby is deleted |
"""
@app.delete(
    "/rooms/{lobby_id}/start_game", # Dueño aprieta start
    status_code=status.HTTP_200_OK
)
async def start_game(player_id: int): #[PLAYERS]

    #select(c for c in Customer if sum(c.orders.total_price) > 1000)
    #dbe.User.get(user_email=email)
    #current_lobby = select()
    #select(player for player in )
    #dbe.Game(md.ViewGame(game_total_players=hola))  # Create Game change hola from function
    """
    class ViewGame(BaseModel):
    game_is_started: bool = False     # Depends on Lobby
    game_next_minister: int    #
    game_failed_elections: int = 0    # = 0 <= 3 then reset to 0
    game_step_turn: int = -1    # = -1 No asigned
    game_last_director: int = -1    # = -1 No asigned
    game_last_minister: int = -1    # = -1 No asigned
    """
    # Pasar jugadores al Game

    # Eliminar Lobby
    # Selecciona los roles y el orden de los jugadores
    # Setea game_started == True
    hf.startGame()
    
    # If the player are not the owner
    if player_id == 1: # cambiar
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= " You are not the owner :("
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