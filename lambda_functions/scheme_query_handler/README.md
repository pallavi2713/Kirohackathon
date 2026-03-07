# Government Scheme Chatbot Lambda Function

## Overview

This Lambda function provides an AI-powered conversational interface for answering questions about Indian Government Schemes. It uses RAG (Retrieval Augmented Generation) to provide accurate, context-aware answers.

## Architecture

```
User Question → Lambda → Query Rewriting → Embedding Generation → 
OpenSearch Vector Search → Context Retrieval → LLM Answer Generation → Response
```

## Features

- **Multi-language Support**: English and Hindi
- **Conversation History**: Maintains context across multiple turns
- **Follow-up Questions**: Automatically rewrites follow-up questions into standalone queries
- **Vector Search**: Uses KNN similarity search in OpenSearch
- **RAG Pipeline**: Combines retrieved context with LLM for accurate answers
- **Source Attribution**: Returns source documents used for answer generation

## Project Structure

```
chatbot_lambda/
├── lambda_function.py           # Main Lambda handler
├── config.py                    # Configuration and environment variables
├── aws_clients.py               # AWS client initialization (Bedrock, OpenSearch)
├── opensearch_operations.py     # OpenSearch index and search operations
├── embedding_service.py         # Embedding generation with Bedrock Titan
├── qna.py                       # Question-answering logic (RAG pipeline)
├── prompts.py                   # Prompt templates for LLM
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Environment Variables

Configure these in AWS Lambda console or use the project root `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_SERVICE` | AWS service name | `aoss` |
| `OPENSEARCH_HOST` | OpenSearch endpoint | Required |
| `OPENSEARCH_PORT` | OpenSearch port | `443` |
| `INDEX_NAME` | OpenSearch index name | `scheme-index` |
| `EMBEDDING_MODEL_ID` | Bedrock embedding model | `amazon.titan-embed-text-v1` |
| `LLM_MODEL_ID` | Bedrock LLM model | `amazon.nova-lite-v1:0` |
| `EMBEDDING_DIMENSION` | Embedding vector dimension | `1536` |
| `SEARCH_RESULTS_SIZE` | Number of search results | `3` |
| `KNN_K_VALUE` | KNN k value | `3` |
| `MAX_TOKENS` | Max tokens for answer | `500` |
| `TEMPERATURE` | LLM temperature | `0.2` |

## Request Format

### API Gateway Request

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
      "content": "There are several schemes for farmers..."
    }
  ]
}
```

### Parameters

- `question` (required): User's question
- `language` (optional): `"en"` for English, `"hi"` for Hindi (default: `"en"`)
- `history` (optional): Array of previous conversation messages

## Response Format

```json
{
  "statusCode": 200,
  "body": {
    "answer": "PM-KISAN is a scheme that provides...",
    "sources": [
      "PM-KISAN scheme provides Rs 6000 per year...",
      "Eligibility criteria include...",
      "Application process involves..."
    ]
  }
}
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt -t .
```

### 2. Create Deployment Package

```bash
zip -r chatbot_lambda.zip .
```

### 3. Deploy to AWS Lambda

- Upload `chatbot_lambda.zip` to AWS Lambda
- Set handler to `lambda_function.lambda_handler`
- Configure environment variables
- Set timeout to at least 60 seconds
- Set memory to at least 512 MB
- Attach IAM role with permissions:
  - Bedrock: `InvokeModel`
  - OpenSearch: Read/Write access
  - CloudWatch: Logs

### 4. Configure API Gateway (Optional)

- Create REST API or HTTP API
- Add POST method
- Integrate with Lambda function
- Enable CORS if needed

## Testing

### Direct Lambda Test

```json
{
  "question": "What is PM-KISAN?",
  "language": "en",
  "history": []
}
```

### Test Command

```bash
aws lambda invoke \
  --function-name government-scheme-chatbot \
  --payload file://test_event.json \
  response.json
```

## Error Handling

The function handles:
- Invalid JSON in request body
- Missing required parameters
- Bedrock API errors
- OpenSearch connection errors
- Unexpected exceptions

All errors are logged to CloudWatch Logs with detailed information.

## Monitoring

Check CloudWatch Logs for:
- Rewritten queries
- Embedding generation
- Search results
- Generated answers
- Error messages
- Performance metrics

## Performance Optimization

- Clients initialized during cold start (reused across invocations)
- Index existence checked once during cold start
- Efficient vector search with KNN
- Configurable search result size
- Optimized LLM parameters

## Multi-language Support

The chatbot supports:
- **English** (`language: "en"`): Default language
- **Hindi** (`language: "hi"`): Answers in Hindi

Language instruction is passed to the LLM to ensure responses in the requested language.
