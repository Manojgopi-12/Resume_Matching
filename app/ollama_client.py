import ollama
import json

def nomic_embed_text(text):
    """
    Call Ollama locally to get embeddings using nomic-embed-text model.
    """
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response['embedding']


def extract_resume_fields(resume_text):
    """
    Call Ollama locally to parse a resume into structured fields for the resumes table.
    Always requests these exact fields in JSON.
    """
    prompt = f"""
You are an expert resume parser.
Your task is to extract the following fields from the given resume text.

Return ONLY valid JSON with the following keys:
{{
  "name": "",
  "email": "",
  "phone": "",
  "linkedin": "",
  "address": "",
  "skills": "",
  "experience": "",
  "education": "",
  "summary": ""
}}

Be concise, clear, and consistent.
Do NOT include any markdown or explanation. Only output the JSON.

Resume text:
---
{resume_text}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    # Parse to JSON
    return json.loads(content)
