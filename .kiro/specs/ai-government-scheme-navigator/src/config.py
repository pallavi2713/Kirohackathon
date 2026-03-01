"""
Configuration constants for the AI Government Scheme Navigator.
"""

# Question flow for collecting user profile
QUESTION_FLOW = [
    ("occupation", "What is your occupation? (farmer / student / self-employed / other)"),
    ("income", "What is your annual income in INR?"),
    ("age", "What is your age?"),
    ("rural", "Do you live in a rural area? (yes/no)")
]

# AWS Bedrock configuration
BEDROCK_MODEL_ID = "amazon.nova-lite-v1:0"
MAX_TOKENS_EXPLANATION = 500
MAX_TOKENS_EXTRACTION = 200

# DynamoDB table names
SCHEMES_TABLE = 'schemes'
SESSIONS_TABLE = 'UserSessions'
