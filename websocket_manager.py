import threading
from threading import Thread, Event, Lock
import time
from typing import Optional, Dict
from fastapi import WebSocket

class WebsocketManager:
    def __init__(self):
        # The dictionary defines how the active sockets are stored. The key is the player_id
        self.lock = Lock()
        #self.active_sockets: Dict[int, WebSocket] = {}
        self.socketPorts = {} 
        #self.threads = []

    def run(self):
        pass

    async def giveSocket(self, player_id : int, ws : WebSocket):
        newEvent = Event()
        self.lock.acquire()
        self.socketPorts[player_id] = (newEvent, True, None)
        self.lock.release()
        newThread = Thread(target=self.run)
        newThread.start()


    async def connect(self, player_id : int, ws: WebSocket):
        """
        Returns True if the connection was successful
        """
        #TODO: Add condition of refusal if socket is already actived // or at least close the previous ws
        #TODO: See if it properly raises an exception if it fails to accept it
        try:
            await ws.accept()
            #self.active_sockets[player_id] = ws
            return True
        except Exception: #TODO: Change for a better exception
            return False

    # add disconect

    async def send_msg(self, player_id : int, message: str):
        pass
        # socket = self.active_sockets[player_id]
        # await socket.send_text(message)

    async def send_dict(self, player_id : int, message: dict):
        pass
        # socket = self.active_sockets[player_id]
        # # dict is close to JSON // check if it works with dict directly or we need to turn it into json str
        # await socket.send_json(message)
