"""
Configuration module for Chatbot Lambda.
Contains all environment variables and constants.
"""
import os

# AWS Configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_SERVICE = os.environ.get("AWS_SERVICE", "aoss")

# OpenSearch Configuration
OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "s511ek222mo165zg7ypb.us-east-1.aoss.amazonaws.com")
OPENSEARCH_PORT = int(os.environ.get("OPENSEARCH_PORT", "443"))
INDEX_NAME = os.environ.get("INDEX_NAME", "scheme-index")

# Bedrock Model Configuration
EMBEDDING_MODEL_ID = os.environ.get("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")
LLM_MODEL_ID = os.environ.get("LLM_MODEL_ID", "amazon.nova-lite-v1:0")
EMBEDDING_DIMENSION = int(os.environ.get("EMBEDDING_DIMENSION", "1536"))

# Search Configuration
SEARCH_RESULTS_SIZE = int(os.environ.get("SEARCH_RESULTS_SIZE", "3"))
KNN_K_VALUE = int(os.environ.get("KNN_K_VALUE", "3"))

# LLM Configuration
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "500"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.1"))  # Low temp for factual accuracy
REWRITE_MAX_TOKENS = int(os.environ.get("REWRITE_MAX_TOKENS", "100"))

