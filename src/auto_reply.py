from datasets import load_dataset
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

ds = pd.read_csv('src/data/cust_support.csv')

model = SentenceTransformer('all-MiniLM-L6-v2')
kb = faiss.read_index('src/data/faiss.index')

def retrieve(query, top_k=2):
    query_emb = model.encode([query], convert_to_numpy=True)
    distances, indices = kb.search(query_emb, top_k)
    context = []
    category = ''
    for i, j in zip(indices[0], distances[0]):
        i = int(i)
        if i == -1:
            continue
        if j >= 0.3:
            context.append(f"q: {ds.iloc[i, 0]} " + f"a: {ds.iloc[i, 3]}")
            category = ds.iloc[i,1]
    return category, context


from google import genai
from dotenv import load_dotenv
import os

def response(sender, query):
    load_dotenv()
    api_key = os.getenv('api_key')
    client = genai.Client(api_key=api_key)
    category, context = retrieve(query)
    prompt =  f"""Act as a professional email assistant. You will be given three inputs:
                The latest email or query that requires a response.
                The context, which includes the previous email responses or any relevant conversation history.
                Your goal is to generate a polite, clear, and contextually accurate reply that continues the conversation naturally. Keep the tone professional unless otherwise specified.

                Inputs:
                Team Name: Linkenite
                Work Time: 9AM - 5PM
                Sender: {sender}
                Query (incoming email): {query}
                Context (previous responses/known interactions): {context}

                Now, draft a well-structured email (body only) reply that is consistent with the context but directly addresses the new query. The response should:
                    - Greet them with proffessional tone.
                    - Acknowledge the sender’s concerns or questions by understanding their tone.
                    - Build on or reference relevant parts of the previous context.
                    - Provide clear next steps, answers, or required information and keep it short.
                    - Maintain an appropriate, professional closing.
                    - Do not add extra empty lines.
                """


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return category, response.candidates[0].content.parts[0].text




