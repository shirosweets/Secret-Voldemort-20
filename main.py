from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import websocket_manager as wsm
import models as md
import db_functions as dbf
import authorization as auth
import helpers_functions as hf

public_ip = "190.195.56.40" # Insert your own public IP address here IF YOU ARE TRYING TO HOST
local_ip = "192.168.0.11" # Insert your own private IP address here IF YOU ARE TRYING TO HOST

app = FastAPI()
wsManager = wsm.WebsocketManager()

# Defines a list of allowed origins (they can send js requests to backend)
origins = [
    (f"http://{public_ip}:3000"), # allows access to external clients ( WAN - Requires server Forwarding on port 3000 and 8000)
    (f"http://{local_ip}:3000"), # allows access to internal clients ( LAN - Requires to be in the same network)
    (f"http://127.0.0.1:3000"), # 127.0.0.1 to 127.255.255.254 ip's, can host different services, sharing the same port
    (f"http://localhost:3000")] # allows access to local clients (Local - Only local mashine testing)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
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


# user endpoints
@app.post("/users/",
          status_code=status.HTTP_201_CREATED,
          response_model=md.UserOut
          )
async def create_user(new_user: md.UserIn) -> int:
    if not hf.valid_format_username(new_user.userIn_username):
        raise_exception(status.HTTP_400_BAD_REQUEST, "Can't parse username"
                        )
    if dbf.check_email_exists(new_user.userIn_email):
        raise_exception(status.HTTP_409_CONFLICT, "Email already registered"
                        )
    if dbf.check_username_exists(new_user.userIn_username):
        raise_exception(status.HTTP_409_CONFLICT, "Username already registered"
                        )
    if not hf.valid_format_password(new_user.userIn_password):
        raise_exception(status.HTTP_400_BAD_REQUEST, "Can't parse password"
                        )
    else:
        dbf.insert_user(
            new_user.userIn_email,
            new_user.userIn_username,
            auth.get_password_hash(new_user.userIn_password),
            new_user.userIn_photo
        )
        return md.UserOut(
            userOut_username=new_user.userIn_username,
            userOut_email=new_user.userIn_email,
            userOut_operation_result=" Succesfully created!"
        )


@app.post("/login/",
          status_code=status.HTTP_200_OK,
          response_model=md.Token
          )
async def login(login_data: auth.OAuth2PasswordRequestForm = auth.Depends()):
    user = dbf.get_user_by_email(login_data.username)
    if (user is None) or (not auth.verify_password(
            login_data.password, user.user_password)):
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            "Email doesn't exist or invalid password",
            {"Authorization": "Bearer"}
        )
    access_token_expires = auth.timedelta(
        minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user_email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/users/",
    status_code=status.HTTP_200_OK,
    response_model=md.ProfileInformation
    )
async def user_information(user_id: int = Depends(auth.get_current_active_user)):
    user = dbf.get_user_by_id(user_id)
    info = md.ProfileInformation(profile_username=user.user_name)
    return info


@app.patch(
    "/users/change_profile/",
    status_code=status.HTTP_200_OK,
    response_model=md.ResponseText
)
async def update_profile(profile_data: md.ChangeProfile, user_id: int = Depends(auth.get_current_active_user)) -> int:
    if profile_data.photo == '' :
        profile_data.photo = None
        
    if ((profile_data.username is None) and (profile_data.photo is None)):
        raise_exception(
            status.HTTP_400_BAD_REQUEST, 
            "You must insert a username or a Photo"
        )
        
    if not (profile_data.username is None):
        if not (hf.valid_format_username(profile_data.username)):
            raise_exception(
                status.HTTP_400_BAD_REQUEST, 
                "Can't parse username"
            )

        if dbf.check_username_exists(profile_data.username):
            raise_exception(
                status.HTTP_409_CONFLICT, "Username is already registered"
            )
    
    dbf.update_user_profile(user_id, profile_data.username, profile_data.photo)
    return md.ResponseText(responseText = "Your data has been updated correctly")


@app.patch(
    "/users/change_profile/change_password/",
    status_code=status.HTTP_200_OK,
    response_model=md.ResponseText
)
async def change_password(pass_data: md.ChangePassword, user_id: int = Depends(auth.get_current_active_user)) -> int:
    user = dbf.get_user_by_id(user_id)
    if not auth.verify_password(
            pass_data.current_password, user.user_password):
        raise_exception(
            status.HTTP_401_UNAUTHORIZED, "Invalid password",
            {"Authorization": "Bearer"}
        )
    
    if not hf.valid_format_password(pass_data.new_password):
        raise_exception(
            status.HTTP_400_BAD_REQUEST, "Can't parse new password"
        )

    if auth.verify_password(pass_data.new_password, user.user_password):
        raise_exception(
            status.HTTP_409_CONFLICT,
            "Can't register the same password you already have"
        )
    pass_data.new_password = auth.get_password_hash(pass_data.new_password)

    dbf.change_password_user(user_id, pass_data.new_password)
    return md.ResponseText(responseText = "Your password has been updated correctly")


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
        lobby_data.lobbyIn_min_players,
        lobby_data.lobbyIn_max_players)

    if  not (4 <= len(lobby_data.lobbyIn_name) <= 20):
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The Lobby name you chose, is out of range (Should be between 4 and 20 characters)"
        )

    if name_check:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The Lobby name you chose, is already taken"
        )

    if (max_check or min_check):
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The amount of players should be a number between 5 and 10"
        )

    new_lobby = dbf.create_lobby(
        lobby_data.lobbyIn_name,
        user_id,
        lobby_data.lobbyIn_max_players,
        lobby_data.lobbyIn_min_players
    )

    dbf.join_lobby(user_id, new_lobby.lobby_id)
    player_id = dbf.get_player_id_from_lobby(user_id, new_lobby.lobby_id)

    return md.LobbyOut(
        lobbyOut_Id=new_lobby.lobby_id,
        lobbyOut_name=lobby_data.lobbyIn_name,
        lobbyOut_player_id=player_id,
        lobbyOut_player_nick=dbf.get_player_nick_by_id(player_id),
        lobbyOut_result=" Your new lobby has been succesfully created!"
    )


