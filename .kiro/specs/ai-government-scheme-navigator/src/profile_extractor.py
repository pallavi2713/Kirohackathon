"""
Natural language profile extraction using AI.
"""
import json
import re
from src.ai_service import invoke_bedrock_model
from src.validators import validate_profile


def call_extraction_model(user_text):
    """
    Extract structured profile data from natural language text.
    
    Args:
        user_text: User's natural language message
        
    Returns:
        JSON string with extracted profile data
    """
    prompt = f"""
You are a strict JSON extraction engine.

Extract:
- occupation (string or null)
- income (integer in INR, convert lakh to full number)
- age (integer or null)
- rural (true if village, false if city, else null)

Return ONLY valid JSON.
No explanation.
No extra text.

User Message:
{user_text}
"""

    return invoke_bedrock_model(prompt)


def fix_json_output(bad_output):
    """
    Attempt to fix malformed JSON output from extraction model.
    
    Args:
        bad_output: Invalid JSON string
        
    Returns:
        Fixed JSON string
    """
    fix_prompt = f"""
The following JSON is invalid or has wrong types.

Fix it and return ONLY valid JSON with:
occupation, income, age, rural

JSON:
{bad_output}
"""

    return invoke_bedrock_model(fix_prompt)


def extract_profile_from_text(user_text):
    """
    Extract and validate profile data from natural language text.
    
    Args:
        user_text: User's natural language message
        
    Returns:
        Validated profile dictionary
    """
    # Step 1: Call extraction model
    raw_output = call_extraction_model(user_text)

    # Step 2: Extract JSON block from response
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    if not match:
        return {}

    # Step 3: Parse JSON
    try:
        data = json.loads(match.group())
    except:
        return {}

    # Step 4: Validate extracted data
    validated = validate_profile(data)

    # If validation successful, return result
    if any(validated.values()):
        return validated

    # Step 5: Attempt to fix invalid JSON
    fixed_output = fix_json_output(raw_output)

    match = re.search(r"\{.*\}", fixed_output, re.DOTALL)
    if not match:
        return {}

    try:
        data = json.loads(match.group())
        return validate_profile(data)
    except:
        return {}
