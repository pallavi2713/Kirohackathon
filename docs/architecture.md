# AI Government Scheme Navigator - System Architecture

## Executive Summary

The AI Government Scheme Navigator is a serverless, AI-powered conversational system designed to help rural citizens discover and understand government schemes they are eligible for. Built on AWS, the system uses RAG (Retrieval Augmented Generation) to provide accurate, context-aware answers in multiple languages.

## Problem Statement

- **Low Awareness**: Rural citizens are unaware of available government schemes
- **Complex Eligibility**: Difficult to understand eligibility criteria
- **Language Barriers**: Schemes documented in complex language
- **Information Overload**: Hundreds of schemes across different departments

## Solution Overview

An intelligent chatbot that:
1. Ingests government scheme documents automatically
2. Answers questions in simple language (English/Hindi)
3. Provides personalized scheme recommendations
4. Maintains conversation context for follow-up questions

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                                │
│                  (Web Browser - S3 Static Website)                    │
│                         index.html                                    │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │ HTTPS
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        AWS API GATEWAY                                │
│  • REST API Endpoint                                                  │
│  • CORS Configuration                                                 │
│  • Request/Response Transformation                                    │
│  • Throttling & Rate Limiting                                         │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      QUERY PROCESSING LAYER                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Lambda: Scheme Query Handler (RAG Pipeline)                  │  │
│  │  • Query Rewriting  • Embedding Generation                    │  │
│  │  • Vector Search    • Answer Generation                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
        ┌───────────────────┐     ┌──────────────────┐
        │  AWS Bedrock      │     │  OpenSearch      │
        │  • Titan Embed    │     │  • Vector Store  │
        │  • Nova LLM       │     │  • KNN Search    │
        └───────────────────┘     └──────────────────┘
                                           ▲
                                           │
┌──────────────────────────────────────────┴───────────────────────────┐
│                    DOCUMENT INGESTION LAYER                           │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐   │
│  │   S3 Bucket  │───▶│  Lambda Trigger │───▶│  FastAPI Service │   │
│  │  (Documents) │    │  (S3 Event)     │    │  (EC2/Container) │   │
│  └──────────────┘    └─────────────────┘    └──────────────────┘   │
│                                                       │               │
│                                                       ▼               │
│                                          ┌────────────────────────┐  │
│                                          │  • Extract Text        │  │
│                                          │  • Chunk Documents     │  │
│                                          │  • Generate Embeddings │  │
│                                          │  • Index in OpenSearch │  │
│                                          └────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 0. Frontend (S3 Static Website)

**Purpose**: User interface for interacting with the chatbot

**Technology**: HTML, CSS, JavaScript hosted on AWS S3

**Features**:
- Simple chat interface
- Language selection (English/Hindi)
- Conversation history display
- Source document attribution
- Mobile-responsive design

**Hosting**:
- **S3 Bucket**: Static website hosting enabled
- **CloudFront** (Optional): CDN for faster global access
- **Custom Domain** (Optional): Route 53 DNS

**API Integration**:
```javascript
// Call API Gateway endpoint
fetch('https://api-gateway-url/prod/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: userQuestion,
    language: selectedLanguage,
    history: conversationHistory
  })
});
```

### 0.5. API Gateway

**Purpose**: RESTful API endpoint for frontend-backend communication

**Technology**: AWS API Gateway (REST API)

**Configuration**:
- **Endpoint**: `POST /query`
- **Integration**: Lambda Proxy Integration with Scheme Query Handler
- **CORS**: Enabled for S3 website origin
- **Throttling**: 1000 requests/second
- **Authentication**: API Key (optional) or IAM

**Request Flow**:
```
Frontend → API Gateway → Lambda → Response → API Gateway → Frontend
```

**Benefits**:
- Managed service (no server maintenance)
- Built-in throttling and rate limiting
- Request/response transformation
- API versioning support
- CloudWatch logging and monitoring

---

### 1. Document Ingestion Pipeline

**Purpose**: Automatically process and index government scheme documents

**Flow**:
```
PDF/DOCX Upload → S3 Bucket → Lambda Trigger → FastAPI Service → OpenSearch
```

**Components**:

#### A. S3 Event Ingestion Trigger (Lambda)
- **Trigger**: S3 ObjectCreated event
- **Function**: Forward S3 event to FastAPI ingestion service
- **Technology**: AWS Lambda, Python 3.11
- **Key Features**:
  - Automatic triggering on document upload
  - Error handling and retry logic
  - CloudWatch logging

#### B. FastAPI Ingestion Service (EC2)
- **Endpoint**: `POST /ingest`
- **Technology**: FastAPI, Python 3.11
- **Modules**:
  - `text_processing.py`: Extract text from PDF/DOCX/TXT
  - `text_chunking.py`: Split documents into 500-char chunks
  - `embedding_generator.py`: Generate embeddings using Bedrock Titan
  - `document_ingestion_service.py`: Orchestrate the pipeline

