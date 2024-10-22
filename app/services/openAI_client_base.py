import os
from openai import OpenAI

class OpenAIClientBase:
    def __init__(self):
        self.OPENAI_API_KEY_ENV_VAR = 'OPENAI_API_KEY'
        self.client = self.set_openai_client()

    def get_api_key(self):
        api_key = os.environ.get(self.OPENAI_API_KEY_ENV_VAR)
        assert api_key, f"API key not found\nSet your OpenAI API key as an environment variable named '{self.OPENAI_API_KEY_ENV_VAR}'"
        return api_key

    def set_openai_client(self):
        client = OpenAI()
        client.api_key = self.get_api_key()
        return client