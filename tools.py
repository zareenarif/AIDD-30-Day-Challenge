
import json
from pathlib import Path
from pypdf import PdfReader
from agents import function_tool

PDF_CACHE_FILE = Path("pdf_text_cache.txt")

@function_tool
def extract_pdf_text(file_path: str) -> str:
    """Extract text from uploaded PDF file"""
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    # store extracted text
    store_pdf_text(full_text)
    return full_text

@function_tool
def load_pdf_text() -> str:
    """Load previously extracted PDF text"""
    if PDF_CACHE_FILE.exists():
        return PDF_CACHE_FILE.read_text(encoding="utf-8")
    return ""

@function_tool
def store_pdf_text(text: str) -> None:
    """Store PDF text for later use"""
    PDF_CACHE_FILE.write_text(text, encoding="utf-8")
