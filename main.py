from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import websocket_manager as wsm
import models as md
import db_functions as dbf
import authorization as auth
import helpers_functions as hf


app = FastAPI()
wsManager = wsm.WebsocketManager()

# For Integration
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

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

    is_present = dbf.is_user_in_lobby(user_id, lobby_id)
    if is_present:
        raise_exception(
            status.HTTP_409_CONFLICT,
            " You already are in the provided lobby"
        )

    if len(dbf.get_players_lobby(lobby_id)) >= dbf.get_lobby_max_players(lobby_id):
        raise_exception(
            status.HTTP_409_CONFLICT,
            " The lobby you selected is already fullfilled"
        )

    lobby = dbf.join_lobby(user_id, lobby_id)
    lobby_name = lobby.lobby_name
    lobby_id = lobby.lobby_id
    player_id = dbf.get_player_id_from_lobby(user_id, lobby_id)

    player_nick= dbf.get_player_nick_by_id(player_id)
    socketDic= { "TYPE": "NEW_PLAYER_JOINED", "PAYLOAD": player_nick }
    await wsManager.broadcastInLobby(lobby_id, socketDic)

    return md.JoinLobby(
        joinLobby_name=lobby_name,
        joinLobby_player_id=player_id,
        joinLobby_result=(f" Welcome to {lobby_name}")
    )

@app.get(
    "/lobby/{lobby_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_lobby_information(lobby_id: int, user_id: int = Depends(auth.get_current_active_user)):
    if not dbf.is_user_in_lobby(user_id, lobby_id):
        raise_exception(status.HTTP_412_PRECONDITION_FAILED,
        "You are not on the lobby requested.")    
        
    players = dbf.get_players_lobby(lobby_id)
    playersDict = {}
    i = 0
    for player in players:
        pl = {
            "player_nick" : player.player_nick,
            "player_connected": True   #TODO read with websocket manager if connected
        }
        playersDict[i] = pl
        i += 1
    retDict = {
        "lobby_name" : dbf.get_lobby_by_id(lobby_id).lobby_name,
        "lobby_players": playersDict
    }
    return retDict

"""
# player entity
class Player(db.Entity):
    player_id               = PrimaryKey(int, auto=True)
    player_number           = Optional(int)    # Definied order
    player_nick             = Required(str)    # = userName Depends on User
    player_nick_points      = Required(int)    # Starts in 0, max 10
    player_role             = Required(int)    # = -1 No asigned
    player_is_alive         = Required(bool)   # = True
    player_chat_blocked     = Required(bool)   # = False
    player_is_candidate     = Required(bool)   #REVIEW
    player_has_voted        = Required(bool)   #REVIEW True if the player has voted
    player_vote             = Required(bool)   #REVIEW Actual vote
    player_director         = Required(bool)
    player_minister         = Required(bool)
    player_game             = Optional(Game)   # one to many relation with Player-Game
    player_lobby            = Optional(Lobby)  # one to many relation with Player-Game, is optional because the Lobby is deleted when game starts   
    player_user             = Required(User)   # one to many relation with Player-User {...}
class Lobby(db.Entity):
    lobby_id                = PrimaryKey(int, auto = True)
    lobby_name              = Required(str, unique=True)
    lobby_max_players       = Optional(int, default=10)   # <=10
    lobby_min_players       = Optional(int, default=5)    # >=5
    lobby_creator           = Required(int)                 # user_id of the creator
    lobby_user              = Set(User)                     # many to many relation with Lobby-User, we use '' because Player is declarated after this call
    lobby_players           = Set('Player')                 # one to many relation with Lobby-Player, we use '' because Player is declarated after this call
"""



@app.post(
    "/lobby/{lobby_id}/change_nick",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.ChangeNick
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
            (f" You changed your nick too many times >:C")
        )

    nick_taken = dbf.check_nick_exists(lobby_id, new_nick.nick)
    if nick_taken:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " The nick you selected is already taken"
        )

    old_nick = dbf.get_player_nick_by_id(player_id)
    nick_points = dbf.change_nick(player_id, new_nick.nick)

    socketDict2= { "OLD_NICK": old_nick, "NEW_NICK": new_nick }
    socketDict= { "TYPE": "CHANGED_NICK", "PAYLOAD": socketDict2 }
    await wsManager.broadcastInLobby(lobby_id, socketDict)

    return md.ChangeNick(
        changeNick_result=(
            f" Your nick has been sucessfully changed to {new_nick.nick}, you can change it {nick_points} more times")
    )


