from google import genai
from os import getenv as env

gemini = genai.Client(api_key=env("AI_API_KEY"))