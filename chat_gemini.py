''' Gemini bot in a group chat'''
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import websockets
import asyncio
#import keyboard

load_dotenv(".env")
key = os.environ["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


def get_bot_answer(human_message):

    messages = [
        (
            "system",
            "You are a friend in group chat",
        ),
        ("human", f"{human_message}"),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content


async def chatting(client_id):
    
    async with websockets.connect("ws://localhost:8000/ws/"+client_id) as ws:
        
        while True:
            recv_message = await ws.recv()
            mse = recv_message.split("\n")[-1]
            if client_id in mse:
                question = mse.split("Gemini_bot:")[1]
                send_message = f"\nEu recebi: {get_bot_answer(question)}"
                await ws.send(send_message)
                print(mse)

if __name__ == "__main__":
    client_id = "Gemini_bot"
    asyncio.run(chatting(client_id))