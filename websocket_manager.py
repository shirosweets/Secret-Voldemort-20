from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK
from typing import Dict, Union
import db_functions as dbf

class WebsocketManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = dict() # key is player_id
    
    async def connect(self, player_id : int, ws: WebSocket):
        await ws.accept()
        self.connections[player_id] = ws
        await ws.send_text(" Socket Connection Accepted")

    def disconnect(self, player_id : int, ws: WebSocket):
        self.connections.pop(player_id, None)

    def isPlayerConnected(self, player_id : int):
        try:
            self.connections[player_id]
            return True
        except KeyError:
            return False

    async def sendMessage(self, player_id : int, message: Union[str, dict]):
        connection = self.connections[player_id]
        if (type(message) == type(" String")):
            await connection.send_text(message)
        else:
            await connection.send_json(message)

    # TODO : At some point someone might leave while this executes so this would raise a key error. We should add a Exception to deal with that    
    async def broadcastPlayingWith(self, player_id : int, message : Union[str, dict], exclude_current_player : bool = False):
        """Sends message to all players that belong on the same game/lobby of this player. Must be called with await"""
        #? Maybe add a function specifically for this mess?
        lobby = dbf.get_lobby_by_player_id(player_id)
        if lobby == None:
            game = dbf.get_game_by_player_id(player_id)
            players_id = [player.player_id for player in dbf.get_players_game(game)]
        else:
            players_id = [player.player_id for player in dbf.get_players_lobby(game)]
        
        if exclude_current_player:
            players_id.remove(player_id)
        
        for p_id in players_id:
            await self.sendMessage(p_id, message)

    async def broadcastInLobby(self, lobby_id : int, message : Union[str, dict]):
        players = dbf.get_players_lobby(lobby_id)
        for player in players:
            await self.sendMessage(player.player_id, message)

    async def broadcastInGame(self, game_id : int, message : Union[str, dict]):
        players = dbf.get_players_game(game_id)
        for player in players:
            await self.sendMessage(player.player_id, message)
