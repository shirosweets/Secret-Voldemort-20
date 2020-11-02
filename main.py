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
async def register(new_user: md.UserIn) -> int:
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
    lobby_name = dbf.join_lobby(user_id, lobby_id)
   
    return md.JoinLobby(
        joinLobby_name = lobby_name,
        joinLobby_result = (f"welcome to {lobby_name}")
    )

    
@app.delete(
    "/lobby/{lobby_id}", 
    status_code = status.HTTP_202_ACCEPTED, 
    response_model = md.JoinLobby
    # , response_model_exclude_unset = True
)
async def leave_lobby(user_id: int, lobby_id: int):
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if not is_present:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = " You are not in the provided lobby"
        )

    if dbf.is_player_lobby_owner(user_id, lobby_id):
        dbf.delete_lobby(lobby_id)
        raise HTTPException(
            status_code = status.HTTP_200_OK, 
            detail = (f"Player {user_id} has left lobby {lobby_id} and was the creator, so the lobby was destroyed >:C")
        )

    actual_player = dbf.get_player_id_from_lobby(user_id, lobby_id)
    if (actual_player is not 0): # 0: is not on lobby
        dbf.leave_lobby(actual_player)
        raise HTTPException(
            status_code = status.HTTP_200_OK, 
            detail = (f" Player {user_id} has left lobby {lobby_id}")
        )
        
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        detail= (f" Player {user_id} was not in lobby {lobby_id}")
    )



# game endpoints

"""
| start game | DELETE | `/rooms/<lobby_id>/start_game` | | 200 - Ok | PRE: Player is the creator. 
A new game is created with players that joined in the lobby, and the lobby is deleted |
"""
@app.delete(
    "/lobby/{lobby_id}/start_game",
    status_code=status.HTTP_200_OK
)
async def start_game(user_id: int, lobby_id: int): # Final, its ok
    precondition = dbf.is_player_lobby_owner(user_id, lobby_id)
    if not precondition:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= " User is not owner of the lobby"
        )
    game_player_quantity = dbf.get_number_of_players(lobby_id) # int
    dbf.insert_game(md.ViewGame(game_total_players = game_player_quantity), lobby_id) # Creates Game

    return md.GameOut(gameOut_result = "Your game has been started")


# board endpoints
# Review
@app.post(
    "/games/{game_id}/actions/", # {game_id} obj
    status_code= status.HTTP_200_OK,
    response_model= md.SelectMYDirector
)#Player.player_number -> Orden
async def select_director(player_number: int, game_id: int, Authorize: AuthJWT = Depends()) -> int: # Espera devolver un Int
    game_players = dbf.get_game_total_players(game_id)
    if (player_number < 0 or game_players <= 10 <= player_number):
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= (f" Player number {player_number} is not between the expected number (0 to {game_players})")
        )
 
    player_id = dbf.get_player_id_by_player_number(player_number, game_id)
    player_nick = dbf.get_player_nick_by_id(player_id)

    # Check 1
    player_is_alive = dbf.is_player_alive(player_id)
    if not player_is_alive:
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= (f" Player {player_nick} can't be selected as director, because is mateando con sirius Black")
        )

    # Check 2
    can_player_be_director = dbf.can_player_be_director(player_number, game_id)
    if can_player_be_director:
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= (f" Player {player_nick} can't be selected as director, has been selected as minister or director in the last turn")
        )

    dbf.select_director(player_id, player_number, game_id) # Selected player as director
    
    return md.SelectMYDirector(
        dir_player_number = player_number, 
        dir_game_id = game_id,
        dir_game_response = (f"Player {player_nick} is now director")
    ) 

# Review
@app.put(
    "/games/{game_id}/actions/",
    status_code= status.HTTP_200_OK
)
async def post_proclamation(is_phoenix_procl: bool, game_id: int, user_id: int, Authorize: AuthJWT = Depends()) -> int: # Espera devolver un Int
    # Checkss if the user is loged
    Authorize.jwt_optional()    # jwt_required()
    current_user = user_id      # Authorize.get_jwt_identity() # user_id

    player_id = dbf.get_player_id_from_game(current_user, game_id)
    # Checks if the player is the director
    is_director= dbf.player_is_director(player_id)
    
    if not is_director:
        player_nick = dbf.get_player_nick_by_id(player_id)
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED , detail= (f"Player {player_nick} is not the director")
        )
    
    # board[0] phoenix - board[1] death eater
    board = dbf.add_proclamation_card_on_board(is_phoenix_procl, game_id)
    
    ##!! Finish game with proclamations ##
    if(board[0] >= 5):
        print("\n >>> The Phoenixes won!!! <<<\n")
        # Message from Phoenixes won
        print(" Appears free Dobby congratulates the Phoenixes with a sock, hagrid is happy too ♥\n")
        # Message from The Death Eaters losed
        print(" Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries")
        raise HTTPException(
            status_code= status.HTTP_307_TEMPORARY_REDIRECT,
            detail= "Appears free Dobby congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
        )
    elif(board[1] == 4): # DE win when total_players = 5 or 6
        if (5 <= dbf.get_game_total_players(game_id) <= 6):
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message from The Death Eaters won
            print(" Sirius Black is death\n")
            # Mesasage from Phoeenixes losed
            print(" Hagrid and Dobby (with a sock dirty and broken) were death")
            raise HTTPException(
                status_code= status.HTTP_307_TEMPORARY_REDIRECT,
                detail= "Sirius Black is death, Hagrid and Dobby (with a sock dirty and broken) were death"
            )
    elif(board[1] == 5): # DE win when total_players = 7 or 8
        if (7 <= dbf.get_game_total_players(game_id) <= 8):
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message from The Death Eaters won
            print(" Sirius Black is death\n")
            # Mesasage from Phoeenixes losed
            print(" Hagrid and Dobby (with a sock dirty and broken) were death")
            raise HTTPException(
                status_code= status.HTTP_307_TEMPORARY_REDIRECT,
                detail= "Sirius Black is death, Hagrid and Dobby (with a sock dirty and broken) were death"
            )
    elif(board[1] >= 6): # DE win when total_players = 9 or 10
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message from The Death Eaters won
            print(" Sirius Black is death\n")
            # Mesasage from Phoeenixes losed
            print(" Hagrid and Dobby (with a sock dirty and broken) were death")
            raise HTTPException(
                status_code= status.HTTP_307_TEMPORARY_REDIRECT,
                detail= "Sirius Black is death, Hagrid and Dobby (with a sock dirty and broken) were death"
            )

    # Next minister
    dbf.set_next_minister(game_id)

    return md.ViewBoard(
        board_promulged_fenix= board[0],
        board_promulged_death_eater= board[1],
        board_is_spell_active= False,
        board_response = " Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
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