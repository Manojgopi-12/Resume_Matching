import pdfplumber
import docx
import easyocr
import re
from PIL import Image
import tempfile

reader = easyocr.Reader(['en'])

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file) -> str:
    with pdfplumber.open(file) as pdf:
        all_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return clean_text(all_text)

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return clean_text("\n".join([p.text for p in doc.paragraphs]))

def extract_text_from_image(image_file) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_file.read())
        tmp.flush()
        text = "\n".join(reader.readtext(tmp.name, detail=0))
    return clean_text(text)

def extract_text(file, filename):
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file)
        if len(text.strip()) < 30:
            # fallback for scanned PDFs
            # convert pages to images externally and OCR them here
            # for simplicity: just say "scan detected" for now
            return "SCAN DETECTED - need advanced PDF to image conversion"
        return text
    elif filename.lower().endswith(".docx"):
        return extract_text_from_docx(file)
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return extract_text_from_image(file)
    else:
        return ""