**Processing Steps**:
1. Receive S3 bucket and key from Lambda
2. Download document from S3
3. Extract text (supports PDF, DOCX, TXT)
4. Split into overlapping chunks (500 chars, 50 overlap)
5. Generate embeddings for each chunk (Titan Embed v1)
6. Index in OpenSearch with metadata

**Supported Formats**:
- PDF (PyPDF2)
- DOCX (python-docx)
- TXT (UTF-8, UTF-16, Latin-1)

---

### 2. Query Processing Pipeline (RAG)

**Purpose**: Answer user questions using Retrieval Augmented Generation

**Flow**:
```
User Question → Query Rewriting → Embedding → Vector Search → 
Context Retrieval → LLM Generation → Answer + Sources
```

**Components**:

#### Scheme Query Handler (Lambda)

**Technology**: AWS Lambda, Python 3.11

**Modules**:
- `prompts.py`: LLM prompt templates
- `qna.py`: RAG pipeline logic
- `embedding_service.py`: Query embedding generation
- `opensearch_operations.py`: Vector search operations
- `config.py`: Configuration management

**RAG Pipeline Steps**:

1. **Query Rewriting**
   - Converts follow-up questions to standalone queries
   - Uses conversation history for context
   - Model: Amazon Nova Lite v1

2. **Embedding Generation**
   - Generates 1536-dim vector for query
   - Model: Amazon Titan Embed Text v1

3. **Vector Search**
   - KNN search in OpenSearch
   - Retrieves top 3 relevant chunks
   - Cosine similarity scoring

4. **Answer Generation**
   - Combines retrieved context + conversation history
   - Generates answer in requested language
   - Model: Amazon Nova Lite v1
   - Temperature: 0.1 (factual accuracy)

5. **Response**
   - Returns answer + source documents
   - Maintains conversation context

**Key Features**:
- Multi-language support (English/Hindi)
- Conversation history tracking
- Context-aware follow-up questions
- Source attribution

---

## Data Flow Diagrams

### Ingestion Flow

```
┌─────────────┐
│   Admin     │
│  Uploads    │
│  Document   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│                    S3 Bucket                             │
│  • government-schemes/pm-kisan.pdf                      │
│  • government-schemes/ayushman-bharat.docx              │
└──────────────────────┬──────────────────────────────────┘
                       │ (S3 Event Notification)
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Lambda: S3 Event Ingestion Trigger                     │
│  • Extract bucket & key                                 │
│  • POST to FastAPI: {bucket, key}                       │
└──────────────────────┬──────────────────────────────────┘
                       │ (HTTP POST)
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FastAPI Ingestion Service (EC2)                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. Download from S3                             │   │
│  │ 2. Extract text (PDF/DOCX/TXT)                  │   │
│  │ 3. Chunk text (500 chars, 50 overlap)           │   │
│  │ 4. Generate embeddings (Bedrock Titan)          │   │
│  │ 5. Index in OpenSearch                          │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              OpenSearch Serverless                       │
│  Index: scheme-index                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Document 1:                                     │   │
│  │  • content: "PM-KISAN provides Rs 6000..."     │   │
│  │  • embedding: [0.123, -0.456, ...]             │   │
│  │  • source_file: "pm-kisan.pdf"                 │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Query Flow

```
┌─────────────┐
│    User     │
│   Browser   │
│  (S3 Site)  │
└──────┬──────┘
       │ POST /query
       ▼
