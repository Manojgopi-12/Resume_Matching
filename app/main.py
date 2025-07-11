from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from . import database, models, schemas, ocr, embedder, ollama_client
import psycopg2
import uuid

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload/", response_model=schemas.ResumeOut)
async def upload_(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Extract text using OCR/pdf/docx
    text = ocr.extract_text(file.file, file.filename)
    if not text or text.startswith("SCAN DETECTED"):
        return {"error": "Unable to extract text"}

    # 2. Embed with nomic-embed-text
    embedding_vector = embedder.get_embedding(text)

    # 3. Extract fields for resumes2
    parsed = ollama_client.extract_resume_fields(text)

    # 4. Insert into resumes2 table
    raw_conn = psycopg2.connect("dbname=postgres user=postgres password=Manojgopi@12")
    cursor = raw_conn.cursor()
    cursor.execute(
        """
        INSERT INTO resumes2 (name, email, phone, linkedin, address, skills, experience, education, summary, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [
            parsed.get("name", ""),
            parsed.get("email", ""),
            parsed.get("phone", ""),
            parsed.get("linkedin", ""),
            parsed.get("address", ""),
            parsed.get("skills", ""),
            parsed.get("experience", ""),
            parsed.get("education", ""),
            parsed.get("summary", ""),
            embedding_vector
        ]
    )
    raw_conn.commit()
    cursor.close()
    raw_conn.close()

    return {"name": parsed.get("name", ""), "raw_text": text}



@app.post("/query/")
async def query_resume(request: schemas.QueryRequest):
    # 1. Embed the user query
    query_embedding = embedder.get_embedding(request.query)

    # 2. Convert list to Postgres vector literal
    embedding_str = '[' + ','.join(str(x) for x in query_embedding) + ']'

    # 3. Cosine similarity search in Postgres
    raw_conn = psycopg2.connect("dbname=postgres user=postgres password=Manojgopi@12")
    cursor = raw_conn.cursor()
    cursor.execute(
        f"""
        SELECT id, filename, raw_text
        FROM resume2
        ORDER BY embedding <-> '{embedding_str}'::vector
        LIMIT 1
        """
    )
    result = cursor.fetchone()
    cursor.close()
    raw_conn.close()

    if not result:
        return {"error": "No similar resume found"}

    resume_id, filename, raw_text = result

    # 4. Extract fields for the new resumes table
    parsed = ollama_client.extract_resume_fields(raw_text)

    # 5. Return all required fields (matching the new table)
    response = {
        "id": resume_id,
        "filename": filename,
        "name": parsed.get("name", ""),
        "email": parsed.get("email", ""),
        "phone": parsed.get("phone", ""),
        "linkedin": parsed.get("linkedin", ""),
        "address": parsed.get("address", ""),
        "skills": parsed.get("skills", ""),
        "experience": parsed.get("experience", ""),
        "education": parsed.get("education", ""),
        "summary": parsed.get("summary", ""),
        "raw_text": raw_text
    }

    return response
