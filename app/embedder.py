from .ollama_client import llama3_embed

def get_embedding(text: str) -> list:
    return llama3_embed(text)