┌─────────────────────────────────────────────────────────┐
│  AWS API Gateway                                         │
│  • Endpoint: https://xxx.execute-api.us-east-1.../query │
│  • Method: POST                                          │
│  • CORS: Enabled                                         │
└──────────────────────┬──────────────────────────────────┘
                       │ Lambda Proxy Integration
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Lambda: Scheme Query Handler                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 1: Parse API Gateway Event                 │   │
│  │  • Extract body from event                      │   │
│  │  • Parse JSON: {question, language, history}    │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 2: Query Rewriting (if follow-up)         │   │
│  │  • Input: "What is PM-KISAN?"                   │   │
│  │  • Output: "What is PM-KISAN?"                  │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 3: Generate Query Embedding                │   │
│  │  • Model: Titan Embed Text v1                   │   │
│  │  • Output: [0.234, -0.567, ...] (1536-dim)     │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  OpenSearch: Vector Search (KNN)                        │
│  • Query: embedding vector                              │
│  • k: 3 (top 3 results)                                 │
│  • Returns: Most similar chunks                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Retrieved Context:                                      │
│  1. "PM-KISAN provides Rs 6000 per year..."            │
│  2. "Eligibility: Small and marginal farmers..."       │
│  3. "Application process: Visit nearest CSC..."        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Lambda: Answer Generation                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 4: Generate Answer with LLM                │   │
│  │  • Model: Amazon Nova Lite v1                   │   │
│  │  • Temperature: 0.1 (factual)                   │   │
│  │  • Input: Question + Context + History          │   │
│  │  • Output: Structured answer                    │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  API Gateway Response                                    │
│  {                                                       │
│    "statusCode": 200,                                   │
│    "headers": {"Content-Type": "application/json"},    │
│    "body": {                                            │
│      "answer": "PM-KISAN is a scheme...",              │
│      "sources": ["Source 1", "Source 2"]               │
│    }                                                    │
│  }                                                      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  User Browser (Frontend)                                 │
│  • Display answer in chat                               │
│  • Show source documents                                │
│  • Update conversation history                          │
└─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Cloud Infrastructure
- **AWS Lambda**: Serverless compute for event-driven functions
- **AWS S3**: Document storage + Static website hosting
- **AWS API Gateway**: RESTful API endpoint for frontend
- **AWS EC2**: FastAPI ingestion service hosting
- **Amazon OpenSearch Serverless**: Vector database for semantic search
- **AWS Bedrock**: Managed AI/ML models
- **AWS CloudWatch**: Logging and monitoring

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive styling
- **JavaScript (ES6+)**: API integration and UI logic

### AI/ML Models
- **Amazon Titan Embed Text v1**: Text embedding (1536 dimensions)
- **Amazon Nova Lite v1**: Large Language Model for text generation

### Backend Services
- **FastAPI**: High-performance Python web framework
- **Python 3.11**: Primary programming language

### Key Libraries
- **opensearch-py**: OpenSearch client
- **boto3**: AWS SDK for Python
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **langchain-text-splitters**: Document chunking
- **requests-aws4auth**: AWS authentication

---

## Data Models

### OpenSearch Index Schema

```json
{
  "index": "scheme-index",
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text"
      },
      "embedding": {
        "type": "knn_vector",
        "dimension": 1536
      },
      "source_file": {
        "type": "keyword"
      }
    }
  }
}
```

### API Request/Response Models

#### Ingestion API

**Request**:
```json
{
  "bucket": "government-schemes-bucket",
  "key": "schemes/pm-kisan.pdf"
}
```

**Response**:
```json
{
  "status": "success",
  "chunks": 15,
  "source": "schemes/pm-kisan.pdf"
}
```

#### Query API

**Request**:
```json
{
  "question": "What is PM-KISAN scheme?",
  "language": "en",
  "history": [
    {
      "role": "user",
      "content": "Tell me about farmer schemes"
    },
    {
      "role": "assistant",
      "content": "There are several schemes..."
    }
  ]
}
```

**Response**:
```json
{
  "statusCode": 200,
  "body": {
    "answer": "PM-KISAN is a scheme that provides...",
    "sources": [
      "PM-KISAN provides Rs 6000 per year...",
      "Eligibility criteria include...",
      "Application process involves..."
    ]
  }
}
```

---

## Configuration Management

### Environment Variables

All services use centralized configuration via `.env` file:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_SERVICE=aoss

# OpenSearch Configuration
OPENSEARCH_HOST=your-endpoint.aoss.amazonaws.com
OPENSEARCH_PORT=443
INDEX_NAME=scheme-index

# Bedrock Models
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1
LLM_MODEL_ID=amazon.nova-lite-v1:0
EMBEDDING_DIMENSION=1536

# Text Processing
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Query Processing
SEARCH_RESULTS_SIZE=3
KNN_K_VALUE=3
MAX_TOKENS=500
TEMPERATURE=0.1
```

### Shared AWS Clients

Single `aws_clients.py` module used across all services:
- Bedrock client initialization
- OpenSearch client with AWS4Auth
- S3 client initialization
- Centralized configuration management

---

## Security & Best Practices

### Security Measures

1. **Environment Variables**: Sensitive data in `.env` (not committed to git)
2. **AWS IAM Roles**: Least privilege access for Lambda functions
3. **AWS4Auth**: Secure authentication for OpenSearch
4. **HTTPS**: All API communications encrypted
5. **Input Validation**: Request validation using Pydantic models

### Code Quality

1. **Modular Design**: Separation of concerns across modules
2. **Type Hints**: Python type annotations throughout
3. **Documentation**: Comprehensive docstrings and comments
4. **Error Handling**: Graceful error handling with logging
5. **DRY Principle**: Shared utilities to avoid code duplication

### Performance Optimization

1. **Cold Start Optimization**: Clients initialized once in Lambda
2. **Efficient Chunking**: Optimal chunk size (500 chars) for context
3. **Vector Search**: KNN algorithm for fast similarity search
4. **Low Temperature**: 0.1 for factual, consistent responses
5. **Caching**: Index existence checked once during cold start

---

## Deployment Architecture

### Lambda Deployment

```bash
# Package Lambda function
cd lambda_functions/scheme_query_handler
pip install -r requirements.txt -t .
zip -r function.zip .

