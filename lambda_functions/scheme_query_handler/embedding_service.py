"""
Embedding generation service using AWS Bedrock Titan model.
"""
import json
import logging
from config import EMBEDDING_MODEL_ID

logger = logging.getLogger(__name__)


def generate_embedding(bedrock_client, text):
    """
    Generate embedding vector for given text using Bedrock Titan model.
    
    Args:
        bedrock_client: Boto3 Bedrock runtime client
        text: Text to generate embedding for
        
    Returns:
        list: Embedding vector
    """
    response = bedrock_client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=json.dumps({"inputText": text})
    )
    
    response_body = json.loads(response["body"].read())
    logger.debug(f"Embedding generated with dimension: {len(response_body['embedding'])}")
    
    return response_body["embedding"]