@app.delete(
    "/lobby/{lobby_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=md.LeaveLobby
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
        # TODO 2) Uncoment, test with integration Front-Back
        socketDic= { "TYPE": "LEAVE_LOBBY", "PAYLOAD": nick} # REVIEW
        await wsManager.broadcastInLobby(lobby_id, socketDic)
        
        return md.LeaveLobby(
            leaveLobby_response=(f" Player {nick} has left lobby {lobby_id} and was the creator, so the lobby was destroyed >:C")
        )

    dbf.leave_lobby(actual_player)

    # TODO 2) Uncoment, test with integration Front-Back
    socketDic= { "TYPE": "LEAVE_LOBBY", "PAYLOAD": nick} # REVIEW
    await wsManager.broadcastInLobby(lobby_id, socketDic)

    return md.LeaveLobby(
        leaveLobby_response=(f" Player {nick} has left lobby {lobby_id}")
    )


# game endpoints
@app.delete(
    "/lobby/{lobby_id}/start_game",
    status_code=status.HTTP_200_OK,
    response_model=md.GameOut
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

    # Changed game_id to lobby_id because after the line 405 the lobby has deleted and the 
    # USERS need to know this on Lobby. Tell me if they need know it when they are on the game (and not on lobby)
    socketDict= { "TYPE": "START_GAME", "PAYLOAD": lobby_id }
    await wsManager.broadcastInLobby(lobby_id, socketDict)

    dbf.insert_game(
        md.ViewGame(game_total_players=game_player_quantity),
        lobby_id
    )

    return md.GameOut(gameOut_result=" Your game has been started")


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


# board endpoints
@app.post(
    "/games/{game_id}/select_director/",
    status_code=status.HTTP_200_OK,
    response_model=md.SelectMYDirector
)
async def select_director(player_number: md.PlayerNumber, game_id: int, user_id: int = Depends(auth.get_current_active_user)) -> int:
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
    if not (0 <= player_number.playerNumber < game_players):  # player_number
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" Player number {player_number} is not between the expected number (0 to {game_players})")
        )

    player_id = dbf.get_player_id_by_player_number(
        player_number.playerNumber, game_id)
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
            (f" Player {player_nick} can't be selected as director candidate because is the acutal minister, or was selected as minister or director in the last turn")
        )

    dbf.select_candidate(player_id, player_number.playerNumber, game_id)

    dbf.reset_votes(game_id)

    return md.SelectMYDirector(
        dir_player_number=player_number.playerNumber,
        dir_game_id=game_id,
        dir_game_response=(f" Player {player_nick} is now director candidate")
    )


