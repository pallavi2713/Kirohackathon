"""
Service for retrieving and filtering government schemes.
"""
import boto3
from src.config import SCHEMES_TABLE
from src.eligibility import is_eligible

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(SCHEMES_TABLE)


def get_eligible_schemes(user_profile):
    """
    Retrieve all schemes and filter by user eligibility.
    
    Args:
        user_profile: Dictionary containing user profile data
        
    Returns:
        List of eligible scheme IDs
    """
    response = table.scan()
    schemes = response['Items']

    eligible = []
    for scheme in schemes:
        if is_eligible(user_profile, scheme):
            eligible.append(scheme["scheme_id"])

    return eligible
