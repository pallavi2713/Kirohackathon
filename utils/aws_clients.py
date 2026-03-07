"""
Shared AWS client initialization for all services.
Used by Lambda functions and ingestion API.
"""
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def get_aws_config():
    """
    Get AWS configuration from environment variables.
    
    Returns:
        dict: AWS configuration parameters
    """
    return {
        "region": os.environ.get("AWS_REGION"),
        "service": os.environ.get("AWS_SERVICE", "aoss"),
        "opensearch_host": os.environ.get("OPENSEARCH_HOST"),
        "opensearch_port": int(os.environ.get("OPENSEARCH_PORT", "443"))
    }


def get_aws_auth(region=None, service=None):
    """
    Get AWS4Auth for OpenSearch authentication.
    
    Args:
        region: AWS region (optional, uses env var if not provided)
        service: AWS service name (optional, uses env var if not provided)
        
    Returns:
        AWS4Auth: Authentication object for OpenSearch
    """
    config = get_aws_config()
    region = region or config["region"]
    service = service or config["service"]
    
    credentials = boto3.Session().get_credentials()
    
    return AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token
    )


def get_opensearch_client(host=None, port=None):
    """
    Initialize and return OpenSearch client with AWS authentication.
    
    Args:
        host: OpenSearch host (optional, uses env var if not provided)
        port: OpenSearch port (optional, uses env var if not provided)
        
    Returns:
        OpenSearch: Authenticated OpenSearch client
    """
    config = get_aws_config()
    host = host or config["opensearch_host"]
    port = port or config["opensearch_port"]
    
    awsauth = get_aws_auth()
    
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    
    return client


def get_bedrock_client(region=None):
    """
    Initialize and return AWS Bedrock runtime client.
    
    Args:
        region: AWS region (optional, uses env var if not provided)
        
    Returns:
        boto3.client: Bedrock runtime client
    """
    config = get_aws_config()
    region = region or config["region"]
    
    return boto3.client("bedrock-runtime", region_name=region)


def get_s3_client(region=None):
    """
    Initialize and return AWS S3 client.
    
    Args:
        region: AWS region (optional, uses env var if not provided)
        
    Returns:
        boto3.client: S3 client
    """
    config = get_aws_config()
    region = region or config["region"]
    
    return boto3.client("s3", region_name=region)
