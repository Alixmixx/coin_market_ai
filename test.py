from openai import OpenAI
import dotenv
import os

# loading the environment variables
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# creating the model to be used
client = OpenAI(api_key=OPENAI_API_KEY)

# defining the model name and messages to display to check if the key works
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hi, my name is Alex."}
  ]
)

# printing the first message
print(completion.choices[0].message)