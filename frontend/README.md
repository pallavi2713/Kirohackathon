# Frontend - AI Government Scheme Navigator

## Overview

Static web application hosted on AWS S3 for interacting with the AI Government Scheme Navigator chatbot.

## Architecture

```
User Browser → S3 Static Website → API Gateway → Lambda (Scheme Query Handler)
```

## Features

- Simple, responsive chat interface
- Multi-language support (English/Hindi)
- Conversation history
- Source document display
- Voice input support
- Mobile-friendly design

## Files

- `index.html` - Main chat interface with embedded styles and scripts
- `config.js` - API configuration (gitignored, create from example)
- `config.example.js` - Example configuration template
- `bucket-policy.json` - S3 bucket policy for public access
- `README.md` - This file

## Quick Start

### 1. Setup Configuration

**IMPORTANT**: Create your `config.js` file before deploying:

```bash
# Copy the example config
cp config.example.js config.js

# Edit config.js and update API_ENDPOINT with your actual API Gateway URL
# Example: https://abc123.execute-api.us-east-1.amazonaws.com/prod/ask
```

Your `config.js` should look like:

```javascript
const CONFIG = {
    API_ENDPOINT: 'https://your-actual-api-gateway-url.amazonaws.com/prod/ask',
    DEFAULT_LANGUAGE: 'en',
    MAX_HISTORY: 10,
    REQUEST_TIMEOUT: 30000
};
```

### 2. Configure S3 Bucket

```bash
# Create S3 bucket (use a unique name)
aws s3 mb s3://your-scheme-navigator-frontend

# Enable static website hosting
aws s3 website s3://your-scheme-navigator-frontend \
  --index-document index.html

# Update bucket name in bucket-policy.json, then apply policy
aws s3api put-bucket-policy \
  --bucket your-scheme-navigator-frontend \
  --policy file://bucket-policy.json
```

### 3. Upload Files

```bash
# Upload all frontend files to S3
aws s3 sync . s3://your-scheme-navigator-frontend \
  --exclude "README.md" \
  --exclude "bucket-policy.json" \
  --exclude "config.example.js"

# Verify config.js is uploaded
aws s3 ls s3://your-scheme-navigator-frontend/
```

### 4. Access Your Application

Get your S3 website endpoint:

```bash
aws s3api get-bucket-website \
  --bucket your-scheme-navigator-frontend
```

Visit: `http://your-scheme-navigator-frontend.s3-website-us-east-1.amazonaws.com`

## Configuration

### API Endpoint

The frontend uses `config.js` to store the API Gateway endpoint. This file is gitignored to prevent committing environment-specific URLs.

**For hackathon judges/reviewers**: Copy `config.example.js` to `config.js` and update the `API_ENDPOINT` value.

### Environment Variables Reference

The backend `.env` file contains `API_GATEWAY_ENDPOINT`. Copy this value to your frontend `config.js`:

```
Backend .env: API_GATEWAY_ENDPOINT=https://...
Frontend config.js: API_ENDPOINT: 'https://...'
```

## API Integration

### Request Format

```javascript
fetch(CONFIG.API_ENDPOINT, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: "What is PM-KISAN?",
    language: "en",
    history: []
  })
})
```

### Response Format

```json
{
  "answer": "PM-KISAN is a scheme...",
  "sources": ["Source 1", "Source 2"]
}
```

## Local Development

For local testing with CORS:

```bash
# Start a simple HTTP server
python -m http.server 8080

# Or use Node.js
npx http-server -p 8080
```

Then visit: `http://localhost:8080`

**Note**: Make sure your API Gateway has CORS enabled for local testing.

## S3 Bucket Policy

Update the bucket name in `bucket-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## CORS Configuration

Ensure API Gateway has CORS enabled:

- **Allowed Origins**: `*` (or your S3 website URL)
- **Allowed Methods**: `POST`, `OPTIONS`
- **Allowed Headers**: `Content-Type`

## Testing

1. Open the S3 website URL in your browser
2. Type a question: "What is PM-KISAN?"
3. Verify the response appears correctly
4. Test language switching (English/Hindi)
5. Test conversation history
6. Test voice input (requires HTTPS or localhost)

## Troubleshooting

### CORS Errors
- Check API Gateway CORS settings
- Verify `Access-Control-Allow-Origin` header is set

### 404 Errors
- Verify S3 bucket is configured for static website hosting
- Check bucket policy allows public read access
- Ensure `index.html` is uploaded

### API Connection Errors
- Verify `config.js` has the correct API Gateway endpoint
- Check Lambda function is deployed and working
- Review CloudWatch logs for Lambda errors

### Voice Input Not Working
- Voice input requires HTTPS or localhost
- Check browser permissions for microphone access

## Monitoring

- **CloudWatch**: API Gateway and Lambda logs
- **S3 Access Logs**: Frontend access patterns
- **Browser Console**: Client-side errors and network requests

## Security Notes

- `config.js` is gitignored to prevent committing API endpoints
- API Gateway URL is public but should be protected by:
  - API keys (optional)
  - Rate limiting
  - WAF rules (optional)
- S3 bucket policy allows public read for static assets only

## Future Enhancements

- Progressive Web App (PWA) support
- Enhanced voice input/output
- File upload for eligibility check
- Scheme comparison tool
- Bookmark favorite schemes
- Dark mode toggle
- Multi-language UI (not just responses)