#REVIEW
@app.put(
    "/games/{game_id}/select_director/vote",
    status_code=status.HTTP_200_OK,
    response_model=md.VoteOut
)
async def vote(vote_recive: md.Vote, game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    player_id = dbf.get_player_id_from_game(user_id, game_id)
    player_nick = dbf.get_player_nick_by_id(player_id)
    
    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
        )

    is_player_alive = dbf.is_player_alive(player_id)
    if not is_player_alive:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are dead in the game ({game_id}), you can't vote")
        )

    actual_vote= dbf.check_has_voted(player_id)
    if actual_vote:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You have already voted in the game ({game_id}), you can't vote more than 2 times")
        )
    
    actual_votes = dbf.player_vote(vote_recive.vote, player_id, game_id) 

    if (actual_votes == (dbf.get_game_total_players(game_id))):
        status_votes= dbf.get_status_vote(game_id)
        #! REVIEW @Agus @Cande
        players = dbf.get_players_game(game_id) # [PLAYERS]
        socketDict2 = {}
        for player in players:
            player_vote = dbf.get_actual_vote_of_player(player_id) # get vote
            socketDict2[player.player_nick] = player_vote
        scoketDict = { "TYPE": "ELECTION_RESULT", "VOTES": socketDict2 }
        await wsManager.broadcastInGame(game_id, scoketDict)
        
        if(status_votes > 0): # Acepted candidate
            print(" Successful Election...")
            actual_candidate= dbf.get_game_candidate_director(game_id)
            player_id_candidate= dbf.get_player_id_by_player_number(actual_candidate, game_id)
            
            dbf.reset_candidate(player_id_candidate, game_id) # Reset candidate
            dbf.reset_votes(game_id) # Reset votes
            dbf.select_director(player_id_candidate, actual_candidate, game_id)
              
            # Get 3 cards
            model_list= dbf.get_three_cards(game_id)
            # Pass 3 cards as str #[card1, card2, card3] (list of 3 str) 
            socket_list= list(model_list.prophecy_card_0, model_list.prophecy_card_1, model_list.prophecy_card_2)
            socketDic={ "TYPE": "MINISTER_DISCARD", "PAYLOAD": socket_list }
            await wsManager.sendMessage(player_id_candidate, socketDic)
        else:
            print(" Failed Election...")
            dbf.add_failed_elections(game_id) # +1 game_failed_elections on db
            dbf.set_next_minister_failed_election(game_id)
            
            player_number_candidate= dbf.get_game_candidate_director(game_id)
            player_id_candidate= dbf.get_player_id_by_player_number(player_number_candidate, game_id)
            dbf.reset_candidate(player_id_candidate, game_id) # Reset candidate
            dbf.reset_votes(game_id) # Reset votes
            
            #! REVIEW @Agus @Cande
            players = dbf.get_players_game(game_id) # [PLAYERS]
            subdict = {}
            for player in players:
                player_vote = dbf.get_actual_vote_of_player(player_id) # get vote
                subdict[player.player_nick] = player_vote
            finalDict = { "TYPE": "ELECTION_RESULT", "VOTES": subdict }
            await wsManager.broadcastInGame(game_id, finalDict)

    return md.VoteOut(
        voteOut=vote_recive.vote,
        voteOut_game_id=game_id,
        voteOut_response=(f" Player {player_nick} has voted")
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
            #print(discarted_cards) #TODO Removes, test with integration Front-Back

            # Websocket to Director... the first two cards (from deck) //
            # Get 3 cards
            model_list= dbf.get_three_cards(game_id)
            # Pass 2 cards as str #[card1, card2] (list of 2 str) 
            socket_list= list(model_list.prophecy_card_0, model_list.prophecy_card_1)
            socketDic= { "TYPE": "DIRECTOR_DISCARD", "PAYLOAD": socket_list}
            # Get actual Director
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
    status_code=status.HTTP_200_OK,
    response_model=md.ViewBoard
)
async def post_proclamation(
        is_phoenix_procl: md.ProclamationCard,
        game_id: int,
        user_id: int = Depends(auth.get_current_active_user)) -> int:

    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
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
    board = dbf.add_proclamation_card_on_board(
        is_phoenix_procl.proclamationCard_phoenix,
        game_id)  # is_phoenix_procl

    # TODO Change for endgame
    if(board[0] >= 5): # Phoenixes won
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
            " Free Dobby appears and congratulates the Phoenixes with a sock, hagrid is happy too ♥ Dracco Malfloy disturbs an Hippogriff peace, gets 'beaked' and cries"
        )
    elif(board[1] == 4):  # DE win when total_players = 5 or 6
        if (5 <= dbf.get_game_total_players(game_id) <= 6):
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
    elif(board[1] == 5):  # DE win when total_players = 7 or 8
        if (7 <= dbf.get_game_total_players(game_id) <= 8):
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
    elif(board[1] >= 6):  # DE win when total_players = 9 or 10
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
    discarted_deck= decoded_game_deck

    dbf.remove_card_for_proclamation(game_id, is_director)

    if(len(discarted_deck) <= 3): # Rule game
        # Checks how many proclamation have
        total_phoenix= dbf.get_total_proclamations_phoenix(game_id)
        total_death_eater= dbf.get_total_proclamations_death_eater(game_id)
        discarted_deck= hf.generate_new_deck(total_phoenix, total_death_eater)
        dbf.set_new_deck(discarted_deck, game_id)

    # Next minister
    if (board[1] < 4):  # Don't Set next minister yet, first cast Avada Kedavra
        # "Upper"
        player_number_current_minister= dbf.get_actual_minister(game_id)
        player_id_current_minister= dbf.get_player_id_by_player_number(player_number_current_minister, game_id)
        socketDict= { "TYPE": "REQUEST_SPELL", "PAYLOAD": "ADIVINATION" }
        await wsManager.sendMessage(player_id_current_minister, socketDict) # REVIEW
        dbf.set_next_minister(game_id) # REVIEW @Diego Checks if the code line go upper or here. Read rule games <3

    # Prophecy // Adivination
    if ( (dbf.get_game_total_players(game_id))== 5 or 6 ):
        player_number_current_minister= dbf.get_actual_minister(game_id)
        player_id_current_minister= dbf.get_player_id_by_player_number(player_number_current_minister, game_id)
        socketDict= { "TYPE": "REQUEST_SPELL", "PAYLOAD": "AVADA_KEDRAVA" }
        await wsManager.sendMessage(player_id_current_minister, socketDict)

    socketDic= { "TYPE": "PROCLAMATION", "PAYLOAD": is_phoenix_procl.proclamationCard_phoenix }
    await wsManager.broadcastInGame(game_id, socketDic)

    return md.ViewBoard(
        board_promulged_fenix=board[0],
        board_promulged_death_eater=board[1],
        board_response=" Proclamation card was promulged correctly (ง'-'︠)ง ≧◉ᴥ◉≦"
    )