@app.get(
    "/lobby/list_lobbies/",
    status_code=status.HTTP_200_OK,
    response_model=md.LobbyDict
)
async def list_lobbies(start_from: int = 1, end_at: int = None, user_id: int = Depends(auth.get_current_active_user)):
    if not (end_at is None):
        if start_from > end_at:
            raise_exception(
                status.HTTP_400_BAD_REQUEST,
                "start_from value must be bigger than end_at value"
            )

    lobby_dict = dbf.get_lobbies_dict(start_from, end_at)
    return md.LobbyDict(lobbyDict=lobby_dict)


@app.post(
    "/lobby/{lobby_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.JoinLobby
)
async def join_lobby(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    lobby_exists = dbf.check_lobby_exists(lobby_id)
    if not lobby_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The lobby you selected does not exist"
        )

    if len(dbf.get_players_lobby(lobby_id)) >= dbf.get_lobby_max_players(lobby_id):
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The lobby you selected is already full"
        )

    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if is_present:
        lobby = dbf.get_lobby_by_id(lobby_id)
    else:
        lobby = dbf.join_lobby(user_id, lobby_id)

    lobby_name = lobby.lobby_name
    player_nicks = dbf.get_player_nicks_from_lobby(lobby_id)
    player_id = dbf.get_player_id_from_lobby(user_id, lobby_id)

    player_nick= dbf.get_player_nick_by_id(player_id)
    socketDic= { "TYPE": "NEW_PLAYER_JOINED", "PAYLOAD": player_nick }
    await wsManager.broadcastInLobby(lobby_id, socketDic)

    return md.JoinLobby(
        joinLobby_name=lobby_name,
        joinLobby_player_id=player_id,
        joinLobby_player_nick=player_nick,
        joinLobby_result=(f" Welcome to {lobby_name}"),
        joinLobby_nicks=player_nicks,
        joinLobby_is_owner=dbf.is_player_lobby_owner(user_id, lobby_id)
    )

@app.post(
    "/lobby/{lobby_id}/change_nick",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.ResponseText
)
async def change_nick(lobby_id: int, new_nick: md.Nick, user_id: int = Depends(auth.get_current_active_user)):
    if not (4 <= len(new_nick.nick) <= 20):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " Your Nick must have between 4 and 20 characters"
        )

    lobby_exists = dbf.check_lobby_exists(lobby_id)
    if not lobby_exists:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The lobby you selected does not exist"
        )

    is_user_in_lobby = dbf.is_user_in_lobby(user_id, lobby_id)
    if not is_user_in_lobby:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the lobby you selected ({lobby_id})")
        )

    player_id = dbf.get_player_id_from_lobby(user_id, lobby_id)
    nick_points = dbf.get_nick_points(player_id)
    if nick_points <= 0:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " You changed your nick too many times >:C"
        )

    nick_taken = dbf.check_nick_exists(lobby_id, new_nick.nick)
    if nick_taken:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The nick you selected is already taken"
        )

    old_nick = dbf.get_player_nick_by_id(player_id)
    nick_points = dbf.change_nick(player_id, new_nick.nick)

    socketDict2= { "OLD_NICK": old_nick, "NEW_NICK": new_nick.nick }
    socketDict= { "TYPE": "CHANGED_NICK", "PAYLOAD": socketDict2 }
    await wsManager.broadcastInLobby(lobby_id, socketDict)

    return md.ResponseText(
        responseText=(
            f" Your nick has been sucessfully changed to {new_nick.nick}, you can change it {nick_points} more times")
    )


@app.delete(
    "/lobby/{lobby_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.ResponseText
)
async def leave_lobby(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    lobby_exists = dbf.check_lobby_exists(lobby_id)
    if not lobby_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The lobby you selected does not exist"
        )

    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if not is_present:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " You are not in the provided lobby"
        )

    actual_player = dbf.get_player_id_from_lobby(user_id, lobby_id)
    nick = dbf.get_player_nick_by_id(actual_player)

    if dbf.is_player_lobby_owner(user_id, lobby_id):
        socketDic= { "TYPE": "LEAVE_LOBBY", "PAYLOAD": "ABANDONED"}
        await wsManager.broadcastInLobby(lobby_id, socketDic)
        for player in dbf.get_players_lobby(lobby_id):
            dbf.leave_lobby(player.player_id)
            await wsManager.disconnect(player.player_id)
        dbf.delete_lobby(lobby_id)
        
        return md.ResponseText(
        responseText=(f" You closed lobby {lobby_id}")
        )

    dbf.leave_lobby(actual_player)
    socketDic= { "TYPE": "PLAYER_LEFT", "PAYLOAD": nick}
    await wsManager.broadcastInLobby(lobby_id, socketDic)

    return md.ResponseText(
        responseText=(f" You left lobby {lobby_id}")
    )


