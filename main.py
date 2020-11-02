from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi import WebSocket, WebSocketDisconnect
from fastapi_jwt_auth import AuthJWT
import models as md
import db_functions as dbf
import helpers_functions as hf
from datetime import datetime
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


@app.post("/login/", 
    status_code=status.HTTP_200_OK
)
async def login(user: md.LogIn, Authorize: AuthJWT = Depends()):
    if dbf.check_email_exists(user.logIn_email):
        u = dbf.get_user_by_email(user.logIn_email)
        print(u.user_email, u.user_password, user.logIn_password)
    else:
        raise HTTPException(status_code=401, detail='Email does not exist')

    print(u.user_email, u.user_password)
    print(user.logIn_password)
    if u.user_password == user.logIn_password:
            # identity must be between string or integer    
        access_token = Authorize.create_access_token(identity=u.user_id)
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
) ## REVIEW
async def create_new_lobby(lobby_data: md.LobbyIn, usuario: int, Authorize: AuthJWT = Depends()) -> int: # Espera devolver un Int

    Authorize.jwt_optional()    ## Authorize.jwt_required()
    #Add for next spritn        
    current_user = usuario      ## Authorize.get_jwt_identity()

    name_check = dbf.exist_lobby_name(lobby_data.lobbyIn_name)
    max_check = dbf.check_max_players(lobby_data.lobbyIn_max_players)
    min_check = dbf.check_min_players(lobby_data.lobbyIn_min_players, lobby_data.lobbyIn_max_players)

    if name_check:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "The Lobby name you chose, is already taken"
        ) 
    if ((max_check or min_check)):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "The amount of players should be a number between 5 and 10"
        )
   
    """
    new_lobby= dbf.create_lobby(lobby_data.lobbyIn_name, 
                    current_user, #lobby_data.lobbyIn_creator,
                    lobby_data.lobbyIn_max_players, 
                    lobby_data.lobbyIn_min_players)
    """
    new_lobby= dbf.create_lobby(lobby_data.lobbyIn_name, current_user, lobby_data.lobbyIn_max_players, lobby_data.lobbyIn_min_players)
    
    dbf.join_lobby(current_user, new_lobby.lobby_id) # Change current_user for "user_id"

    return md.LobbyOut(
        lobbyOut_Id = new_lobby.lobby_id,
        lobbyOut_name = lobby_data.lobbyIn_name,
        lobbyOut_result = "Your new lobby has been succesfully created!"
    )

@app.post(
    "/lobby/{lobby_id}", 
    status_code = status.HTTP_202_ACCEPTED, 
    response_model = md.JoinLobby
    # , response_model_exclude_unset = True
)
async def join_lobby(user_id: int, lobby_id: int):
    # Review
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    #is_present =dbf.check_user_presence_in_lobby(lobby_id, current_user)
    # return <- join_lobby {player}

    if is_present:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = " You already are in the provided lobby"
        )
    
    dbf.join_lobby(user_id, lobby_id)

    
@app.delete(
    "/lobby/{lobby_id}", 
    status_code = status.HTTP_202_ACCEPTED, 
    response_model = md.JoinLobby
    # , response_model_exclude_unset = True
)
async def leave_lobby (user_id: int, lobby_id: int):
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if not is_present:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = " You are not in the provided lobby"
        )
    actual_player = dbf.get_player_id_from_lobby(user_id, lobby_id)
    if dbf.is_player_lobby_owner(actual_player, lobby_id):
        # Eliminar jugadores del lobby, cuando es el owner el que se va
        dbf.delete_lobby(lobby_id)
        raise HTTPException(
            status_code = status.HTTP_200_OK, 
            detail = (f"Player {user_id} has left lobby {lobby_id} and was the creator, so the lobby was destroyed >:C")
        )
    if (actual_player is not 0): # 0: is not on lobby
        dbf.leave_lobby(actual_player)
        raise HTTPException(
            status_code = status.HTTP_200_OK, 
            detail = (f"Player {user_id} has left lobby {lobby_id}")
        )
        
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        detail= (f"Player {user_id} was not in lobby {lobby_id}")
    )



# game endpoints

"""
| start game | DELETE | `/rooms/<lobby_id>/start_game` | | 200 - Ok | PRE: Player is the creator. 
A new game is created with players that joined in the lobby, and the lobby is deleted |
"""
@app.delete(
    "/rooms/{lobby_id}/start_game",
    status_code=status.HTTP_200_OK
)
async def start_game(player_id: int, lobby_id: int):
    precondition = dbf.is_player_lobby_owner(player_id, lobby_id) # 
    if not precondition:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= ' Player is not the owner'
        )
    game_player_quantity = dbf.get_number_of_players(lobby_id) # int
    dbf.insert_game(md.ViewGame(game_total_players = game_player_quantity), lobby_id) # Creates Game


# board endpoints
# Review
@app.post(
    "/games/{game_id}/actions/", # {game_id} obj
    status_code= status.HTTP_200_OK,
    response_model= md.SelectMYDirector
)
async def select_director(player_number: int, Authorize: AuthJWT = Depends()) -> int: # Espera devolver un Int
    candidate= md.SelectMYDirector                      # candidate: md.SelectMYDirector
    candidate.dir_player_number= player_number          # candidate.dir_player_number= player_number
    candidate.dir_game_id=  0                           # {game_id}   candidate.dir_game_id=  0

    if candidate.dir_player_number == None or candidate.dir_game_id == None:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT, detail= " 409 - Internal error :("
        )

    return {"is_selected": True}

# Review
@app.put(
    "/games/{game_id}/actions/",
    status_code= status.HTTP_200_OK
)
async def post_proclamation(is_phoenix_procl: bool, game_id: int, Authorize: AuthJWT = Depends()) -> int: # Espera devolver un Int
    # Checkss if the user is loged
    Authorize.jwt_optional()  # jwt_required()
    current_user = Authorize.get_jwt_identity() # user_id

    # Checks if the player is the director
    is_director= dbf.player_is_director(game_id, current_user)
    
    if is_director:
        board = dbf.add_proclamation_card_on_board(is_phoenix_procl, game_id)
        return md.ViewBoard(board)
    else:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT, detail= " 409 - I couldn't add the card :("
    )


# log endpoints

"""
@app.get(
    status_code=status.HTTP_201_CREATED,
)
async def create_log(user_id: int, role_was_fenix: bool,  won: bool):
    if role_was_fenix:
        # add log on fenix
        if won:
            # Win, add log on fenix win
        else:
            # Lose, add log on fenix lose
    else:
        # add log on death eater
        if won:
            # Win, add log on death eater
        else:
            # Lose, add log on death eater
    # Add +1 to all games
"""


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