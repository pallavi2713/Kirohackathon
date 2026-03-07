"""Ingestion service: S3 -> chunk -> OpenSearch."""
import os
import sys

# Add common module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.settings import INDEX_NAME, EMBEDDING_DIMENSION
from common.aws_clients import get_opensearch_client, get_bedrock_client, get_s3_client
from app.text_chunking import chunk_text
from app.embedding_generator import generate_embedding
from app.text_processing import extract_text_from_file


class DocumentIngestionService:
    """Service for ingesting documents from S3 to OpenSearch."""
    
    def __init__(self):
        """Initialize the ingestion service with AWS clients."""
        self.opensearch_client = get_opensearch_client()
        self.bedrock_client = get_bedrock_client()
        self.s3_client = get_s3_client()
    
    def create_index_if_not_exists(self):
        """Create OpenSearch index if it doesn't exist."""
        if not self.opensearch_client.indices.exists(index=INDEX_NAME):
            index_body = {
                "settings": {"index.knn": True},
                "mappings": {
                    "properties": {
                        "content": {"type": "text"},
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": EMBEDDING_DIMENSION
                        }
                    }
                }
            }
            
            self.opensearch_client.indices.create(index=INDEX_NAME, body=index_body)
    
    def ingest_document(self, bucket: str, key: str) -> dict:
        """
        Ingest a document from S3 into OpenSearch.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            
        Returns:
            Dictionary with ingestion status and metadata
        """
        # Ensure index exists
        self.create_index_if_not_exists()
        
        # Get file from S3
        obj = self.s3_client.get_object(Bucket=bucket, Key=key)
        raw_data = obj["Body"].read()
        
        # Extract text based on file type
        file_extension = os.path.splitext(key)[1]
        text = extract_text_from_file(raw_data, file_extension)
        
        # Chunk the text
        chunks = chunk_text(text)
        
        # Generate embeddings and index each chunk
        for i, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk, self.bedrock_client)
            doc = {
                "content": chunk,
                "embedding": embedding,
                "source_file": key
            }
            
            self.opensearch_client.index(index=INDEX_NAME, body=doc)
        
        return {
            "status": "success",
            "chunks": len(chunks),
            "source": key
        }
