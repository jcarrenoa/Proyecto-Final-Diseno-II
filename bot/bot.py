from dotenv import load_dotenv
import os
from openai import OpenAI

class Bot:
    def __init__(self):
        load_dotenv()
        self.__client = OpenAI()
        self.__client.api_key = os.getenv("OPENAI_API_KEY")
        self.__messages_context = [
            {"role": "system", "content": "Eres un bot que solo da informacion etimologica de los nombres que se te proporcionan."},
        ]
    
    def get_response(self, message):
        message_f = self.__messages_context + [{"role": "user", "content": message}]
        completion = self.__client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_f,
            temperature=0,
            max_tokens=1000,
            top_p = 1,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        return completion.choices[0].message.content