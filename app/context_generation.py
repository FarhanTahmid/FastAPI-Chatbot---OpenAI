import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI


class Contexts:
    
    # Load embeddings and texts
    embeddings = np.load('app/embeddings.npy')
    with open('app/texts.txt', 'r',encoding='utf-8') as f:
        texts = f.readlines()
    
    def openaiEmbedding(text,openai:OpenAI):
        response=openai.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return (response.data[0].embedding)
    
    # Function to find relevant texts
    def find_relevant_texts(user_message_embeddings,top_n=3):

        # Assume get_embedding is a function that converts the user message to an embedding
        similarities = cosine_similarity([user_message_embeddings], Contexts.embeddings)[0]
        most_relevant_indices = similarities.argsort()[-top_n:][::-1]
        relevant_texts = [Contexts.texts[i] for i in most_relevant_indices]
        
        return relevant_texts