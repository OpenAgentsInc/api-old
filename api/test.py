import os
from dotenv import load_dotenv
import openai
from .llms.openai_helpers import chat_complete

# Load environment variables from .env file
load_dotenv()


def test():

    # Set OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define a conversation
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]

    # Generate a response
    response = chat_complete(conversation)

    print(response)
