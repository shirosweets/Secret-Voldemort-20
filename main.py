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
        raise_exception(
            status.HTTP_400_BAD_REQUEST, 
            ' Can not parse username'
        )
            
    if not new_user.valid_format_password():
        raise_exception(
            status.HTTP_400_BAD_REQUEST, 
            ' Can not parse password'
        )
    
    if dbf.check_email_exists(new_user.userIn_email):
        raise_exception(
            status.HTTP_409_CONFLICT,
            ' The email already registered'
        )
    
    if dbf.check_username_exists(new_user.userIn_username):
        raise_exception(
            status.HTTP_409_CONFLICT,
            ' Username already registered'
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
          status_code = status.HTTP_200_OK,
          response_model = md.Token
)
async def login(login_data: auth.OAuth2PasswordRequestForm = auth.Depends()):
    user = dbf.get_user_by_email(login_data.username)
    if (user is None) or (not auth.verify_password(login_data.password, user.user_password)):
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            'Email does not exist or bad password', 
            {"Authorization": "Bearer"}
        )

    access_token_expires = auth.timedelta(minutes = auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
                        data = {"sub": user.user_email},
                        expires_delta = access_token_expires
                        )
    return {"access_token": access_token, "token_type": "Bearer"}


# lobby endpoints
@app.post(
    "/lobby/",
    status_code = status.HTTP_201_CREATED,
    response_model = md.LobbyOut
)
async def create_new_lobby(lobby_data: md.LobbyIn, user_id: int = Depends(auth.get_current_active_user)) -> int:
    name_check = dbf.exist_lobby_name(lobby_data.lobbyIn_name)
    max_check = dbf.check_max_players(lobby_data.lobbyIn_max_players)
    min_check = dbf.check_min_players(lobby_data.lobbyIn_min_players, lobby_data.lobbyIn_max_players)
    
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
    
    return md.LobbyOut(
        lobbyOut_Id = new_lobby.lobby_id,
        lobbyOut_name = lobby_data.lobbyIn_name,
        lobbyOut_result = " Your new lobby has been succesfully created!"
    )


@app.post(
    "/lobby/list_lobbies/",
    status_code = status.HTTP_200_OK,
    response_model = md.LobbyDict
)
async def list_lobbies(wantedLobbies: md.WantedLobbies, user_id: int = Depends(auth.get_current_active_user)):
    start_from = wantedLobbies.WantedLobbies_from
    end_at = wantedLobbies.WantedLobbies_end_at
    if not (end_at is None):    
        if start_from > end_at:
            raise_exception(
                status.HTTP_400_BAD_REQUEST, 
                "start_from value must be bigger than end_at value"
            )

    lobby_dict = dbf.get_lobbies_dict(start_from, end_at)
    return md.LobbyDict(lobbyDict = lobby_dict)


@app.post(
    "/lobby/{lobby_id}/",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = md.JoinLobby
)
async def join_lobby(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    lobby_exists = dbf.check_lobby_exists(lobby_id)
    if not lobby_exists:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The lobby you selected does not exist"
        )
        
    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if is_present:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " You already are in the provided lobby"
        )
    
    lobby_name = dbf.join_lobby(user_id, lobby_id)
    return md.JoinLobby(
        joinLobby_name = lobby_name,
        joinLobby_result = (f" Welcome to {lobby_name}")
    )


@app.post(
    "/lobby/{lobby_id}/change_nick",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = md.ChangeNick
)
async def change_nick(lobby_id: int, new_nick: md.Nick, user_id: int = Depends(auth.get_current_active_user)):
    if not (4 <= len(new_nick.nick) <=20):
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

    is_user_in_lobby= dbf.is_user_in_lobby(user_id, lobby_id)
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
            (f" You changed your nick too many times >:C")
        )
        
    nick_taken= dbf.check_nick_exists(lobby_id, new_nick.nick)
    if nick_taken:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The nick you selected is already taken"
        )

    #TODO 1) Uncoment, test with integration Front-Back
    # old_nick = dbf.get_player_nick_by_id(player_id)
    nick_points = dbf.change_nick(player_id, new_nick.nick)

    #TODO 1) Uncoment, test with integration Front-Back
    # await wsManager.broadcastInLobby(lobby_id, f" {old_nick} changed its nick to: {new_nick}")

    return md.ChangeNick(
            changeNick_result = (f" Your nick has been sucessfully changed to {new_nick.nick}, you can change it {nick_points} more times")
        )

    
