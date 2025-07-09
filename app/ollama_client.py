import ollama
import json

def llama3_embed(text):
    """
    Call Ollama locally to get embeddings using LLaMA3.
    """
    response = ollama.embeddings(
        model="llama3",
        prompt=text
    )
    return response['embedding']


def llama3_parse_fields(resume_text):
    """
    Call Ollama locally to parse a resume into structured fields.
    Always requests these exact fields in JSON.
    """
    prompt = f"""
You are an expert resume parser.
Your task is to extract the following fields from the given resume text.

Return ONLY valid JSON with the following keys:

{{
  "name": "",
  "phone_number": "",
  "linkedin_url": "",
  "email": "",
  "location": "",
  "skills": [],
  "experience": "",
  "profile_summary": ""
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
