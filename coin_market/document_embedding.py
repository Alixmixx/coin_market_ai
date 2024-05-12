import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import dotenv
import json
import numpy

# Load environment variables
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_DOC_DIR = '/home/amuller/Documents/mirinae/lookup/coin_market/docs'

output_dir = '/home/amuller/Documents/mirinae/lookup/coin_market/data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def load_documents(api_doc_dir):
    loaded_text = ""
    for filename in os.listdir(api_doc_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(api_doc_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                loaded_text += file.read() + "\n\n"

    return loaded_text  # Returns a single string containing all texts


def text_splitter(text_content):
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50,
                                              length_function=len, is_separator_regex=False)
    chunk_list = splitter.split_text(text_content)
    return chunk_list

# Embedding
def generate_embeddings(texts):
    embeddings_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    embeddings = embeddings_model.embed_documents(texts)
    return embeddings

def save_chunks_and_embeddings(chunk_list, embeddings, chunks_path="chunks.json", embeddings_path="embeddings.npy"):
    # Save chunks
    with open(output_dir + '/' + chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunk_list, f, ensure_ascii=False, indent=4)
    
    # Save embeddings
    numpy.save(output_dir + '/' + embeddings_path, embeddings)

    print(f"Chunks saved to {chunks_path}")
    print(f"Embeddings saved to {embeddings_path}")

def generate_embedding(api_doc_dir = API_DOC_DIR):
    document = load_documents(api_doc_dir)
    chunk_list = text_splitter(document)
    embeddings = generate_embeddings(chunk_list)

    save_chunks_and_embeddings(chunk_list, embeddings)
    return chunk_list, embeddings

generate_embedding()