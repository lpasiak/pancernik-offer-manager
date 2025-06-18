from openai import OpenAI
import config


class OpenAIClient:

    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
