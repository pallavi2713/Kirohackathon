# S3 Event Ingestion Trigger Lambda Function

## Overview

This Lambda function is automatically triggered when a new document is uploaded to an S3 bucket. It forwards the S3 event to the FastAPI ingestion service running on EC2 for processing.

## Architecture Flow

```
S3 Bucket → Lambda Trigger → EC2 FastAPI → OpenSearch
```

1. User uploads document to S3
2. S3 triggers Lambda function
3. Lambda extracts bucket name and object key
4. Lambda sends POST request to EC2 FastAPI endpoint
5. EC2 processes document and indexes in OpenSearch

## Environment Variables

Configure these in AWS Lambda console:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `EC2_API_URL` | FastAPI ingestion endpoint URL | **Yes** | `http://your-ec2-ip:8000/ingest` |
| `REQUEST_TIMEOUT` | Request timeout in seconds | No | `50` |

**IMPORTANT**: 
- `EC2_API_URL` is **required** and must be set in Lambda environment variables
- Never hardcode the URL in the code
- The function will fail with a clear error if EC2_API_URL is not set

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt -t .
```

### 2. Create Deployment Package

```bash
zip -r lambda_function.zip .
```

### 3. Deploy to AWS Lambda

- Upload `lambda_function.zip` to AWS Lambda
- Set handler to `lambda_function.lambda_handler`
- Configure environment variables
- Set timeout to at least 60 seconds
- Attach IAM role with S3 read permissions

### 4. Configure S3 Trigger

- Go to S3 bucket settings
- Add event notification
- Select "All object create events"
- Choose Lambda function as destination

## Testing

### Sample S3 Event

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "your-bucket-name"
        },
        "object": {
          "key": "documents/sample.pdf"
        }
      }
    }
  ]
}
```

### Test Command

```bash
aws lambda invoke \
  --function-name s3-event-ingestion-trigger \
  --payload file://test_event.json \
  response.json
```

## Error Handling

The function handles:
- Missing records in event
- Invalid event structure
- Network timeouts
- Connection errors to EC2
- Unexpected errors

All errors are logged to CloudWatch Logs.

## Monitoring

Check CloudWatch Logs for:
- Successful ingestion triggers
- Error messages
- Response status codes
- Processing times
