"""Text chunking utilities for splitting documents into smaller pieces."""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.settings import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str) -> list[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        text: The text to split into chunks
        
    Returns:
        List of text chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    return splitter.split_text(text)
