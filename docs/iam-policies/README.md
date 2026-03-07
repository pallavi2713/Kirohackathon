# IAM Policies

This directory contains IAM policy templates for the AI Government Scheme Navigator.

## Policies

### 1. Lambda Execution Role (`lambda-execution-role.json`)

Attach this policy to the IAM role used by both Lambda functions:
- `s3_event_ingestion_trigger`
- `scheme_query_handler`

**Permissions:**
- CloudWatch Logs (for logging)
- S3 Read (for accessing uploaded documents)
- OpenSearch Serverless (for vector search)
- Bedrock (for embeddings and LLM)

**Setup:**
```bash
# Create IAM role
aws iam create-role \
  --role-name SchemeNavigatorLambdaRole \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach policy
aws iam put-role-policy \
  --role-name SchemeNavigatorLambdaRole \
  --policy-name SchemeNavigatorLambdaPolicy \
  --policy-document file://lambda-execution-role.json
```

### 2. EC2 Instance Role (`ec2-instance-role.json`)

Attach this policy to the IAM role used by the EC2 instance running FastAPI.

**Permissions:**
- S3 Read (for accessing uploaded documents)
- OpenSearch Serverless (for indexing documents)
- Bedrock (for generating embeddings)

**Setup:**
```bash
# Create IAM role
aws iam create-role \
  --role-name SchemeNavigatorEC2Role \
  --assume-role-policy-document file://ec2-trust-policy.json

# Attach policy
aws iam put-role-policy \
  --role-name SchemeNavigatorEC2Role \
  --policy-name SchemeNavigatorEC2Policy \
  --policy-document file://ec2-instance-role.json

# Attach role to EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-1234567890abcdef0 \
  --iam-instance-profile Name=SchemeNavigatorEC2Role
```

## Trust Policies

### Lambda Trust Policy

Create `lambda-trust-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### EC2 Trust Policy

Create `ec2-trust-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Important Notes

1. **Replace Placeholders**: Update `your-document-bucket` with your actual S3 bucket name
2. **Least Privilege**: These policies follow the principle of least privilege
3. **OpenSearch Access**: Ensure OpenSearch collection has data access policy allowing these roles
4. **Bedrock Access**: Ensure Bedrock models are enabled in your AWS region
5. **Region Specific**: Update region in ARNs if not using wildcards

## OpenSearch Data Access Policy

In addition to IAM policies, configure OpenSearch Serverless data access policy:

```json
[
  {
    "Rules": [
      {
        "ResourceType": "index",
        "Resource": ["index/scheme-index/*"],
        "Permission": ["aoss:*"]
      }
    ],
    "Principal": [
      "arn:aws:iam::YOUR-ACCOUNT-ID:role/SchemeNavigatorLambdaRole",
      "arn:aws:iam::YOUR-ACCOUNT-ID:role/SchemeNavigatorEC2Role"
    ]
  }
]
```

## Security Best Practices

- Use separate roles for Lambda and EC2
- Enable CloudTrail for audit logging
- Rotate credentials regularly
- Use VPC endpoints for private connectivity
- Enable encryption at rest and in transit
- Review and update policies regularly

