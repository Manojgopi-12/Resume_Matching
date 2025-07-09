import easyocr
import pdfplumber
import docx
import tempfile
import re

reader = easyocr.Reader(['en'])

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        all_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return clean_text(all_text)

def extract_from_docx(file):
    doc = docx.Document(file)
    return clean_text("\n".join([p.text for p in doc.paragraphs]))

def extract_from_image(image_file):
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        tmp.write(image_file.read())
        tmp.flush()
        text = "\n".join(reader.readtext(tmp.name, detail=0))
    return clean_text(text)

def extract_text(file, filename):
    if filename.lower().endswith('.pdf'):
        text = extract_from_pdf(file)
        if len(text.strip()) < 30:
            return "SCAN DETECTED"  # You can use OCR page conversion if you want
        return text
    elif filename.lower().endswith('.docx'):
        return extract_from_docx(file)
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return extract_from_image(file)
    else:
        return ""
