
# uvicorn app:app -- reload

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from chat_connection import ChatConnection

app = FastAPI()

html = open("chat.html", "r", encoding="utf-8").read()

print(html)
chat = ChatConnection()

@app.get("/")
async def main():
    return HTMLResponse(html)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket:WebSocket, user_id:str):
    await chat.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await chat.broadcast(f"Client: {user_id} says: {data}")
            await chat.send_individual_message(f"You wrote {data}", websocket)
    except WebSocketDisconnect:
        chat.disconnect(websocket)
        await chat.broadcast(f"{user_id} has left the chat!")