@app.delete(
    "/lobby/{lobby_id}",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = md.LeaveLobby
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
    if (actual_player == 0):  # 0: is not on lobby (actual_player is not 0)
        raise_exception(
            status.HTTP_400_BAD_REQUEST,
            (f" User {user_id} was not in lobby {lobby_id}")
        )

    nick = dbf.get_player_nick_by_id(actual_player)

    if dbf.is_player_lobby_owner(user_id, lobby_id):
        dbf.leave_lobby(actual_player)
        dbf.delete_lobby(lobby_id)   
        #TODO 2) Uncoment, test with integration Front-Back
        # await wsManager.broadcastInLobby(lobby_id, (f" {nick} has left the lobby"))
        return md.LeaveLobby(
            leaveLobby_response = (f" Player {nick} has left lobby {lobby_id} and was the creator, so the lobby was destroyed >:C")
        )

    dbf.leave_lobby(actual_player)
    dbf.delete_lobby(lobby_id)   
        
    #TODO 2) Uncoment, test with integration Front-Back
    # await wsManager.broadcastInLobby(lobby_id, (f" {nick} has left the lobby"))

    return md.LeaveLobby(
            leaveLobby_response = (f" Player {nick} has left lobby {lobby_id}")
        )


# game endpoints
@app.delete(
    "/lobby/{lobby_id}/start_game",
    status_code = status.HTTP_200_OK,
    response_model = md.GameOut
)
async def start_game(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
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
            " List of players should be between 5 and 10"
        )

    dbf.insert_game(
        md.ViewGame(game_total_players = game_player_quantity),
        lobby_id
    )
    
    return md.GameOut(gameOut_result = " Your game has been started")


# board endpoints
@app.post(
    "/games/{game_id}/select_director/",
    status_code = status.HTTP_200_OK,
    response_model = md.SelectMYDirector
)
async def select_director(player_number: md.PlayerNumber, game_id: int, user_id: int = Depends(auth.get_current_active_user)) -> int:
    # REVIEW Added user in game check
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

    game_players = dbf.get_game_total_players(game_id)
    if not (0 <= player_number.playerNumber < game_players): #player_number
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
            (f" Player {player_nick} can't be selected as director, {player_nick} is dead")
        )

    can_player_be_director = dbf.can_player_be_director(player_number.playerNumber, game_id)
    if can_player_be_director:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player {player_nick} can't be selected as director because is the acutal minister, or was selected as minister or director in the last turn")
            )

    dbf.select_director(player_id, player_number.playerNumber, game_id)
    
    return md.SelectMYDirector(
        dir_player_number = player_number.playerNumber,
        dir_game_id = game_id,
        dir_game_response = (f" Player {player_nick} is now director")
    )


#REVIEW
@app.put(
    "/games/{game_id}/discard_card/",
    status_code = status.HTTP_200_OK,
    response_model = md.Card
)
async def discard_card(cards: md.Card, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    is_user_in_game= dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game ({game_id})")
        )

    player_id= dbf.get_player_id_from_game(user_id, game_id)
    is_minister= dbf.is_player_minister(player_id)
    is_director= dbf.is_player_director(player_id)
    
    if(is_minister): # Checks if the current players is the Minister
        if(1<= cards.card_discarted <=3): # Checks if the card is between 1 - 3
            print(f"\n Minister: Discarding the card...")          
            # Discard the card from deck  ...
            discarted_cards= dbf.discardCard(cards.card_discarted, game_id, is_minister, is_director)
            # get_three_cards 2 first cards
            print(discarted_cards) #TODO Removes, test with integration Front-Back
            #TODO 4) Uncoment, test with integration Front-Back
            # Websocket to Director... the first two cards (from deck) //
            #await wsManager.broadcastInGame(game_id, (f" Minister send 2 cards to Director..."))
            return md.Card(
                card_discarted= cards.card_discarted
            )
        else:
            raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                (f" You don't have the corrects cards ")
            )
    # He recived 2 cards   
    elif(is_director): # Checks if the current players is the Director
        # Then he have 2 cards
        if(1<= cards.card_discarted <=2): # Checks if the card is between 1 - 2
            print(f"\n Director: Discarding the card...")
            # Discard the card from deck  ...
            discarted_cards= dbf.discardCard(cards.card_discarted, game_id, is_minister, is_director)
            # get_three_cards 1 first card ...
            return md.Card(
                card_discarted= cards.card_discarted
            )
        elif not is_director and not is_minister:
            player_nick = dbf.get_player_nick_by_id(player_id)
            raise_exception(
                status.HTTP_401_UNAUTHORIZED,
                (f" Player {player_nick} is not the Director or Minister")
            )
        else:
            raise_exception(
                status.HTTP_412_PRECONDITION_FAILED,
                (f" You don't have the corrects cards ")
            )


