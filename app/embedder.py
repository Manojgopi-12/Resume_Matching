from .ollama_client import nomic_embed_text

def get_embedding(text: str) -> list:
    return nomic_embed_text(text)
