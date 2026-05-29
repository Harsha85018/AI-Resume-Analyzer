from io import BytesIO
import pdfplumber
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    data = uploaded_file.read()
    uploaded_file.seek(0)

    text_parts = []

    # Try pdfplumber first
    try:
        with pdfplumber.open(BytesIO(data)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
    except Exception:
        pass

    # Fallback to pypdf
    if not text_parts:
        reader = PdfReader(BytesIO(data))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

    return "\n".join(text_parts)