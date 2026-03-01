"""
Question flow management for collecting user profile information.
"""
from src.config import QUESTION_FLOW


def get_next_question(user_profile):
    """
    Determine the next question to ask based on missing profile fields.
    
    Args:
        user_profile: Dictionary containing user profile data
        
    Returns:
        Tuple of (field_name, question_text) or (None, None) if complete
    """
    for field, question in QUESTION_FLOW:
        if user_profile.get(field) is None:
            return field, question
    return None, None
