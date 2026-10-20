import io
import pdfplumber
from docx import Document
from fastapi import UploadFile

async def extract_text(file: UploadFile) -> str:
    contents=await file.read()
    filename=(file.filename or "").lower()
    if filename.endswith(".pdf"):
        return _extract_pdf(contents)
    elif filename.endswith(".docx"):
        return _extract_docx(contents)
    elif filename.endswith(".txt"):
        return contents.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {filename}")

def _extract_pdf(contents: bytes) -> str:
    text_parts=[]
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def _extract_docx(contents: bytes) -> str:
    doc=Document(io.BytesIO(contents))
    return "\n".join(p.text for p in doc.paragraphs if p.text)

