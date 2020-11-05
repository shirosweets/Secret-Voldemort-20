from fastapi import WebSocket
from time import sleep
from typing import Dict, Union

class WebsocketManager:
    def __init__(self):
        #Dict[str, float] // key is player_id
        self.connections: Dict[int, WebSocket] = dict()
    
    async def __dispatchMessage(self):
        pass

    async def connect(self, player_id : int, ws: WebSocket):
        await ws.accept()
        self.connections[player_id] = ws
        await ws.send_text("Socket Connection Accepted")

    def disconnect(self, player_id : int, ws: WebSocket):
        self.connections.pop(player_id, None)

    async def sendMessage(self, player_id : int, message: Union[str, dict]):
        connection = self.connections[player_id]
        if (type(message) == type("String")):
            await connection.send_text(message)
        else:
            await connection.send_json(message)
