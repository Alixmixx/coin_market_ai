import os
import json
from sentence_transformers import SentenceTransformer, util
import torch

# Load and preprocess the API documentation
def load_and_preprocess(api_docs_dir):
    docs = []
    for filename in os.listdir(api_docs_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(api_docs_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                docs.append(text)
    return docs

# Generate embeddings
def generate_embeddings(docs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(docs, convert_to_tensor=True)
    return embeddings

# RAG Integration: This is a simplified version, real implementation would need an actual retrieval and generation mechanism
class RAGModel:
    def __init__(self, docs, embeddings):
        self.docs = docs
        self.embeddings = embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve_and_generate(self, query):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        retrieved_doc = self.docs[scores.argmax().item()]

        # Here, you would integrate with a generative model to generate the response
        response = f"Retrieved Info: {retrieved_doc[:200]}..."  # Simplified response
        return response

# Load documents and generate embeddings
api_docs_dir = '/path/to/your/api_docs'
docs = load_and_preprocess(api_docs_dir)
embeddings = generate_embeddings(docs)

# Initialize RAG
rag = RAGModel(docs, embeddings)

# Example Query
response = rag.retrieve_and_generate("How do I authenticate API requests?")
print(response)
