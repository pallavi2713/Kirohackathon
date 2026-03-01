"""
Eligibility checking logic for government schemes.
"""


def is_eligible(user, scheme):
    """
    Check if user is eligible for a specific scheme.
    
    Args:
        user: Dictionary containing user profile
        scheme: Dictionary containing scheme requirements
        
    Returns:
        Boolean indicating eligibility
    """
    if user["income"] is None or user["age"] is None or user["occupation"] is None or user["rural"] is None:
        return False

    if user["income"] > scheme["max_income"]:
        return False
        
    if scheme["occupation"] != "any" and user["occupation"] != scheme["occupation"]:
        return False
        
    if scheme["rural_required"] and not user["rural"]:
        return False
        
    if user["age"] < scheme["min_age"] or user["age"] > scheme["max_age"]:
        return False
        
    return True
