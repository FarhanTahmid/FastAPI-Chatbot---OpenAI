from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.context_generation import Contexts
from app.chatbot import ChatBot

load_dotenv('.env', override=True)
app = FastAPI()
openai=OpenAI()
chatbot=ChatBot()

app.mount("/static", StaticFiles(directory="app/templates"), name="static")

@app.get("/")
async def get():
    with open("app/templates/index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        
        user_message_embedding=Contexts.openaiEmbedding(openai=openai,text=message)
        most_relevant_texts=Contexts.find_relevant_texts(user_message_embeddings=user_message_embedding)
        
        chatbot.add_message(chatbot.client,chatbot.thread_id,message,most_relevant_texts)
        assistant_message=chatbot.createRunAndGenerate(chatbot.client,chatbot.thread_id)
        
        # response = openai.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": message}]
        # )
        # assistant_message = response.choices[0].message.content
        print(assistant_message)
        await websocket.send_text(assistant_message)
