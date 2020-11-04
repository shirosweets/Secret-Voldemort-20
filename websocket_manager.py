from starlette.concurrency import run_until_first_complete
from threading import Thread, Condition, RLock, current_thread
from time import sleep
from fastapi import WebSocket
from typing import Union

#async def run_until_first_complete(*args: typing.Tuple[typing.Callable, dict]) -> None:

class WebsocketManager:
    def __init__(self):
        # The dictionary defines how the active sockets are stored. The key is the player_id
        self.lock = RLock()
        #self.active_sockets: Dict[int, WebSocket] = {}
        self.socketPorts = {} 
        #self.threads = []

    async def __receiveMessage(self, player_id : int, ws : WebSocket):
        msg = await ws.receive_text()
        print(msg) #TODO: replace for what we do with incomming messages

    async def __sendMessage(self, player_id : int, ws : WebSocket):
        print("Private sendMessage() function of websocket Manager called")
        while True:
            self.lock.acquire()
            cond = self.socketPorts[player_id][0]
            while (len(self.socketPorts[player_id][1]) == 0):
                cond.wait()
            print(f"Thread {current_thread().getName()} was signaled and woke Up!")
            messages = self.socketPorts[player_id][1]
            self.socketPorts[player_id][1] = []
            self.lock.release()
            for msg in messages:
                if (type(msg) == type("String")):
                    await ws.send_text(msg)
                else:
                    await ws.send_json(msg)
            del messages

    async def listen(self, player_id : int, ws : WebSocket):
        print("Listen function of websocket Manager called")
        while True:
            await run_until_first_complete(
                (self.__receiveMessage, {"player_id": player_id, "websocket": ws}),
                (self.__sendMessage, {"player_id": player_id, "websocket": ws}),
                )
            
    async def giveSocket(self, player_id : int, ws : WebSocket):
        print("Socket given to the manager")
        newCondition = Condition(lock=self.lock)
        self.lock.acquire()
        self.socketPorts[player_id] = [newCondition, list()]
        self.lock.release()
        newThread = Thread(target=self.listen, args=(player_id, ws,), daemon=True)
        newThread.start()

    #TODO: add disconect

    async def send_msg(self, player_id : int, message: Union[str, dict]):
        print(f"Send message public function called with argument {str(message)}")
        self.lock.acquire()
        #print(self.socketPorts)
        self.socketPorts[player_id][1].append(message)
        cond = self.socketPorts[player_id][0]
        cond.notifyAll()
        self.lock.release()
