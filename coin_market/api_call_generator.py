import os
import dotenv
import json
from retrival_embedding import retrieve_similar_chunks
from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage
from coin_market_api_call import make_api_call

# Load environment variables
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COINMARKET_API_KEY = os.getenv("COINMARKET_API_KEY")

# Setup the model
model = ChatOpenAI(model="gpt-3.5-turbo-0125")
structured_llm = model #.with_structured_output(method="json_mode")

def get_llm_json_api_query(query):
    # Retrieve similar chunks from the documentation based on the query
    context_documents = retrieve_similar_chunks(query)
    context_messages = [SystemMessage(content=doc) for doc in context_documents]
    
    # Build the message sequence
    message_sequence = [
        SystemMessage(content="You are an assistant who provides the best query to send to the CoinMarket API. You have access to the API documentation and you should provide the best query to answer the user question. You must always provide a valid query and don't respond if it's not your expertise. Here are some informations about CoinMarket API:")
    ] + context_messages + [SystemMessage(content='You must anwser only with the endpoint request that need to be used nothing more, no quotes or spaces. Example of valid endpoints are: "/v1/cryptocurrency/airdrop" "/v1/cryptocurrency/categories"' )]  + [HumanMessage(content=query)]

    # Invoke the structured LLM with the constructed message sequence
    response = structured_llm.invoke(message_sequence)
    return response.json()

if __name__ == '__main__':
    user_query = input("Enter your query: ")
    api_request = get_llm_json_api_query(user_query)
    print("API Request from LLM:", api_request)
    endpoint = json.loads(api_request)["content"]
    print("Endpoint:", endpoint)
    response = make_api_call(endpoint, COINMARKET_API_KEY)
    print("Response from COINMARKET:", response)
