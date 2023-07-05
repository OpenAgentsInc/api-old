"""OpenAI helpers"""

import logging
import os
import time

import openai

from dotenv import load_dotenv

load_dotenv()

MAX_CONTENT_LENGTH = 8191
MAX_CONTENT_LENGTH_COMPLETE = 4097
MAX_CONTENT_LENGTH_COMPLETE_CODE = 8191
EMBED_DIMS = 1536
MODEL_EMBED = 'text-embedding-ada-002'
MODEL_COMPLETION = 'text-davinci-003'
MODEL_COMPLETION_CODE = 'code-davinci-002'


openai.api_key = os.getenv("OPENAI_API_KEY")


def complete(prompt, tokens_response=1024, model=MODEL_COMPLETION):
    """
    This function takes in a prompt (string) and an optional argument for tokens_response (default 1024).
    The prompt is passed to the OpenAI API for completions using the MODEL_COMPLETION and the specified parameters.
    If the length of the prompt exceeds the MAX_CONTENT_LENGTH_COMPLETE - tokens_response,
    the function truncates the prompt and adds the string '...truncated' to indicate this.
    The function will try up to 3 times to get a response from the API, with a 0.6 second delay between each try.
    If a response is successfully obtained, the function returns the text of the response.
    """
    if len(prompt) > MAX_CONTENT_LENGTH_COMPLETE - tokens_response:
        nonsequitor = '\n...truncated\n'
        margin = int(len(nonsequitor) / 2)
        first_half = int((MAX_CONTENT_LENGTH_COMPLETE - tokens_response) / 2)
        prompt = prompt[:first_half - margin] + \
            nonsequitor + prompt[-first_half + margin:]

    # Try 3 times to get a response
    for i in range(0, 3):
        try:
            results = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=tokens_response,
                temperature=0.2,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.6)
            break
        except Exception as error:
            logging.error(error, exc_info=True)
            print(f"Tried {i} times. Couldn't get response, trying again...")
            # log the error here
            time.sleep(0.6)
            continue

    # print(results)
    # print("---- done completion result ---")

    total_tokens = results['usage']['total_tokens']
    prompt_tokens = results['usage']['prompt_tokens']
    completion_tokens = results['usage']['completion_tokens']

    print(
        f"Completion - Tokens used: {total_tokens} (prompt: {prompt_tokens}, completion: {completion_tokens})")

    return results['choices'][0]['text'].strip()
