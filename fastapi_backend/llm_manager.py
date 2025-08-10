# from google import genai
from turtle import mode
import google.generativeai as genai
from google.genai import types

SYSTEM_PROMPT = """You are a helpful assistant who answers in simple, to-the-point and clear language. 
                    Keep your answers short and concise."""

class LLMManager:
    def __init__(self, model_name="gemini-1.5-flash", api_key=None):

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT
        )

    def infer(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text