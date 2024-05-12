import os
import json
import numpy as np
from langchain_openai import OpenAI, OpenAIEmbeddings
import dotenv

# Function to load chunks from a JSON file
def load_chunks(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    return chunks

# Function to load embeddings from a numpy file
def load_embeddings(filename):
    return np.load(filename, allow_pickle=True)

# Load your model here, for example:
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAIN_PATH = os.getenv("MAIN_PATH")
embeddings_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def find_most_relevant_docs(query, document_embeddings, documents, top_n=3):
    query_embedding = embeddings_model.embed_documents([query])[0]
    similarities = np.dot(document_embeddings, query_embedding)
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    return [documents[i] for i in top_indices]

def generate_response(query, context_documents):
    context = "\n\n".join(context_documents) + "\n\n" + query
    # Assume a GPT model is set up here to generate the response:
    response = embeddings_model.model.generate(context, max_tokens=150)
    return response

# Example usage:
def retrieve_similar_chunks(query = "How do I fetch the airdrops?"):
    # Load data
    chunks_path = MAIN_PATH + '/data/' + 'chunks.json'
    embeddings_path = MAIN_PATH + '/data/' + 'embeddings.npy'
    loaded_texts = load_chunks(chunks_path)
    document_embeddings = load_embeddings(embeddings_path)

    context_docs = find_most_relevant_docs(query, document_embeddings, loaded_texts)
    print(context_docs)
    return context_docs

