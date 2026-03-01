"""
AI model interactions using AWS Bedrock.
"""
import json
import boto3
from src.config import BEDROCK_MODEL_ID, MAX_TOKENS_EXPLANATION, MAX_TOKENS_EXTRACTION

bedrock = boto3.client('bedrock-runtime')


def invoke_bedrock_model(prompt, max_tokens=MAX_TOKENS_EXTRACTION, temperature=0):
    """
    Invoke AWS Bedrock model with given prompt.
    
    Args:
        prompt: Text prompt for the model
        max_tokens: Maximum tokens in response
        temperature: Model temperature setting
        
    Returns:
        Model response text
    """
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature
            }
        })
    )

    result = json.loads(response['body'].read())
    return result["output"]["message"]["content"][0]["text"]


def generate_explanation(user, eligible_schemes):
    """
    Generate human-readable explanation of eligibility results.
    
    Args:
        user: User profile dictionary
        eligible_schemes: List of eligible scheme IDs
        
    Returns:
        Explanation text
    """
    if not eligible_schemes:
        return "You are currently not eligible for any available schemes based on provided information."

    prompt = f"""
    User Profile:
    Income: {user['income']}
    Occupation: {user['occupation']}
    Age: {user['age']}
    Rural: {user['rural']}

    Eligible Schemes: {eligible_schemes}

    Explain clearly:
    1. Why the user is eligible
    2. Brief benefits of each scheme
    3. Use simple language
    """
    
    return invoke_bedrock_model(prompt, max_tokens=MAX_TOKENS_EXPLANATION)