# game endpoints
@app.delete(
    "/lobby/{lobby_id}/start_game",
    status_code=status.HTTP_200_OK,
    response_model=md.ResponseText
)
async def start_game(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    lobby_exists = dbf.check_lobby_exists(lobby_id)
    if not lobby_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The lobby you selected does not exist"
        )

    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if not is_present:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " You are not in the provided lobby"
        )
        
    precondition = dbf.is_player_lobby_owner(user_id, lobby_id)
    if not precondition:
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            " User is not owner of the lobby"
        )

    game_player_quantity = dbf.get_number_of_players(lobby_id)

    lobby_min_players = dbf.get_lobby_min_players(lobby_id)
    lobby_max_players = dbf.get_lobby_max_players(lobby_id)
    if not (lobby_min_players <= game_player_quantity <= lobby_max_players):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" List of players should be between {lobby_min_players} and {lobby_max_players}")
        )
    
    game_id = dbf.insert_game(
        md.ViewGame(game_total_players=game_player_quantity),
        lobby_id
    )

    dbf.set_game_step_turn("START_GAME", game_id) # Set step_turn

    socketDict= { "TYPE": "START_GAME", "PAYLOAD": game_id }
    await wsManager.broadcastInGame(game_id, socketDict)
    await hf.newMinister(wsManager, game_id)
    return md.ResponseText(responseText=(" Your game has been started"))


@app.get(
    "/games/list_games/",
    status_code=status.HTTP_200_OK,
    response_model=md.GameDict
)
async def list_games(start_from: int = 1, end_at: int = None, user_id: int = Depends(auth.get_current_active_user)):
    if not (end_at is None):
        if start_from > end_at:
            raise_exception(
                status.HTTP_400_BAD_REQUEST,
                " start_from value must be bigger than end_at value"
            )

    game_dict = dbf.get_games_dict(start_from, end_at, user_id)
    return md.GameDict(gameDict=game_dict)


@app.get(
    "/games/{game_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_relative_game_information(game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    if not dbf.is_user_in_game(user_id, game_id):
        raise_exception(status.HTTP_412_PRECONDITION_FAILED,
        " You are not on the game requested.")

    game_info = dbf.get_relative_game_information(user_id, game_id)
    for nick in game_info["player_array"]:
        p_num = game_info["player_array"][nick]["player_number"]
        p_id = dbf.get_player_id_by_player_number(p_num, game_id)
        game_info["player_array"][nick]["connected"] = wsManager.isPlayerConnected(p_id)
    return game_info

@app.get(
    "/games/{game_id}/deck",
    status_code=status.HTTP_200_OK,
)
async def get_deck_amount(game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )
    if not dbf.is_user_in_game(user_id, game_id):
        raise_exception(status.HTTP_412_PRECONDITION_FAILED,
        " You are not on the game requested.")

    response = { "cards_in_deck": dbf.get_amount_deck(game_id) }
    return response


# board endpoints
@app.post(
    "/games/{game_id}/select_director/",
    status_code=status.HTTP_200_OK,
    response_model=md.SelectMYDirector
)
async def select_director(player_number: md.PlayerNumber, game_id: int, user_id: int = Depends(auth.get_current_active_user)) -> int:
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    user_player_id = dbf.get_player_id_from_game(user_id, game_id)
    is_player_minister = dbf.is_player_minister(user_player_id)
    if not is_player_minister:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not the minister")
        )

    step_turn= dbf.get_game_step_turn(game_id)
    if not (("START_GAME" == step_turn) or ("POST_PROCLAMATION_ENDED" == step_turn) or ("VOTATION_ENDED_NO" == step_turn) or ("SPELL" == step_turn)):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " Step turn is not START_GAME or POST_PROCLAMATION_ENDED. You are not in the stage of the corresponding turn."
    )

    game_players = dbf.get_game_total_players(game_id)
    if not (0 <= player_number.playerNumber < game_players):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player number {player_number} is not between the expected number (0 to {game_players})")
        )

    player_id = dbf.get_player_id_by_player_number(player_number.playerNumber, game_id)
    player_nick = dbf.get_player_nick_by_id(player_id)
    player_is_alive = dbf.is_player_alive(player_id)
    if not player_is_alive:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player {player_nick} can't be selected as director candidate, {player_nick} is dead")
        )

    can_player_be_director = dbf.can_player_be_director(
        player_number.playerNumber, game_id)
    if can_player_be_director:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player {player_nick} can't be selected as director candidate because is the acutal minister or was selected as minister/director in the last turn")
        )

    minister_id = dbf.get_player_id_from_game(user_id, game_id)
    minister_number = dbf.get_player_number_by_player_id(minister_id)
    if (minister_number == player_number.playerNumber): # Particularly usefull with Imperius
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            "You can not select yourself as director"
        )

    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
            status.HTTP_409_CONFLICT,
            " You can not do this while expeliarmus stage is active"
        )

    dbf.select_candidate(player_id, player_number.playerNumber, game_id)

    dbf.set_game_step_turn("SELECT_CANDIDATE_ENDED", game_id)

    candidate_id= dbf.get_player_id_by_player_number(player_number.playerNumber, game_id)
    candidate_nick= dbf.get_player_nick_by_id(candidate_id)
    socketDict= { "TYPE": "REQUEST_VOTE", "PAYLOAD": candidate_nick }
    await wsManager.broadcastInGame(game_id, socketDict)

    return md.SelectMYDirector(
        dir_player_number=player_number.playerNumber,
        dir_game_id=game_id,
        dir_game_response=(f" Player {player_nick} is now director candidate")
    )


