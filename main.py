from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv('.env', override=True)
app = FastAPI()

# Set your OpenAI API key here
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app.mount("/static", StaticFiles(directory="app/templates"), name="static")

@app.get("/")
async def get():
    with open("app/templates/index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    openai=OpenAI()
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": data}]
        )
        assistant_message = response.choices[0].message.content
        await websocket.send_text(assistant_message)