@app.put(
    "/games/{game_id}/proclamation/",
    status_code = status.HTTP_200_OK,
    response_model = md.ViewBoard
)
async def post_proclamation(
            is_phoenix_procl: md.ProclamationCard, 
            game_id: int, 
            user_id: int = Depends(auth.get_current_active_user)) -> int:    

    is_user_in_game= dbf.is_user_in_game(user_id, game_id)

    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    player_id = dbf.get_player_id_from_game(user_id, game_id)

    is_director = dbf.is_player_director(player_id)
    if not is_director:
        player_nick = dbf.get_player_nick_by_id(player_id)
        raise_exception(
            status.HTTP_401_UNAUTHORIZED,
            (f" Player {player_nick} is not the director")
        )
    
    # board[0] phoenix - board[1] death eater
    board = dbf.add_proclamation_card_on_board(is_phoenix_procl.proclamationCard_phoenix, game_id) #is_phoenix_procl

    ##!! Finish game with proclamations ##
    #TODO Change for endgame
    if(board[0] >= 5):
        print("\n >>> The Phoenixes won!!! <<<\n")
        # Message from Phoenixes won
        print(" Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥\n")
        # Message "Death Eaters losed"
        print(" Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries")
        raise_exception(
            status.HTTP_307_TEMPORARY_REDIRECT,
            " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
        )
    elif(board[1] == 4):  # DE win when total_players = 5 or 6
        if (5 <= dbf.get_game_total_players(game_id) <= 6):
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message "Death Eaters won"
            print(" Sirius Black is dead\n")
            # Mesasage "Phoenixes losed"
            print(" Hagrid and Dobby (with a dirty and broken sock) die")
            raise_exception(
                status.HTTP_307_TEMPORARY_REDIRECT,
                " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
            )
    elif(board[1] == 5):  # DE win when total_players = 7 or 8
        if (7 <= dbf.get_game_total_players(game_id) <= 8):
            print("\n >>> Death Eaters won!!! <<<\n")
            # Message "Death Eaters won"
            print(" Sirius Black is dead\n")
            # Mesasage "Phoenixes losed"
            print(" Hagrid and Dobby (with a dirty and broken sock) die")
            raise_exception(
                status.HTTP_307_TEMPORARY_REDIRECT,
                " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
            )
    elif(board[1] >= 6):  # DE win when total_players = 9 or 10
        print("\n >>> Death Eaters won!!! <<<\n")
        # Message "Death Eaters won"
        print(" Sirius Black is dead\n")
        # Mesasage "Phoenixes losed"
        print(" Hagrid and Dobby (with a dirty and broken sock) die")
        raise_exception(
            status.HTTP_307_TEMPORARY_REDIRECT,
            " Sirius Black is dead, Hagrid and Dobby (with a dirty and broken sock) die"
        )
    
    coded_game_deck= dbf.get_coded_deck(game_id)
    decoded_game_deck= dbf.get_decoded_deck(coded_game_deck)
    discarted_deck= decoded_game_deck

    dbf.remove_card_for_proclamation(game_id, is_director)

    if(len(discarted_deck) <= 3): # Rule game
        # Checks how many proclamation have
        total_phoenix= dbf.get_total_proclamations_phoenix(game_id)
        total_death_eater= dbf.get_total_proclamations_death_eater(game_id)
        discarted_deck= hf.generate_new_deck(total_phoenix, total_death_eater)
        dbf.set_new_deck(discarted_deck, game_id)

    # Next minister
    if (board[1] < 4): # Don't Set next minister yet, first cast Avada Kedavra
        dbf.set_next_minister(game_id)

    return md.ViewBoard(
        board_promulged_fenix=board[0],
        board_promulged_death_eater=board[1],
        board_response=" Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    )


@app.get(
    "/games/{game_id}/spell/prophecy",
    status_code= status.HTTP_200_OK,
    response_model = md.Prophecy
)
async def spell_prophecy(game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    # REVIEW Added user in game check
    is_user_in_game= dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    total_players= dbf.get_game_total_players(game_id)
    if (total_players>6):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
           " The game has more than 6 players :("
        )

    total_proclamation_DE = dbf.get_death_eaters_proclamations(game_id)
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
    
    return dbf.get_three_cards(game_id)


@app.put(
    "/games/{game_id}/spell/avada_kedavra",
    status_code= status.HTTP_200_OK,
    response_model = md.AvadaKedavra
)
async def spell_avada_kedavra(victim: md.Victim, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    game_players = dbf.get_game_total_players(game_id)
    if not (0 <= victim.victim_number < game_players):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player number {victim.victim_number} is not between the expected number (0 to {game_players})")
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
    
    total_proclamation_DE = dbf.get_death_eaters_proclamations(game_id)
    if (total_proclamation_DE <= 3):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " Death Eaters don't have enough proclamations posted :("
        )
    
    victim_id = dbf.get_player_id_by_player_number(victim.victim_number, game_id)
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
    
    dbf.set_next_minister(game_id)

    minister_name = dbf.get_player_nick_by_id(player_id)
    #TODO 3) Uncoment, test with integration Front-Back
    # await wsManager.broadcastInGame(game_id, (f" Minister {minister_name} had a wand duel against {victim_name} and won, now {victim_name} is dead"))

    return md.AvadaKedavra(
        AvadaKedavra_response = (f"You, {minister_name} had a wand duel against {victim_name} and you won, now {victim_name} is dead")
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

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: wsm.WebSocket, player_id: int):
    await wsManager.connect(player_id, websocket)
    try:
        while True:
            chatMsg = await websocket.receive_text()
            #*TODO for when we implement chat
            print(f" Player {player_id} sent: {chatMsg}")
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