@app.put(
    "/games/{game_id}/select_director/vote",
    status_code=status.HTTP_200_OK,
    response_model=md.VoteOut
)
async def vote(vote_recive: md.Vote, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    is_player_alive = dbf.is_player_alive(player_id)
    if not is_player_alive:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are dead in the game ({game_id}), you can't vote")
        )

    step_turn= dbf.get_game_step_turn(game_id)
    if("SELECT_CANDIDATE_ENDED" != step_turn):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" The candidate director has not been elected")
        )
    
    actual_vote= dbf.check_has_voted(player_id)
    if actual_vote:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You have already voted in the game ({game_id}), you can't vote more than 2 times")
        )
    
    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You can not do this while expeliarmus stage is active"
            )
    
    actual_votes = dbf.player_vote(vote_recive.vote, player_id, game_id)
    total_players_in_game = dbf.get_game_total_players(game_id)

    total_players_alive_in_game = total_players_in_game - (dbf.get_dead_players(game_id))
    
    is_vote_player = dbf.check_has_voted(player_id) # TRUE
    if ((actual_votes == total_players_alive_in_game) and (is_vote_player)):
        status_votes = dbf.get_status_vote(game_id)
        actual_candidate = dbf.get_game_candidate_director(game_id)
        player_id_candidate = dbf.get_player_id_by_player_number(actual_candidate, game_id)

        dict1 = dict()
        for player in dbf.get_players_game(game_id):
            dict1[player.player_nick] = player.player_vote
        dic2={ "TYPE": "ELECTION_RESULT", "PAYLOAD": dict1 }
        await wsManager.broadcastInGame(game_id, dic2)

        if(status_votes > 0): # Acepted candidate
            print(" Successful Election...")
            dbf.reset_candidate(player_id_candidate, game_id) # Reset candidate
            dbf.reset_votes(game_id) # Reset votes on players
            dbf.reset_game_status_votes(game_id) # Reset status votes on game
            dbf.reset_game_votes(game_id) # Reset game votes on game
            dbf.set_game_step_turn("VOTATION_ENDED_OK", game_id) # Set step_turn
            dbf.select_director(player_id_candidate, actual_candidate, game_id)
            # Get 3 cards
            model_list = dbf.get_three_cards(game_id)
            # Pass 3 cards as str #[card1, card2, card3] (list of 3 str) 
            socket_list = [model_list.prophecy_card_0, model_list.prophecy_card_1, model_list.prophecy_card_2]
            socketDic={
                "TYPE": "MINISTER_DISCARD", "PAYLOAD": socket_list
            }
            await wsManager.sendMessage(player_id_candidate, socketDic)

            if ((dbf.get_player_role(player_id_candidate) == 2) and (dbf.get_total_proclamations_death_eater(game_id) >= 4)):
                roles_dict = dbf.get_roles(game_id)
                result_dict = {"WINNER": 1, "ROLES": roles_dict}
                socketDic= { "TYPE": "ENDGAME", "PAYLOAD": result_dict }
                await wsManager.broadcastInGame(game_id, socketDic)
                dbf.set_game_step_turn("FINISHED_GAME", game_id)
        else:
            print(" Failed Election...")
            dbf.reset_candidate(player_id_candidate, game_id) # Reset candidate
            dbf.reset_votes(game_id) # Reset votes
            dbf.reset_game_status_votes(game_id) # Reset status votes on game
            dbf.reset_game_votes(game_id) # Reset game votes on game
            dbf.set_game_step_turn("VOTATION_ENDED_NO", game_id) # Set step_turn
            dbf.add_failed_elections(game_id) # +1 game_failed_elections on db
            dbf.set_next_minister_failed_election(game_id)
            dbf.set_last_proclamation(-1, game_id)

            await hf.newMinister(wsManager, game_id)

            dbf.set_last_proclamation(-1, game_id)
            if (dbf.is_imperius_active(game_id) != -1):
                dbf.finish_imperius(game_id)

            if (dbf.get_game_failed_elections(game_id) == 3):
                dbf.reset_failed_elections(game_id)

                # caos_promulgate_card

                promulgated_card = dbf.remove_card_for_proclamation(game_id)
                board = dbf.add_proclamation_card_on_board(promulgated_card, game_id) 

                # Informs all the players what proclamation has been posted
                socketDic= { "TYPE": "CHAOS", "PAYLOAD": promulgated_card }
                await wsManager.broadcastInGame(game_id, socketDic)
                
                if(board[0] >= 5): # Phoenixes win when they manage to post 5 of their proclamations
                    players = dbf.get_players_game(game_id) # [PLAYERS]
                    result= {}
                    for player in players:
                        role= dbf.get_player_role(player.player_id)
                        result[player.player_nick]= role
                    socketDict2= { "WINNER": 0, "PAYLOAD": result }
                    socketDict={ "TYPE": "END_GAME", "PAYLOAD": socketDict2 }
                    await wsManager.broadcastInGame(game_id, socketDict)
            
                    raise_exception(
                        status.HTTP_307_TEMPORARY_REDIRECT,
                        " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
                    )
            
                elif(board[1] >= 6):  # DE win when they manage to post 6 of their proclamations
                    players = dbf.get_players_game(game_id) # [PLAYERS]
                    result= {}
                    for player in players:
                        role= dbf.get_player_role(player.player_id)
                        result[player.player_nick]= role
                    socketDict2= { "WINNER": 0, "PAYLOAD": result }
                    socketDict={ "TYPE": "END_GAME", "PAYLOAD": socketDict2 }
                    await wsManager.broadcastInGame(game_id, socketDict)
                    
                    raise_exception(
                        status.HTTP_307_TEMPORARY_REDIRECT,
                        " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
                    )

                coded_game_deck= dbf.get_coded_deck(game_id)
                decoded_game_deck= dbf.get_decoded_deck(coded_game_deck)

                if(len(decoded_game_deck) < 3): # shuffles the deck if there are less than 3 cards
                    # Checks how many proclamations are posted (if they have been posted, they cant be in the deck)
                    total_phoenix= dbf.get_total_proclamations_phoenix(game_id)
                    total_death_eater= dbf.get_total_proclamations_death_eater(game_id)
                    new_deck= hf.generate_new_deck(total_phoenix, total_death_eater)
                    dbf.set_new_deck(new_deck, game_id)
                
                dbf.clean_director(player_id, game_id)


    player_nick = dbf.get_player_nick_by_id(player_id)
    return md.VoteOut(
        voteOut=vote_recive.vote,
        voteOut_game_id=game_id,
        voteOut_response=(f" Player {player_nick} has voted")
    )


