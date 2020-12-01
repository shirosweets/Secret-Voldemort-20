from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK
from asyncio import wait_for
from typing import List, Dict, Union
import db_functions as dbf

class WebsocketManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = dict() # key is player_id


    async def disconnect(self, player_id : int):
        try:
            websocket = self.connections[player_id]
            await websocket.close()
        except KeyError:
            pass
        self.connections.pop(player_id, None)

    
    def isPlayerConnected(self, player_id: int) -> bool:
        try:
            self.connections[player_id]
            return True
        except Exception:
            return False
                

    async def handleConnection(self, player_id: int, websocket: WebSocket):
        self.connections[player_id] = websocket
        try:
            while True:
                chat = await websocket.receive_text()
                nick = dbf.get_player_nick_by_id(player_id)
                dic = { "TYPE": "CHAT", "PAYLOAD": f"({nick}): {chat}"}
                await self.broadcastPlayingWith(player_id, dic, include_current_player=True)
        except WebSocketDisconnect:
            #await self.disconnect(player_id)
            self.connections.pop(player_id, None)
        except ConnectionClosedOK:
            #await self.disconnect(player_id)
            self.connections.pop(player_id, None)


    async def sendMessage(self, player_id : int, message: Union[str, dict]):
        try:
            connection = self.connections[player_id]
            if (type(message) == type(" String")):
                await connection.send_text(message)
            else:
                if(message["TYPE"] != "CHAT"):
                    dbf.save_last_message_ws(player_id, message)
                else:
                    await connection.send_json(message)
        except KeyError:
            print(f"I can't send '{message}' to player_id = {player_id}'")

    # async def broadcastChat(self, player_id: int, message: Union[str, dict]):
    #     # Recibir el mensaje a todos los jugadores independientemente si está vivo o no

    #     try:
    #         # Cuando el jugador que envía el mensaje está vivo
    #         if(True):
    #             print("Estoy vivo :D")
    #         # Cuando el jugador que envía el mensaje está muerto
    #         else:
    #             print("Estoy muerto :(")
    #     except KeyError:
    #         print(f"I can't send '{message}' to player_id = {player_id}'")

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
        print(f" broadcasting to lobby {lobby_id}")
        players_ids = [p.player_id for p in dbf.get_players_lobby(lobby_id)]
        await self.__broadcast(players_ids, message)


    async def broadcastInGame(self, game_id : int, message : Union[str, dict]):
        players_ids = [p.player_id for p in dbf.get_players_game(game_id)]
        await self.__broadcast(players_ids, message)


    async def __broadcast(self, p_ids: List[int], message: Union[str, dict]):
        for p_id in p_ids:
            try:
                await self.sendMessage(p_id, message)
                print(f" Sent {message} to player {p_id}")
            except KeyError:
                print(f" Tried to send a message to Player[{p_id}] but websocket is disconnected")
