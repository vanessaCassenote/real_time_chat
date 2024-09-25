#!/usr/bin/env python

import asyncio
from websockets.server import serve
from fastapi import WebSocket


class ChatConnection:
    
    def __init__(self) -> None:
        self.connection_clients: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connection_clients.append(websocket)
    
    def disconnect(self, websocket:WebSocket):
        self.connection_clients.remove(websocket)
        
    async def broadcast(self, message:str):
        for c in self.connection_clients:
            await c.send_text(message)
    
    async def send_individual_message(self, message:str, websocket:WebSocket):
        await websocket.send_text(message)
