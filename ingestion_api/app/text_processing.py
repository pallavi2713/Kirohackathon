"""Text extraction utilities for different file formats."""
import io
import logging
from docx import Document
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_file(raw_data: bytes, file_extension: str) -> str:
    """
    Extract text from file based on its extension.
    
    Args:
        raw_data: Raw bytes of the file
        file_extension: File extension (e.g., '.txt', '.docx', '.pdf')
        
    Returns:
        Extracted text content
        
    Raises:
        ValueError: If file type is not supported
    """
    ext = file_extension.lower()
    
    if ext == '.pdf':
        # Handle PDF document
        pdf_reader = PdfReader(io.BytesIO(raw_data))
        text_parts = []
        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())
        text = '\n'.join(text_parts)
        logger.info(f"Extracted {len(text)} chars from PDF with {len(pdf_reader.pages)} pages")
        return text
    
    elif ext == '.docx':
        # Handle Word document
        doc = Document(io.BytesIO(raw_data))
        text = '\n'.join([para.text for para in doc.paragraphs])
        logger.info(f"Extracted {len(text)} chars from Word doc")
        return text
        
    elif ext == '.txt':
        # Handle text file with multiple encoding attempts
        try:
            return raw_data.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return raw_data.decode("utf-16")
            except UnicodeDecodeError:
                return raw_data.decode("latin-1")
    
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported types: .pdf, .docx, .txt")

