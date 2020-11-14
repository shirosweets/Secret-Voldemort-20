from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK
from asyncio import wait_for
from typing import List, Dict, Union
import db_functions as dbf

class WebsocketManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = dict() # key is player_id


    def disconnect(self, player_id : int, ws: WebSocket):
        self.connections.pop(player_id, None)
    

    async def handleConnection(self, player_id: int, websocket: WebSocket):
        self.connections[player_id] = websocket
        try:
            while True:
                chat = await websocket.receive_text()
                nick = dbf.get_player_nick_by_id(player_id)
                chat = f"({nick}): {chat}"
                await self.broadcastPlayingWith(player_id, chat)
        except WebSocketDisconnect:
            self.disconnect(player_id, websocket)
        except ConnectionClosedOK:
            self.disconnect(player_id, websocket)


    async def sendMessage(self, player_id : int, message: Union[str, dict]):
        connection = self.connections[player_id]
        if (type(message) == type(" String")):
            await connection.send_text(message)
        else:
            await connection.send_json(message)


    async def broadcastPlayingWith(self, player_id : int, message : Union[str, dict], include_current_player : bool = False):
        """Sends message to all players that belong on the same game/lobby of this player. Must be called with await"""
        pl_ids = dbf.get_players_id_playing_with_player_id(player_id)

        if include_current_player:
            pl_ids.append(player_id)
        
        for pl_id in pl_ids:
            try:
                await self.sendMessage(pl_id, message)
            except KeyError:
                print(f" Tried to send a message to Player[{pl_id}] but websocket is disconnected")


    async def broadcastInLobby(self, lobby_id : int, message : Union[str, dict]):
        players_ids = [p.player_id for p in dbf.get_players_lobby(lobby_id)]
        await self.__broadcast(players_ids, message)


    async def broadcastInGame(self, game_id : int, message : Union[str, dict]):
        players_ids = [p.player_id for p in dbf.get_players_game(game_id)]
        await self.__broadcast(players_ids, message)


    async def __broadcast(self, p_ids: List[int], message: Union[str, dict]):
        for p_id in p_ids:
            try:
                await self.sendMessage(p_id, message)
            except KeyError:
                print(f" Tried to send a message to Player[{p_id}] but websocket is disconnected")
