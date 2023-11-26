import openai
import os
import random

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Helper function for making OpenAPI call.
# From https://learn.deeplearning.ai/chatgpt-prompt-eng


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


sys_message = {"role": "system", "content": "You are extremely snarky."}


async def get_setting():
    settings = [
        "Medieval Times",
        "Gothic",
        "Ancient",
        "Modern",
        "One Piece",
        "Harry Potter",
        "Lord of the Rings",
        "Star Wars",
        "Pokemon",
        "Dungeons & Dragons"
    ]

    return random.choice(settings)


async def call_openai(prompt):
    messages = [sys_message, {"role": "user", "content": prompt}]
    return get_completion_from_messages(messages, temperature=1)


async def get_prompt(name1, name2, compat_value):
    return f"""
    I want to play a game.  
    I will give you two names and a number.  The names are to represent people, 
    and the number will be a value from 0 to 100.  

    Using this information, I want you to write a short, humorous story about the two people.

    The number will be used to determine how compatible these two people are in their relationship.
    Use the following criteria:
    - 0: Want to kill each other.
    - 1-9: Gets into physical fights whenver they see each other.
    - 10-19: Constantly arguing at each other.
    - 20-29: Hates being around each other.
    - 30-39: Gets annoyed when they see each other.
    - 40-49: They are fine with seeing each other, but not interested in being friends.
    - 50-59: Will talk to each other, but they are not quite friends.
    - 60-69: Will be friends with each other, with some interest in dating.
    - 70-79: Romantically interested in each other, but not quite in love.
    - 80-89: Will fall in love with each other.
    - 90-99: Madly in love with each other.
    - 100: So in love that they literally cannot stop thinking about each other.

    Do not try to write a good ending if their compat value is below 50.

    Do not start your story with "once upon a time."

    The setting of the story will be {await get_setting()}

    The values given to you to determine the two people's names and the compatibility value will be as follows:
    ```
    Person 1: {name1}
    Person 2: {name2}
    Compatibility Value: {compat_value}
    ```

    Remember to respond in less than 50 words.
    """
