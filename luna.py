import os
import requests
import json
import openai
from pprint import pprint
from helper import Helper

#openai.api_key = os.getenv("AZURE_OPENAI_KEY")
#openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")

openai.api_type = "azure"
openai.api_base = "https://rd-aoai-new.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "7b7d41f1856e43dfaf6cfd5576f765dc"


class Luna:
    def prompt(self, s_prompt, user_prompt):

        system_prompt = """
            You are a NASA Technical Standards expert well versed with technical documentation.
            Remember to use NESC Technical Bulletins, lessons learned from NASA,
            Assist me in reviewing NASA Technical Standards for clarity and consistency, identifying and rectifying any ambiguities or errors with the user prompt
            ALWAYS respond back ONLY when the text needs to be updated else give the original text
        """
        system_prompt += s_prompt
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Evaluate line: " + user_prompt}
           ]
        #try: 
        response = openai.ChatCompletion.create(
            engine="rd-turbo",
            messages = messages,
            temperature=0.7,
            max_tokens=1500,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)
        print(response)
        content = response.choices[0].message.content
        return content
        #except:
        #    print("something went wrong with openai")
        
        #return user_prompt
        #return { "status": "success", "response": content}