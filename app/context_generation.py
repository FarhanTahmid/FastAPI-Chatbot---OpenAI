import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import pandas as pd

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

    def find_related_posts_and_comments(posts_file, comments_file, search_string):
        # Load the datasets
        posts_df = pd.read_csv(posts_file)
        comments_df = pd.read_csv(comments_file)

        # Fill NaN values with empty strings
        posts_df['post_title'] = posts_df['post_title'].fillna('')
        posts_df['selftext'] = posts_df['selftext'].fillna('')
        comments_df['comment'] = comments_df['comment'].fillna('')
        
        # Search for the string in posts (title and text)
        matching_posts = posts_df[posts_df.apply(lambda row: search_string.lower() in row['post_title'].lower() or search_string.lower() in row['selftext'].lower(), axis=1)]
        
        # Search for the string in comments
        matching_comments = comments_df[comments_df['comment'].str.contains(search_string, case=False, na=False)]
        
        # Get the unique post IDs from both matching posts and comments
        matching_post_ids = set(matching_posts['post_id']).union(set(matching_comments['post_id']))
        
        # Retrieve the related posts and comments
        related_posts = posts_df[posts_df['post_id'].isin(matching_post_ids)]
        related_comments = comments_df[comments_df['post_id'].isin(matching_post_ids)]
        
        # Create a dictionary to store the results
        results = {}
        for post_id in matching_post_ids:
            post_info = related_posts[related_posts['post_id'] == post_id].iloc[0]
            comments = related_comments[related_comments['post_id'] == post_id]['comment'].tolist()
            results[post_id] = {
                'post title': post_info['post_title'],
                'texts': post_info['selftext'],
                'comments': comments
            }
        return results
    