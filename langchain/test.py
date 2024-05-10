from langchain_openai import OpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
import os
import dotenv
import pprint
import json

def pretty(data):
    return pprint.PrettyPrinter(indent=4).pprint(data)

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(model_name="gpt-3.5-turbo-instruct")

message = [
    SystemMessage(content="You are a tutor who provides answers with a bit of sarcasm"),
    HumanMessage(content="What is the capital of France?")
]

response = openai.invoke(message)
pretty(response)