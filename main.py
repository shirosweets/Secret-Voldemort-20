from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import websocket_manager as wsm
import models as md
import db_functions as dbf
import authorization as auth
import helpers_functions as hf


app = FastAPI()
wsManager = wsm.WebsocketManager()

#For Integration
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Constrain
    allow_headers=["*"],
)


def raise_exception(
        st_code: str,
        message: str,
        head: md.Optional[dict] = None):
    if head is None:
        raise HTTPException(st_code, message)
    else:
        raise HTTPException(st_code, message, head)


@app.post("/users/",
          status_code=status.HTTP_201_CREATED,
          response_model=md.UserOut
          )
async def create_user(new_user: md.UserIn) -> int:
    if not new_user.valid_format_username():
        raise_exception(status.HTTP_400_BAD_REQUEST, 'can not parse username')
    if not new_user.valid_format_password():
        raise_exception(status.HTTP_400_BAD_REQUEST, 'can not parse password')
    if dbf.check_email_exists(new_user.userIn_email):
        raise_exception(status.HTTP_409_CONFLICT, 'email already registered')
    if dbf.check_username_exists(new_user.userIn_username):
        raise_exception(status.HTTP_409_CONFLICT,
                        'username already registered')
    else:
        dbf.insert_user(
            new_user.userIn_email,
            new_user.userIn_username,
            auth.get_password_hash(new_user.userIn_password),
            new_user.userIn_photo)
        return md.UserOut(
            userOut_username=new_user.userIn_username,
            userOut_email=new_user.userIn_email,
            userOut_operation_result=" Succesfully created!")


@app.post("/login/",
          status_code=status.HTTP_200_OK, response_model=md.Token
          )
async def login(login_data: auth.OAuth2PasswordRequestForm = auth.Depends()):
    user = dbf.get_user_by_email(login_data.username)
    if (user is None) or (not auth.verify_password(login_data.password, user.user_password)):
        raise_exception(status.HTTP_401_UNAUTHORIZED, 'Email does not exist or bad password', {
            "Authorization": "Bearer"})
    access_token_expires = auth.timedelta(
        minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user_email},
        expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}


# lobby endpoints
@app.post(
    "/lobby/",
    status_code=status.HTTP_201_CREATED,
    response_model=md.LobbyOut
)
async def create_new_lobby(lobby_data: md.LobbyIn, user_id: int = Depends(auth.get_current_active_user)) -> int:
    name_check = dbf.exist_lobby_name(lobby_data.lobbyIn_name)
    max_check = dbf.check_max_players(lobby_data.lobbyIn_max_players)
    min_check = dbf.check_min_players(
        lobby_data.lobbyIn_min_players, lobby_data.lobbyIn_max_players)
    if name_check:
        raise_exception(status.HTTP_409_CONFLICT,
                        "The Lobby name you chose, is already taken")
    if (max_check or min_check):
        raise_exception(
            status.HTTP_409_CONFLICT,
            "The amount of players should be a number between 5 and 10")

    new_lobby = dbf.create_lobby(
        lobby_data.lobbyIn_name,
        user_id,
        lobby_data.lobbyIn_max_players,
        lobby_data.lobbyIn_min_players)

    dbf.join_lobby(user_id, new_lobby.lobby_id)
    return md.LobbyOut(
        lobbyOut_Id=new_lobby.lobby_id,
        lobbyOut_name=lobby_data.lobbyIn_name,
        lobbyOut_result="Your new lobby has been succesfully created!"
    )


@app.post(
    "/lobby/{lobby_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.JoinLobby
)
async def join_lobby(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if is_present:
        raise_exception(status.HTTP_409_CONFLICT,
                        "You already are in the provided lobby")
    
    lobby_name = dbf.join_lobby(user_id, lobby_id)
    return md.JoinLobby(
        joinLobby_name=lobby_name,
        joinLobby_result=(f"Welcome to {lobby_name}")
    )

@app.delete(
    "/lobby/{lobby_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.JoinLobby
)
async def leave_lobby(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if not is_present:
        raise_exception(status.HTTP_409_CONFLICT,
                        "You are not in the provided lobby")
                        
    if dbf.is_player_lobby_owner(user_id, lobby_id):
        dbf.delete_lobby(lobby_id)
        raise_exception(
            status.HTTP_200_OK,
            (f"Player {user_id} has left lobby {lobby_id} and was the creator, so the lobby was destroyed >:C"))

    actual_player = dbf.get_player_id_from_lobby(user_id, lobby_id)
    if (actual_player != 0):  # 0: is not on lobby (actual_player is not 0)
        dbf.leave_lobby(actual_player)
        raise_exception(status.HTTP_200_OK,
                        (f"Player {user_id} has left lobby {lobby_id}"))

    raise_exception(status.HTTP_400_BAD_REQUEST,
                    (f"Player {user_id} was not in lobby {lobby_id}"))

# game endpoints
@app.delete(
    "/lobby/{lobby_id}/start_game",
    status_code=status.HTTP_200_OK
)
async def start_game(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    precondition = dbf.is_player_lobby_owner(user_id, lobby_id)
    if not precondition:
        raise_exception(status.HTTP_401_UNAUTHORIZED,
                        "User is not owner of the lobby")

    game_player_quantity = dbf.get_number_of_players(lobby_id)
    if not (5<=game_player_quantity<=10):
        raise_exception(status.HTTP_412_PRECONDITION_FAILED,
                        "List of players should be between 5 and 10")
    dbf.insert_game(md.ViewGame(
        game_total_players=game_player_quantity), lobby_id)
    return md.GameOut(gameOut_result="Your game has been started")


# board endpoints
@app.post(
    "/games/{game_id}/actions/",
    status_code=status.HTTP_200_OK,
    response_model=md.SelectMYDirector
)  # Player.player_number -> Orden
async def select_director(player_number: int, game_id: int, user_id: int = Depends(auth.get_current_active_user)) -> int:  # Espera devolver un Int
    game_players = dbf.get_game_total_players(game_id)    
    if (player_number < 0 or game_players <= 10 <= player_number):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"Player number {player_number} is not between the expected number (0 to {game_players})"))
    player_id = dbf.get_player_id_by_player_number(player_number, game_id)
    player_nick = dbf.get_player_nick_by_id(player_id)

    player_is_alive = dbf.is_player_alive(player_id)    
    if not player_is_alive:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"Player {player_nick} can't be selected as director, because is not alive"))

    can_player_be_director = dbf.can_player_be_director(player_number, game_id)
    if can_player_be_director:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"Player {player_nick} can't be selected as director because is the acutal minister, or was selected as minister or director in the last turn"))

    dbf.select_director(player_id, player_number, game_id)
    return md.SelectMYDirector(
        dir_player_number=player_number,
        dir_game_id=game_id,
        dir_game_response=(f"Player {player_nick} is now director")
    )