# Deploy to AWS
aws lambda update-function-code \
  --function-name scheme-query-handler \
  --zip-file fileb://function.zip
```

### FastAPI Deployment (EC2)

```bash
# Install dependencies
cd ingestion_api
pip install -r requirements.txt

# Run with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### S3 Trigger Configuration

```bash
# Configure S3 event notification
aws s3api put-bucket-notification-configuration \
  --bucket government-schemes-bucket \
  --notification-configuration file://s3-notification.json
```

---

## Monitoring & Observability

### CloudWatch Logs

All Lambda functions log to CloudWatch:
- Request/response details
- Embedding generation
- Search results
- Error traces
- Performance metrics

### Key Metrics

- **Ingestion**: Documents processed, chunks created, indexing time
- **Query**: Response time, search accuracy, user satisfaction
- **System**: Lambda invocations, error rates, cold starts

---

## Scalability & Performance

### Current Capacity

- **Ingestion**: ~100 documents/hour
- **Query**: ~1000 queries/minute
- **Storage**: Unlimited (S3 + OpenSearch Serverless)

### Scaling Strategy

1. **Horizontal Scaling**: Lambda auto-scales based on load
2. **OpenSearch**: Serverless auto-scaling
3. **FastAPI**: Deploy multiple EC2 instances with load balancer
4. **Caching**: Add Redis for frequently asked questions

---

## Future Enhancements

### Phase 2 Features

1. **Voice Interface**: Integration with Amazon Connect
2. **WhatsApp Bot**: Direct messaging support
3. **Personalization**: User profile-based recommendations
4. **Analytics Dashboard**: Usage statistics and insights
5. **Multi-modal**: Support for images and videos
6. **Regional Languages**: Support for 10+ Indian languages

### Technical Improvements

1. **Hybrid Search**: Combine vector + keyword search
2. **Re-ranking**: Improve search result relevance
3. **Fine-tuning**: Custom model for government schemes
4. **Feedback Loop**: Learn from user interactions
5. **A/B Testing**: Optimize prompts and parameters

---

## Project Structure

```
AI-For-Bharat-Hackathon/
├── frontend/                           # Web interface (S3 hosted)
│   ├── index.html                     # Main chat interface
│   ├── bucket-policy.json             # S3 bucket policy
│   └── README.md                      # Frontend documentation
├── backend/
│   ├── aws_clients.py                 # Shared AWS client initialization
│   ├── lambda_functions/              # AWS Lambda functions
│   │   ├── s3_event_ingestion_trigger/
│   │   │   ├── lambda_function.py
│   │   │   ├── requirements.txt
│   │   │   └── README.md
│   │   └── scheme_query_handler/      # RAG query processor
│   │       ├── lambda_function.py
│   │       ├── config.py
│   │       ├── prompts.py
│   │       ├── qna.py
│   │       ├── embedding_service.py
│   │       ├── opensearch_operations.py
│   │       ├── requirements.txt
│   │       └── README.md
│   └── ingestion_api/                 # FastAPI service
│       ├── app/
│       │   ├── main.py
│       │   ├── settings.py
│       │   ├── document_ingestion_service.py
│       │   ├── text_processing.py
│       │   ├── text_chunking.py
│       │   └── embedding_generator.py
│       ├── requirements.txt
│       └── README.md
├── .kiro/specs/                       # Project specifications
│   └── ai-government-scheme-navigator/
│       ├── requirements.md
│       └── design.md
├── docs/
│   └── architecture.md                # This file
├── scripts/                           # Deployment scripts
├── .env                               # Environment variables
├── .env.example                       # Example configuration
├── .gitignore
└── README.md
```

---

## Conclusion

The AI Government Scheme Navigator demonstrates a production-ready, scalable architecture for building intelligent conversational systems. By leveraging AWS serverless technologies and modern AI models, the system provides accurate, context-aware answers to help rural citizens access government schemes.

**Key Achievements**:
- ✅ Fully serverless and scalable
- ✅ RAG-based accurate responses
- ✅ Multi-language support
- ✅ Modular, maintainable codebase
- ✅ Production-ready security practices
- ✅ Comprehensive documentation

**Impact**:
- Increased scheme awareness among rural citizens
- Simplified eligibility understanding
- Reduced language barriers
- Improved government scheme utilization