@app.put(
    "/games/{game_id}/discard_card/",
    status_code = status.HTTP_200_OK,
    response_model = md.Card
)
async def discard_card(cards: md.Card, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )
    
    is_user_in_game= dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game ({game_id})")
        )

    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
            status.HTTP_409_CONFLICT,
            " You can not do this while expeliarmus stage is active"
        )

    step_turn= dbf.get_game_step_turn(game_id)
    if ("VOTATION_ENDED_NO" == step_turn):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The candidate was not approved, you can't discard card"
        )

    if not ("VOTATION_ENDED_OK" == step_turn):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " You are not in the stage of the corresponding turn"
        )

    player_id= dbf.get_player_id_from_game(user_id, game_id)
    is_minister= dbf.is_player_minister(player_id)
    is_director= dbf.is_player_director(player_id)
    if not (is_director or is_minister):
        player_nick = dbf.get_player_nick_by_id(player_id)
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            (f" Player {player_nick} is not the Director or Minister")
        )
    
    if(is_minister):
        if(1<= cards.card_discarted <=3):
            # Get 3 cards
            model_list= dbf.get_three_cards(game_id)
            dbf.discardCard(cards.card_discarted, game_id, is_minister, is_director)

            # Websocket to Director... the first two cards (from deck) //
            socket_list= [model_list.prophecy_card_0, model_list.prophecy_card_1] # Pass 2 cards as str #[card1, card2] (list of 2 str)
            socketDic= { "TYPE": "DIRECTOR_DISCARD", "PAYLOAD": socket_list}
            number_actual_director= dbf.get_game_candidate_director(game_id)
            id_actual_director= dbf.get_player_id_by_player_number(number_actual_director, game_id)
            await wsManager.sendMessage(id_actual_director, socketDic)
            
            return md.Card(
                card_discarted= cards.card_discarted
            )
        else:
            raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                (f" You don't have the corrects cards ")
            )
    elif(is_director):
        # Then he has 2 cards
        if(1<= cards.card_discarted <=2):
            dbf.discardCard(cards.card_discarted, game_id, is_minister, is_director)

            dbf.set_game_step_turn("DISCARD_ENDED", game_id) # Set step_turn

            return md.Card(
                card_discarted= cards.card_discarted
            )
        else:
            raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                (f" You don't have the corrects cards ")
            )
        