@app.put(
    "/games/{game_id}/actions/",
    status_code=status.HTTP_200_OK
)
async def post_proclamation(is_phoenix_procl: bool, game_id: int, user_id: int = Depends(auth.get_current_active_user)) -> int:
    player_id = dbf.get_player_id_from_game(user_id, game_id)

    is_director = dbf.player_is_director(player_id)
    if not is_director:
        player_nick = dbf.get_player_nick_by_id(player_id)
        raise_exception(status.HTTP_401_UNAUTHORIZED,
                        (f"Player {player_nick} is not the director"))
    # board[0] phoenix - board[1] death eater
    board = dbf.add_proclamation_card_on_board(is_phoenix_procl, game_id)
    ##!! Finish game with proclamations ##
    if(board[0] >= 5):
        print("\n >>> The Phoenixes won!!! <<<\n")
        # Message from Phoenixes won
        print("Appears free Dobby congratulates the Phoenixes with a sock, hagrid is happy too ♥\n")
        # Message from The Death Eaters losed
        print("Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries")
        raise_exception(
            status.HTTP_307_TEMPORARY_REDIRECT,
            "Appears free Dobby congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries")

    elif(board[1] == 4):  # DE win when total_players = 5 or 6
        if (5 <= dbf.get_game_total_players(game_id) <= 6):
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message from The Death Eaters won
            print("Sirius Black is death\n")
            # Mesasage from Phoeenixes losed
            print("Hagrid and Dobby (with a sock dirty and broken) were death")
            raise_exception(
                status.HTTP_307_TEMPORARY_REDIRECT,
                "Sirius Black is death, Hagrid and Dobby (with a sock dirty and broken) were death")

    elif(board[1] == 5):  # DE win when total_players = 7 or 8
        if (7 <= dbf.get_game_total_players(game_id) <= 8):
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message from The Death Eaters won
            print("Sirius Black is death\n")
            # Mesasage from Phoeenixes losed
            print("Hagrid and Dobby (with a sock dirty and broken) were death")
            raise_exception(
                status.HTTP_307_TEMPORARY_REDIRECT,
                "Sirius Black is death, Hagrid and Dobby (with a sock dirty and broken) were death")

    elif(board[1] >= 6):  # DE win when total_players = 9 or 10
        print("\n >>> Death Eaters won!!! <<<\n")
        # Message from The Death Eaters won
        print("Sirius Black is death\n")
        # Mesasage from Phoeenixes losed
        print("Hagrid and Dobby (with a sock dirty and broken) were death")
        raise_exception(
            status.HTTP_307_TEMPORARY_REDIRECT,
            "Sirius Black is death, Hagrid and Dobby (with a sock dirty and broken) were death")
    # Next minister
    dbf.set_next_minister(game_id)
    return md.ViewBoard(
        board_promulged_fenix=board[0],
        board_promulged_death_eater=board[1],
        board_is_spell_active=False,
        board_response="Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦")


@app.get(
    "/games/{game_id}/actions/prophecy",
    status_code= status.HTTP_200_OK
)
async def spell_prophecy (game_id: int, user_id: int = Depends(auth.get_current_active_user)):

    total_players= dbf.get_game_total_players(game_id)
    if (total_players>6):
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= " The game has more than 6 players :("
        )

    total_proclamation_DE= dbf.get_death_eaters_proclamations(game_id)
    if (total_proclamation_DE != 3):
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= " Death Eaters doesnt have exactly three proclamations posted :("
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    if not (dbf.player_is_minister(player_id)):
        raise HTTPException(
            status_code= status.HTTP_412_PRECONDITION_FAILED,
            detail= " The player is not the minister :("
        )
    
    return dbf.get_three_cards(game_id)


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

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: wsm.WebSocket, player_id: int):
    await wsManager.connect(player_id, websocket)
    try:
        while True:
            chatMsg = await websocket.receive_text()
            # * for when we implement chat
            print(f"Player {player_id} sent: {chatMsg}")
    except wsm.WebSocketDisconnect:
        wsManager.disconnect(player_id, websocket)
    except wsm.ConnectionClosedOK:
        wsManager.disconnect(player_id, websocket)


#! TEMPORARY FUNCTION FOR TESTING
@app.post("/wsmsg/{player_id}",
          response_model=md.LobbyIn
          )
async def test_endpoint(player_id: int, user_id: int = Depends(auth.get_current_active_user)):
    a = 50
    dic = {"MSG_TYPE": "RAND_INT", "VALUE": a}
    await wsManager.sendMessage(player_id, dic)
    return md.LobbyIn(lobbyIn_name="Pato")
