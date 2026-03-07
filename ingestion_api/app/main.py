"""FastAPI application for document ingestion."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.document_ingestion_service import DocumentIngestionService


app = FastAPI(
    title="Document Ingestion API",
    description="API for ingesting documents from S3 to OpenSearch",
    version="1.0.0"
)

# Initialize ingestion service
ingestion_service = DocumentIngestionService()


class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    bucket: str
    key: str


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Document Ingestion API"}


@app.post("/ingest")
def ingest(req: IngestRequest):
    """
    Ingest a document from S3 into OpenSearch.
    
    Args:
        req: IngestRequest containing bucket and key
        
    Returns:
        Dictionary with ingestion status and metadata
    """
    try:
        result = ingestion_service.ingest_document(
            bucket=req.bucket,
            key=req.key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
