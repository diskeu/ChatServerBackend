import asyncio
import datetime
import csv
import websockets
import hashlib
import random
from concurrent.futures import Future
from typing import Callable


class ChatCommunication():
    def __init__(self):
        self.rooms = self.Chats()

    class Chats():
        def __init__(self):
            self.chats = []

    class Chat():
        def __init__(self):
            self.peers = {}
            self.id = None
            self.len_Members = 2
        async def create_Id(self) -> None:
            num: int = random.randint(10000, 99999)
            num_Name: str = str(num)+str(self.peers)
            id: str = hashlib.sha256(num_Name.encode()).hexdigest()
            self.id = id[:8]

    class Peer():
        def __init__(self):
            self.ws = None
            self.id = None
            self.name = None
        def __str__(self):
            return self.id

    async def disconnect(self, client_Peer: Peer, room) -> None:
        ws = client_Peer.ws
        dscnt_Msg: str = f"{client_Peer.name} left the room"

        def server_dscnt(peer) -> str:
            server_dscnt_Msg: str = f"{room.peers[peer.ws][1]} - {room.peers[peer.ws][0][:4]} disconnected"
            return server_dscnt_Msg
        
        room.peers.pop(client_Peer.ws)
        close_all = True if len(room.peers) < 2 else False
        for peer in room.peers:
            await peer.send(dscnt_Msg)
            if close_all:
                await peer.close(code=1000, reason=dscnt_Msg)
                server_dscnt(peer)
                room.peers.pop(peer)
        return

    async def recv_Loop(self, room, client_Peer, msg_Alarm):
        ws = client_Peer.ws
        try:
            while True:
                msg = await ws.recv()
                await msg_Alarm.put(msg)
        except websockets.ConnectionClosed:
            await self.disconnect(client_Peer, room=room)
            return
        
    async def send_Loop(self, room, client_Peer, msg_Alarm):
        ws = client_Peer.ws
        room_Id = room.id
        client_Id = client_Peer.id
        try:
            while True:
                msg = await msg_Alarm.get()
                now = datetime.datetime.now()
                time = now.strftime("%Y.%m.%d - %X")
                msg = f"{client_Peer.name}: {msg}"
                for peer in room.peers:
                    if peer != ws:
                        await peer.send(msg)
        except websockets.ConnectionClosed:
            await self.disconnect(client_Peer, room=room)

    def create_Peer(self, roomName, ws):
        cur_Peer = self.Peer()
        cur_Peer.name = roomName
        cur_Peer.ws = ws
        num = random.randint(10000, 99999)
        num_Name = str(num)+roomName
        id = hashlib.sha256(num_Name.encode()).hexdigest()
        cur_Peer.id = id[:16]
        return cur_Peer

    async def breaking(self, task1: Callable, args1, task2: Callable, args2):
        t1 = asyncio.create_task(task1(*args1))
        t2 = asyncio.create_task(task2(*args2))
        done, pending = await asyncio.wait(
            {t1, t2},
            return_when=asyncio.FIRST_EXCEPTION
        )
        for t in pending:
            t.cancel()

    async def join_Room(self, room, client_Peer):
        ws = client_Peer.ws
        members = []
        for peer in room.peers:
            if peer != ws:
                members.append(room.peers[peer][1])
                await peer.send(f"{client_Peer.name} joined the room")
        if members:
            await ws.send(f"you are in a room with {", ".join(members)}")


    async def handle_Client(self, ws):
        await ws.send("Enter /r for random chat, /rc for random chat room")
        chat_Type = await ws.recv()
        await ws.send("Enter Name")
        roomName = await ws.recv()
        client_Peer = self.create_Peer(roomName=roomName, ws=ws)
        async def find_Room(length):
            for room in self.rooms.chats:
                if (len(room.peers) < room.len_Members) and (room.len_Members == length):
                    room.peers[client_Peer.ws] = [client_Peer.id, client_Peer.name]
                    await self.join_Room(room=room, client_Peer=client_Peer)
                    msg_Alarm = asyncio.Queue()
                    return room, msg_Alarm
            room = self.Chat()
            self.rooms.chats.append(room)
            room.len_Members = length
            room.peers[client_Peer.ws] = [client_Peer.id, client_Peer.name]
            await room.create_Id()
            msg_Alarm = asyncio.Queue()
            await self.join_Room(room=room, client_Peer=client_Peer)
            return room, msg_Alarm

        if chat_Type == "/r":
            room, msg_Alarm = await find_Room(2)
        elif chat_Type == "/rc":
            room, msg_Alarm = await find_Room(5)
        await self.breaking(
                task1=self.recv_Loop, args1=(room, client_Peer, msg_Alarm),
                task2=self.send_Loop, args2=(room, client_Peer, msg_Alarm)
            )
        return

    async def main(self):
        async with websockets.serve(self.handle_Client, "localhost", 8756):
            await asyncio.Future()
