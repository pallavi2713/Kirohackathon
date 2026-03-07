"""
AWS Lambda Function: Government Scheme Chatbot
===============================================
This Lambda function provides a conversational AI interface for answering
questions about Indian Government Schemes using RAG (Retrieval Augmented Generation).

Flow:
1. Receive user question and conversation history
2. Rewrite follow-up questions into standalone queries
3. Generate embedding for the query
4. Search OpenSearch for relevant scheme information
5. Generate answer using LLM with retrieved context
6. Return answer with source documents

Features:
- Multi-language support (English/Hindi)
- Conversation history tracking
- Context-aware follow-up questions
- Vector similarity search
- RAG-based answer generation

Author: AI-For-Bharat-Hackathon Team
"""

import json
import sys
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add project root to path for aws_clients
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.aws_clients import get_bedrock_client, get_opensearch_client
from opensearch_operations import create_index_if_not_exists, search_opensearch
from embedding_service import generate_embedding
from qna import rewrite_query, generate_answer, format_conversation_history
from polly_service import text_to_speech


# ============================================
# Initialize AWS Clients (Cold Start)
# ============================================

# Initialize clients once during cold start for better performance
bedrock_client = get_bedrock_client()
opensearch_client = get_opensearch_client()

# Ensure index exists
create_index_if_not_exists(opensearch_client)


# ============================================
# Lambda Handler Function
# ============================================

def lambda_handler(event, context):
    """
    Main Lambda handler function for chatbot queries.
    
    Args:
        event (dict): API Gateway event or direct Lambda test event
        context (object): Lambda context object
        
    Returns:
        dict: Response with statusCode, answer, and sources
    """
    
    # Step 1: Parse request body
    body = event.get("body")
    
    if body:
        # Body is a string (from API Gateway)
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON in body"})
            }
    else:
        # Direct Lambda test, body is the event itself
        body = event
    
    # Step 2: Extract parameters
    question = body.get("question")
    language = body.get("language", "en")
    history = body.get("history", [])
    
    # Validate required parameters
    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Question is required"})
        }
    
    # Step 3: Format conversation history
    history_text = format_conversation_history(history)
    
    # Step 4: Determine language instruction
    lang_instruction = "Answer in Hindi." if language == "hi" else "Answer in English."
    
    # Step 5: Process query and generate answer
    try:
        # Rewrite follow-up question into standalone question
        rewritten_question = rewrite_query(bedrock_client, question, history_text)
        logger.info(f"Rewritten Question: {rewritten_question}")
        
        # Generate embedding for the rewritten question
        embedding = generate_embedding(bedrock_client, rewritten_question)
        
        # Search OpenSearch for relevant context
        retrieved_context = search_opensearch(opensearch_client, embedding)
        context_text = "\n".join(retrieved_context)
        
        # Generate final answer using LLM
        answer = generate_answer(
            bedrock_client,
            question,
            lang_instruction,
            context_text,
            history_text
        )
        
        # Generate speech audio using AWS Polly
        audio_url = text_to_speech(answer, language=language)
        
    except Exception as e:
        # Catch any errors for better debugging
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }
    
    # Step 6: Return successful response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "answer": answer,
            "sources": retrieved_context,
            "audio_url": audio_url
        })
    }
