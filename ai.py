import os
import requests
import json
import openai
import tiktoken
from pprint import pprint
from helper import Helper
import config
import re

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

openai.api_key = config.OPENAI_API_KEY
openai.api_base = config.OPENAI_API_BASE
openai.api_type = config.OPENAI_API_TYPE
openai.api_version = config.OPENAI_API_VERSION
deployment_name = config.OPENAI_DEPLOYMENT_NAME
deployment_emb_name = config.OPENAI_DEPLOYMENT_EMBEDDING_NAME

class AI:

    def get_token_count(string: str) -> int:
        encoding_name = "cl100k_base"
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def get_llm_model_for_lang_chain(self):
        return OpenAI(
          engine=deployment_name,
          temperature=0.1,
          max_tokens=1500, 
          openai_api_base=openai.api_base,
          openai_api_key=openai.api_key,)

    def get_embeddings_model(self):
        return OpenAIEmbeddings(
          deployment=deployment_emb_name,
          openai_api_base=openai.api_base,
          openai_api_type=openai.api_type,
          openai_api_key=openai.api_key,
          chunk_size=1
       )

    def prompt(self, system_prompt, user_prompt, temperature = 0.7, max_tokens = 500):

        system_promt = "You are a NASA Standards document proof reader, well versed with NASA standards, here is the context: " + system_prompt  
        error = None
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
           ]
        try:
            response = openai.ChatCompletion.create(
                engine = "rd-turbo",
                messages = messages,
                temperature = 0.7,
                max_tokens = 1500,
            )
            content = response.choices[0].message.content
            print(content)
            return { "status": "success", "response": content}
        except openai.error.Timeout as e:
            error = Helper.makeError("OpenAI API request timed out: {e}")
        except openai.error.APIError as e:
            error = Helper.makeError("OpenAI API returned an API Error: {e}")
        except openai.error.APIConnectionError as e:
            error = Helper.makeError("OpenAI API request failed to connect: {e}")
        except openai.error.InvalidRequestError as e:
            print(e)
            error = Helper.makeError("OpenAI API request was invalid: {e}")
        except openai.error.AuthenticationError as e:
            error = Helper.makeError("OpenAI API request was not authorized: {e}")
        except openai.error.PermissionError as e:
            error = Helper.makeError("OpenAI API request was not permitted: {e}")
        except openai.error.RateLimitError as e:
            error = Helper.makeError("OpenAI API request exceeded rate limit: {e}")
        return error