@app.get(
    "/games/{game_id}/spell/prophecy",
    status_code=status.HTTP_200_OK,
    response_model=md.Prophecy
)
async def spell_prophecy(game_id: int, user_id: int = Depends(auth.get_current_active_user)):
    is_user_in_game = dbf.is_user_in_game(user_id, game_id)
    if not is_user_in_game:
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            (f" You are not in the game you selected ({game_id})")
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

    return dbf.get_three_cards(game_id)


@app.put(
    "/games/{game_id}/spell/avada_kedavra",
    status_code=status.HTTP_200_OK,
    response_model=md.AvadaKedavra
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

    total_proclamation_DE = dbf.get_total_proclamations_death_eater(game_id)
    if (total_proclamation_DE <= 3):
        raise_exception(
            status.HTTP_412_PRECONDITION_FAILED,
            " Death Eaters don't have enough proclamations posted :("
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
    dbf.set_next_minister(game_id)
    minister_name = dbf.get_player_nick_by_id(player_id)
    socketDic= { "TYPE": "AVADA_KEDAVRA", "PAYLOAD": victim_name }
    await wsManager.broadcastInGame(game_id, socketDic)

    return md.AvadaKedavra(
        AvadaKedavra_response=(
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
    await websocket.accept()
    await websocket.send_text("Send auth token")
    try:
        token = await wsm.wait_for(websocket.receive_text(), timeout=8.0)
    except wsm.timeoutErr:
        await websocket.send_text("Connection rejected. No auth token received")
        await websocket.close()
        return
    user_by_token = auth.get_user_from_token(token)
    user_by_player_id = dbf.get_user_by_player_id(player_id)
    if (user_by_token == None or user_by_token.user_id != user_by_player_id.user_id):
        await websocket.send_text("Connection rejected. Wrong authorization")
        await websocket.close()
    else:
        await websocket.send_text("Connection Accepted")
        nick = dbf.get_player_nick_by_id(player_id)
        print(f" Player[{player_id}] ({nick}) opened their websocket connection")
        await wsManager.handleConnection(player_id, websocket)
        print(f" Player[{player_id}] ({nick}) closed their websocket connection")
