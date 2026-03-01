"""
Profile validation and normalization utilities.
"""


def validate_profile(data):
    """
    Validate and sanitize user profile data.
    
    Args:
        data: Dictionary containing profile fields
        
    Returns:
        Dictionary with validated fields (occupation, income, age, rural)
    """
    validated = {
        "occupation": None,
        "income": None,
        "age": None,
        "rural": None
    }

    if isinstance(data.get("occupation"), str):
        validated["occupation"] = data["occupation"]

    if isinstance(data.get("income"), int):
        validated["income"] = data["income"]

    if isinstance(data.get("age"), int):
        validated["age"] = data["age"]

    if isinstance(data.get("rural"), bool):
        validated["rural"] = data["rural"]

    return validated


def normalize_user_input(event):
    """
    Extract profile fields from event payload.
    
    Args:
        event: Lambda event dictionary
        
    Returns:
        Dictionary with profile fields
    """
    return {
        "occupation": event.get("occupation"),
        "income": event.get("income"),
        "age": event.get("age"),
        "rural": event.get("rural")
    }
