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
        
        # user_message_embedding=Contexts.openaiEmbedding(openai=openai,text=message)
        # most_relevant_texts=Contexts.find_relevant_texts(user_message_embeddings=user_message_embedding)
        posts_file = 'Dataset/reddit_posts.csv'
        comments_file = 'Dataset/reddit_post_comments.csv'
        results = Contexts.find_related_posts_and_comments(posts_file, comments_file, message)
        posts_title=[]
        posts_text=[]
        post_comments=[]
        for post_id, content in results.items():
            # print(f"Post ID: {post_id}")
            # print(f"Title: {content['post title']}")
            posts_title.append(content['post title'])
            # print(f"Text: {content['texts']}")
            posts_text.append(content['texts'])
            # print(f"Comments: {content['comments']}")
            post_comments.append(content['comments'])
            print(posts_title)
            print(posts_text)
            print(post_comments)

        chatbot.add_message(chatbot.client,chatbot.thread_id,message,posts_title,posts_text,post_comments)
        assistant_message=chatbot.createRunAndGenerate(chatbot.client,chatbot.thread_id)
        
        # response = openai.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": message}]
        # )
        # assistant_message = response.choices[0].message.content
        print(assistant_message)
        await websocket.send_text(assistant_message)