@app.put(
    "/games/{game_id}/proclamation/",
    status_code=status.HTTP_200_OK,
    response_model=md.ViewBoard
)
async def post_proclamation(
        game_id: int,
        user_id: int = Depends(auth.get_current_active_user)) -> int:

    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    is_director = dbf.is_player_director(player_id)
    if not is_director:
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            " You are not the director"
        )

    step_turn= dbf.get_game_step_turn(game_id)
    if not ("DISCARD_ENDED" == step_turn):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The cards are not discarted, you can't post"
        )

    promulged_card = dbf.remove_card_for_proclamation(game_id)
    dbf.set_last_proclamation(promulged_card, game_id)

    # board[0] phoenix - board[1] death eater
    board = dbf.add_proclamation_card_on_board(
        promulged_card,
        game_id)  

    # TODO Change for endgame
    if(board[0] >= 5): # Phoenixes win when they manage to post 5 of their proclamations
        players = dbf.get_players_game(game_id) # [PLAYERS]
        result= {}
        for player in players:
            role= dbf.get_player_role(player.player_id)
            result[player.player_nick]= role
        socketDict2= { "WINNER": 0, "PAYLOAD": result }
        socketDict={ "TYPE": "END_GAME", "PAYLOAD": socketDict2 }
        await wsManager.broadcastInGame(game_id, socketDict)
 
        raise_exception(
            status.HTTP_307_TEMPORARY_REDIRECT,
            " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
        )
   
    elif(board[1] >= 6): # DE win when they manage to post 6 of their proclamations
        players = dbf.get_players_game(game_id) # [PLAYERS]
        result= {}
        for player in players:
            role= dbf.get_player_role(player_id)
            result[player.player_nick]= role
        socketDict2= { "WINNER": 0, "PAYLOAD": result }
        socketDict={ "TYPE": "END_GAME", "PAYLOAD": socketDict2 }
        await wsManager.broadcastInGame(game_id, socketDict)
        
        raise_exception(
            status.HTTP_307_TEMPORARY_REDIRECT,
            " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
        )

    
    coded_game_deck= dbf.get_coded_deck(game_id)
    decoded_game_deck= dbf.get_decoded_deck(coded_game_deck)

    if(len(decoded_game_deck) <= 3): # shuffles the deck if there are less than 3 cards
        # Checks how many proclamations are posted (if they have been posted, they cant be in the deck)
        total_phoenix= dbf.get_total_proclamations_phoenix(game_id)
        total_death_eater= dbf.get_total_proclamations_death_eater(game_id)
        new_deck= hf.generate_new_deck(total_phoenix, total_death_eater)
        dbf.set_new_deck(new_deck, game_id)
    
    # Informs all the players what proclamation has been posted
    socketDic= { "TYPE": "PROCLAMATION", "PAYLOAD": promulged_card}
    await wsManager.broadcastInGame(game_id, socketDic)

    if not (dbf.is_expeliarmus_active(game_id) == 0):
        dbf.deactivate_expeliarmus(game_id)

    if not promulged_card:
        if (dbf.is_imperius_active(game_id) != -1):
            dbf.finish_imperius(game_id)
        dbf.set_next_minister(game_id)
        await hf.newMinister(wsManager, game_id)
            
    else:
        # Informs the minister what spell has to be casted (if any)
        actual_spell = dbf.get_spell(game_id)
        if (actual_spell == "No Spell"):  
            dbf.set_next_minister(game_id)
            await hf.newMinister(wsManager, game_id)
            
            if (dbf.is_imperius_active(game_id) != -1):
                dbf.finish_imperius(game_id)
        elif (actual_spell == "Crucio"):
            player_number_current_minister= dbf.get_actual_minister(game_id)
            player_id_current_minister= dbf.get_player_id_by_player_number(player_number_current_minister, game_id)
            sock_dict = dbf.get_player_number_crucio(game_id)
            socketDict= { "TYPE": "REQUEST_CRUCIO", "PAYLOAD": sock_dict }
            await wsManager.sendMessage(player_id_current_minister, socketDict)

        elif (actual_spell == "Imperius"):
            player_number_current_minister= dbf.get_actual_minister(game_id)
            player_id_current_minister= dbf.get_player_id_by_player_number(player_number_current_minister, game_id)
            socketDict= { "TYPE": "REQUEST_SPELL", "PAYLOAD": "IMPERIUS" }
            await wsManager.sendMessage(player_id_current_minister, socketDict)

        elif (actual_spell == "Prophecy"):
            player_number_current_minister= dbf.get_actual_minister(game_id)
            player_id_current_minister= dbf.get_player_id_by_player_number(player_number_current_minister, game_id)
            socketDict= { "TYPE": "REQUEST_SPELL", "PAYLOAD": "ADIVINATION" }
            await wsManager.sendMessage(player_id_current_minister, socketDict)

        elif (actual_spell == "Avada Kedavra"): 
            player_number_current_minister= dbf.get_actual_minister(game_id)
            player_id_current_minister= dbf.get_player_id_by_player_number(player_number_current_minister, game_id)
            socketDict= { "TYPE": "REQUEST_SPELL", "PAYLOAD": "AVADA_KEDRAVA" }
            await wsManager.sendMessage(player_id_current_minister, socketDict)
        
    dbf.set_game_step_turn("POST_PROCLAMATION_ENDED", game_id) # Set step_turn

    return md.ViewBoard(
        board_promulged_fenix=board[0],
        board_promulged_death_eater=board[1],
        board_response=" Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    )


@app.put(
    "/games/{game_id}/spell/expeliarmus",
    status_code=status.HTTP_200_OK,
    response_model=md.ResponseText
)
async def spell_expelliarmus(minister_decition: md.MinisterDecition, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    is_director = dbf.is_player_director(player_id)
    if ((not is_director) and (dbf.is_expeliarmus_active(game_id) == 0)) :
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            " You are not the director"
        )

        
    player_id = dbf.get_player_id_from_game(user_id, game_id)
    is_minister = dbf.is_player_minister(player_id)
    if ((not is_minister) and (dbf.is_expeliarmus_active(game_id) == 1)) :
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            " You are not the minister"
        )
        
    death_eater_proclamations = dbf.get_total_proclamations_death_eater(game_id) 
    if not (death_eater_proclamations == 5):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " You can not use expelliarmus, there are not enough Death Eater proclamations posted."
        )
    
    if (dbf.is_expeliarmus_active(game_id) == 2):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You can not do this, expeliarmus has been already rejected this turn"
            )
    
    if ((dbf.is_expeliarmus_active(game_id) == 1) and (minister_decition.ministerDecition is None)):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You need to make a decition as the minister"
            )

    
    if (dbf.is_expeliarmus_active(game_id) == 0):
        dbf.activate_expeliarmus(game_id)
        miniser_number = dbf.get_actual_minister(game_id)
        minister_id = dbf.get_player_id_by_player_number(miniser_number, game_id)
        minister_nick= dbf.get_player_nick_by_id(minister_id)
        socketDic = { "TYPE": "EXPELIARMUS_NOTICE", "PAYLOAD": minister_nick }
        await wsManager.broadcastInGame(game_id, socketDic)
        responseText = "Expeliarmus stage has started"

    else:
        if minister_decition.ministerDecition:
            responseText = "Expeliarmus stage has been accepted"
            dbf.add_failed_elections(game_id)
            dbf.set_next_minister_failed_election(game_id)
            await hf.newMinister(wsManager, game_id)
            # Discard 2 actual cards
            dbf.remove_card_for_proclamation(game_id)
            dbf.remove_card_for_proclamation(game_id)

            coded_game_deck= dbf.get_coded_deck(game_id)
            decoded_game_deck= dbf.get_decoded_deck(coded_game_deck)
            if(len(decoded_game_deck) < 3): # shuffles the deck if there are less than 3 cards
                # Checks how many proclamations are posted (if they have been posted, they cant be in the deck)
                total_phoenix= dbf.get_total_proclamations_phoenix(game_id)
                total_death_eater= dbf.get_total_proclamations_death_eater(game_id)
                new_deck= hf.generate_new_deck(total_phoenix, total_death_eater)
                dbf.set_new_deck(new_deck, game_id)

            dbf.deactivate_expeliarmus(game_id)
        else:
            director_number = dbf.get_actual_director(game_id)
            director_id = dbf.get_player_id_by_player_number(director_number, game_id)
            director_nick = dbf.get_player_nick_by_id(director_id)
            socketDic = { "TYPE": "EXPELIARMUS_REJECT_NOTICE", "PAYLOAD": director_nick }
            await wsManager.broadcastInGame(game_id, socketDic)
            
            # Director Normally select and post proclamation
            dbf.rejected_expeliarmus(game_id)
            responseText = "Expeliarmus stage has been rejected"

    return md.ResponseText( responseText = responseText)


