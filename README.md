# AI Government Scheme Navigator

An AI-powered conversational system to help rural citizens discover and understand government schemes they are eligible for.

## Project Structure

```
AI-For-Bharat-Hackathon/
├── frontend/                       # Web interface (S3 hosted)
│   ├── index.html                 # Main chat interface
│   ├── bucket-policy.json         # S3 bucket policy
│   └── README.md                  # Frontend documentation
├── backend/
│   ├── aws_clients.py             # Shared AWS client initialization
│   ├── lambda_functions/          # AWS Lambda functions
│   │   ├── s3_event_ingestion_trigger/
│   │   └── scheme_query_handler/
│   └── ingestion_api/             # Document ingestion service
├── .kiro/specs/                   # Project specifications
├── scripts/                       # Deployment scripts
├── docs/                          # Documentation
├── .env                           # Environment variables
├── .env.example                   # Example configuration
├── .gitignore
└── README.md
```

## Quick Start

1. Clone the repository
2. **IMPORTANT**: Copy `.env.example` to `.env` and configure with your actual values:
   ```bash
   cp .env.example .env
   ```
3. **Never commit `.env` to git** - it contains sensitive information
4. Update `.env` with your AWS credentials, OpenSearch endpoint, and EC2 URL
5. Follow setup instructions in each component's README

## Security Best Practices

- ✅ `.env` is in `.gitignore` - never commit it
- ✅ Use `.env.example` with placeholder values for documentation
- ✅ Store actual credentials only in `.env` locally or in AWS Secrets Manager
- ✅ Rotate credentials regularly

## Components

### FastAPI Ingestion API
Document ingestion service that processes files from S3 and indexes them in OpenSearch.
See [fastapi_ingestion_api/README.md](fastapi_ingestion_api/README.md) for details.

### Lambda Functions
- **S3 Event Ingestion Trigger**: Automatically triggers document ingestion when files are uploaded to S3
- **Chatbot**: Handles user queries and provides scheme recommendations

## Environment Variables

All environment variables are managed in the project root `.env` file. See `.env.example` for required configuration.

## Documentation

- [Architecture](docs/architecture.md)
- [Requirements](.kiro/specs/ai-government-scheme-navigator/requirements.md)
- [Design](.kiro/specs/ai-government-scheme-navigator/design.md)
