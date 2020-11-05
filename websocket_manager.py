from fastapi import WebSocket
#from threading import Thread, Condition, RLock, current_thread
from time import sleep
from typing import Dict, Union

class WebsocketManager:
    def __init__(self):
        #Dict[str, float] // key is player_id
        self.connections: Dict[int, WebSocket] = dict()

    async def connect(self, player_id : int, ws: WebSocket):
        await ws.accept()
        self.connections[player_id] = ws

    def disconnect(self, player_id : int, ws: WebSocket):
        self.connections.pop(player_id, None)

    async def sendMessage(self, player_id : int, message: Union[str, dict]):
        sleep(2)
        connection = self.connections[player_id]
        if (type(message) == type("String")):
            await connection.send_text(message)
        else:
            await connection.send_json(message)
