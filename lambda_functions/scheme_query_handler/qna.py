"""
Question-answering logic using RAG (Retrieval Augmented Generation).
Handles query rewriting, context retrieval, and answer generation.
"""
import json
from config import LLM_MODEL_ID, MAX_TOKENS, TEMPERATURE, REWRITE_MAX_TOKENS
from prompts import get_query_rewrite_prompt, get_answer_generation_prompt


def rewrite_query(bedrock_client, question, history):
    """
    Convert a follow-up question into a standalone question using conversation history.
    
    Args:
        bedrock_client: Boto3 Bedrock runtime client
        question: User's follow-up question
        history: Conversation history text
        
    Returns:
        str: Rewritten standalone question
    """
    prompt = get_query_rewrite_prompt(history, question)
    
    body = {
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {
            "maxTokens": REWRITE_MAX_TOKENS,
            "temperature": 0
        }
    }
    
    response = bedrock_client.invoke_model(
        modelId=LLM_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response["body"].read())
    
    return response_body["output"]["message"]["content"][0]["text"]


def generate_answer(bedrock_client, question, lang_instruction, context, history):
    """
    Generate answer using RAG approach with retrieved context and conversation history.
    
    Args:
        bedrock_client: Boto3 Bedrock runtime client
        question: User's question
        lang_instruction: Language instruction (English/Hindi)
        context: Retrieved context from OpenSearch
        history: Conversation history text
        
    Returns:
        str: Generated answer
    """
    prompt = get_answer_generation_prompt(lang_instruction, history, context, question)
    
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
    }
    
    response = bedrock_client.invoke_model(
        modelId=LLM_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response["body"].read())
    
    return response_body["output"]["message"]["content"][0]["text"]


def format_conversation_history(history):
    """
    Format conversation history into readable text.
    
    Args:
        history: List of conversation messages with role and content
        
    Returns:
        str: Formatted conversation history text
    """
    history_text = ""
    
    for msg in history:
        role = msg.get("role")
        content = msg.get("content")
        
        if role == "user":
            history_text += f"User: {content}\n"
        else:
            history_text += f"Assistant: {content}\n"
    
    print("History:", history_text, "------")
    return history_text

