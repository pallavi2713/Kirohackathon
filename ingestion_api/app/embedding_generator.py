"""Embedding generation using AWS Bedrock."""
import json
from app.settings import BEDROCK_MODEL_ID


def generate_embedding(text: str, bedrock_client) -> list[float]:
    """
    Generate embedding for text using AWS Bedrock Titan model.
    
    Args:
        text: The text to generate embedding for
        bedrock_client: Boto3 Bedrock runtime client
        
    Returns:
        List of floats representing the embedding vector
    """
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response["body"].read())
    
    return response_body["embedding"]