@app.post(
    "/games/{game_id}/spell/crucio",
    status_code=status.HTTP_200_OK
)
async def spell_crucio(victim: md.Victim, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )
        
    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    total_players = dbf.get_game_total_players(game_id)
    # If crucio should't be called right now
    if (dbf.get_spell(game_id) != "Crucio"): 
        death_eater_proclamations = dbf.get_total_proclamations_death_eater(game_id)
        if (9 <= total_players <= 10):
            if (death_eater_proclamations == 0):
               raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " Death Eaters dont have enough proclamations posted"
                )

            if (3 <= death_eater_proclamations):
               raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " Death Eaters have too much proclamations posted"
                )   

        if (7 <= total_players <= 8):
            if (death_eater_proclamations <= 1):
               raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " Death Eaters dont have enough proclamations posted"
                )

            if (3 <= death_eater_proclamations):
               raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " Death Eaters have too much proclamations posted"
                )  

        if (total_players < 7):
            raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " The game has less than 7 players"
            )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    if not (dbf.is_player_minister(player_id)):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            "The player is not the minister :("
        )

    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You can not do this while expeliarmus stage is active"
            )

    if not (0 <= victim.victim_number < total_players):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"Player number should be between 0 and {total_players - 1}")
        )

    player_number = dbf.get_player_number_by_player_id(player_id)
    if (victim.victim_number == player_number):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            "You can not spell Crucio to yourself"
        )

    victim_id = dbf.get_player_id_by_player_number(victim.victim_number, game_id)
    victim_nick = dbf.get_player_nick_by_id(victim_id)
    if not (dbf.is_player_alive(victim_id)):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"You can not spell Crucio to {victim_nick}, is already dead")
        )

    if dbf.get_player_number_crucio(game_id) == victim.victim_number:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"You can not spell Crucio to {victim_nick}, has been already Crucified")
        )
    
    minister_nick= dbf.get_player_nick_by_id(player_id)
    socketDic= { "TYPE": "CRUCIO_NOTICE", "PAYLOAD": minister_nick }
    await wsManager.broadcastInGame(game_id, socketDic)
    
    dbf.activate_crucio(victim.victim_number, game_id)
    if dbf.get_player_role(victim_id) == 0:
        victim_role = 0
    else:
        victim_role = 1

    dbf.set_next_minister(game_id)
    await hf.newMinister(wsManager, game_id)
    dbf.set_game_step_turn("SPELL", game_id) # Set step_turn
    return md.CrucioOut(role=victim_role)


@app.put(
    "/games/{game_id}/spell/imperius",
    status_code=status.HTTP_200_OK,
    response_model=md.ResponseText
)
async def spell_imperius(victim: md.Victim, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )
        
    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    total_players = dbf.get_game_total_players(game_id)

    # If Imperius should't be called right now
    if (dbf.get_spell(game_id) != "Imperius"): 
        death_eater_proclamations = dbf.get_total_proclamations_death_eater(game_id)
        if (9 <= total_players <= 10):
            if (((7 <= total_players <= 8)) or (death_eater_proclamations < 3)):
               raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " Death Eaters dont have enough proclamations posted"
                )

            if (4 <= death_eater_proclamations):
               raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " Death Eaters have too much proclamations posted"
                )   

        if (total_players < 7):
            raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                " The game has less than 7 players"
            )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    if not (dbf.is_player_minister(player_id)):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " You are not the minister :("
        )

    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You can not do this while expeliarmus stage is active"
            )

    if not (0 <= victim.victim_number < total_players):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"Player number should be between 0 and {total_players - 1}")
        )

    player_number = dbf.get_player_number_by_player_id(player_id)
    if (victim == player_number):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            "You can not spell Imperius to yourself"
        )

    victim_id = dbf.get_player_id_by_player_number(victim.victim_number, game_id)
    victim_nick = dbf.get_player_nick_by_id(victim_id)
    if not (dbf.is_player_alive(victim_id)):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f"You can not spell Imperius to {victim_nick}, is already dead")
        )


    minister_nick= dbf.get_player_nick_by_id(player_id)
    socketDic= { "TYPE": "IMPERIUS_NOTICE", "PAYLOAD": victim_nick }
    await wsManager.broadcastInGame(game_id, socketDic)

    dbf.activate_imperius(victim.victim_number, game_id)
    dbf.set_game_step_turn("SPELL", game_id) # Set step_turn
    dbf.set_next_minister_imperius(victim.victim_number, game_id)
    await hf.newMinister(wsManager, game_id)
    return md.ResponseText(responseText = (f"spell imperius has been casted to {victim_nick}"))


