from openai import OpenAI
import os
from dotenv import load_dotenv

class ChatBot:
    
    # Set your OpenAI API key here
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    client=OpenAI()
    
    # create thread for the conversation
    thread=client.beta.threads.create()
    print(f"New thread was created. {thread}")
    thread_id=thread.id
    
    assistant_id=os.getenv('ASSISTANT_ID')

    def add_message(self,client,thread_id,user_message,post_title,post_text,post_comments):
        # context = "\n".join(context_list)
        message=client.beta.threads.messages.create(
            thread_id=thread_id,role="user",content=f"{user_message}. Given Contexts are: From previous reddit posts we see that people posted about the topic like this:\n Post titles:{post_title}, Post texts: {post_text}, Comments on the posts:{post_comments}"
        )

        print(f"Passed message to API is: {user_message}. Given Contexts are: From previous reddit posts we see that people posted about the topic like this:\n Post titles:{post_title}, Post texts: {post_text}, Comments on the posts:{post_comments}")
    
    def createRunAndGenerate(self,client,thread_id):
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=ChatBot.assistant_id,
        )
        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            print(messages)
            return messages.data[0].content[0].text.value
        else:
            print(run.status)