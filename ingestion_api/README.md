# FastAPI Ingestion API

A modular FastAPI service for ingesting documents from S3 into OpenSearch with AWS Bedrock embeddings.

## Project Structure

```
fastapi_ingestion_api/
├── app/
│   ├── __init__.py                      # Package initialization
│   ├── main.py                          # FastAPI application and endpoints
│   ├── settings.py                      # Configuration (loads from project root .env)
│   ├── document_ingestion_service.py    # Core ingestion service logic
│   ├── text_processing.py               # Text extraction from files
│   ├── text_chunking.py                 # Text chunking utilities
│   └── embedding_generator.py           # Embedding generation with Bedrock
├── requirements.txt                     # Python dependencies
└── README.md                            # This file

Note: .env file is located in the project root (AI-For-Bharat-Hackathon/.env)
Note: AWS clients are imported from the shared common/ module
```

## Setup

1. Install dependencies:
```bash
cd fastapi_ingestion_api
pip install -r requirements.txt
```

2. Configure environment variables:
   - The project uses a shared `.env` file located in the project root: `AI-For-Bharat-Hackathon/.env`
   - Copy `.env.example` to `.env` in the project root if it doesn't exist:
   ```bash
   cd ..
   cp .env.example .env
   ```
   - Update `.env` with your AWS and OpenSearch credentials

3. Run the API from the fastapi_ingestion_api directory:
```bash
cd fastapi_ingestion_api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```
GET /
```

### Ingest Document
```
POST /ingest
Content-Type: application/json

{
  "bucket": "your-s3-bucket",
  "key": "path/to/document.txt"
}
```

## Supported File Types

- `.txt` - Text files (UTF-8, UTF-16, Latin-1)
- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents

## Environment Variables

Environment variables are stored in the project root `.env` file (`AI-For-Bharat-Hackathon/.env`).

See `AI-For-Bharat-Hackathon/.env.example` for all available configuration options.