@app.get(
    "/games/{game_id}/spell/prophecy",
    status_code=status.HTTP_200_OK,
    response_model=md.Prophecy
)
async def spell_prophecy(game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You can not do this while expeliarmus stage is active"
            )

    total_players = dbf.get_game_total_players(game_id)
    if (total_players > 6):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The game has more than 6 players :("
        )

    total_proclamation_DE = dbf.get_total_proclamations_death_eater(game_id)
    if (total_proclamation_DE != 3):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " Death Eaters dont have exactly three proclamations posted :("
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    if not (dbf.is_player_minister(player_id)):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            "The player is not the minister :("
        )

    minister_nick= dbf.get_player_nick_by_id(player_id)
    socketDic= { "TYPE": "ADIVINATION_NOTICE", "PAYLOAD": minister_nick }
    await wsManager.broadcastInGame(game_id, socketDic)

    dbf.set_game_step_turn("SPELL", game_id) # Set step_turn
    dbf.set_next_minister(game_id)
    await hf.newMinister(wsManager, game_id)
    return dbf.get_three_cards(game_id)


@app.put(
    "/games/{game_id}/spell/avada_kedavra",
    status_code=status.HTTP_200_OK,
    response_model=md.ResponseText
)
async def spell_avada_kedavra(victim: md.Victim, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_exists = dbf.check_game_exists(game_id)
    if not game_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The game you selected does not exist"
        )

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)
    is_player_minister = dbf.is_player_minister(player_id)
    if not is_player_minister:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " You are not the minister :("
        )
    
    if not (dbf.is_expeliarmus_active(game_id) == 0):
        raise_exception(
                status.HTTP_409_CONFLICT,
                " You can not do this while expeliarmus stage is active"
            )


    total_proclamation_DE = dbf.get_total_proclamations_death_eater(game_id)
    if (total_proclamation_DE <= 3):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " Death Eaters don't have enough proclamations posted :("
        )

    game_players = dbf.get_game_total_players(game_id)
    if not (0 <= victim.victim_number < game_players):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player number {victim.victim_number} is not between the expected number (0 to {game_players})")
        )

    victim_id = dbf.get_player_id_by_player_number(
        victim.victim_number, game_id)
    is_minister_victim = victim_id == player_id
    if is_minister_victim:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " You can't kill yourself"
        )

    victim_name = dbf.get_player_nick_by_id(victim_id)

    is_victim_alive = dbf.is_player_alive(victim_id)
    if not is_victim_alive:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You cant kill {victim_name}, is already dead")
        )

    dbf.kill_player(victim_id)
    if (dbf.get_player_role(victim_id) == 2):
        roles_dict = dbf.get_roles(game_id)
        result_dict = {"WINNER": 0, "ROLES": roles_dict}
        socketDic= { "TYPE": "ENDGAME", "PAYLOAD": result_dict }
        await wsManager.broadcastInGame(game_id, socketDic)

    else:
        minister_name = dbf.get_player_nick_by_id(player_id)
        socketDic= { "TYPE": "AVADA_KEDAVRA", "PAYLOAD": victim_name }
        await wsManager.broadcastInGame(game_id, socketDic)

        if (dbf.is_imperius_active(game_id) != -1):
            dbf.finish_imperius(game_id)

        dbf.set_next_minister(game_id)
        await hf.newMinister(wsManager, game_id)
        dbf.set_game_step_turn("SPELL", game_id) # Set step_turn
    minister_name = dbf.get_player_nick_by_id(player_id)
    return md.ResponseText(
        responseText=(
            f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")
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

@app.websocket("/websocket/{player_id}")
async def open_websocket(websocket: wsm.WebSocket, player_id: int):
    TIMEOUT = 8.0
    await websocket.accept()
    await websocket.send_json({"TYPE": "REQUEST_AUTH", "PAYLOAD": f"Timeout: {TIMEOUT}"})
    
    try:
        token = await wsm.wait_for(websocket.receive_text(), timeout=TIMEOUT)
        user_by_token = auth.get_user_from_token(token)
        user_by_player_id = dbf.get_user_by_player_id(player_id)
    except Exception:
        await websocket.send_text("Connection rejected")
        await websocket.close()
        return
    
    if (user_by_token == None or user_by_token.user_id != user_by_player_id.user_id):
        await websocket.send_text("Connection rejected")
        await websocket.close()
    else:
        await websocket.send_text("Connection Accepted")
        nick = dbf.get_player_nick_by_id(player_id)
        print(f" Player[{player_id}] ({nick}) opened their websocket connection")
        await wsManager.handleConnection(player_id, websocket)
        print(f" Player[{player_id}] ({nick}) closed their websocket connection")
    
    

@app.post("/echo/", status_code=status.HTTP_200_OK)
async def repeatInWebsocket(echo: md.Echo):
    if (echo.game_id == None):
        await wsManager.sendMessage(echo.player_id, echo.message)
    else:
        await wsManager.broadcastInGame(echo.game_id, echo.message)
    return { "RESULT" : "Message sent" }
