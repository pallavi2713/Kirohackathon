"""
AWS Lambda function for AI Government Scheme Navigator.
Main handler for user profile collection, eligibility checking, and scheme recommendations.
"""
from src.session_manager import get_or_create_session, save_session
from src.validators import normalize_user_input
from src.profile_extractor import extract_profile_from_text
from src.question_flow import get_next_question
from src.scheme_service import get_eligible_schemes
from src.ai_service import generate_explanation


def lambda_handler(event, context):
    """
    Main Lambda handler for government scheme navigator.
    
    Args:
        event: Lambda event containing session_id and message
        context: Lambda context object
        
    Returns:
        Dictionary with status and response data
    """
    session_id = event.get("session_id")
    user_message = event.get("message")

    if not session_id:
        return {"error": "session_id required"}

    # Step 1: Get or create session
    session = get_or_create_session(session_id)

    # Step 2: Store user message in history
    if user_message:
        session["messages"].append({
            "role": "user",
            "text": user_message
        })

    # Step 3: Extract structured data from multiple sources
    incoming = {}

    # Extract from natural language message
    if user_message:
        extracted = extract_profile_from_text(user_message)
        incoming.update(extracted)

    # Also allow direct structured JSON input (for testing)
    structured = normalize_user_input(event)
    for key in structured:
        if structured[key] is not None:
            incoming[key] = structured[key]

    # Step 4: Merge extracted data into stored profile
    for key in incoming:
        if incoming[key] is not None:
            session["profile"][key] = incoming[key]

    # Step 5: Check for missing profile fields
    field, question = get_next_question(session["profile"])

    if field:
        session["messages"].append({
            "role": "assistant",
            "text": question
        })

        save_session(session)

        return {
            "status": "incomplete",
            "next_question": question,
            "current_profile": session["profile"]
        }

    # Step 6: All data collected - run eligibility check
    eligible = get_eligible_schemes(session["profile"])

    # Step 7: Generate explanation using AI
    explanation = generate_explanation(session["profile"], eligible)

    session["messages"].append({
        "role": "assistant",
        "text": explanation
    })

    save_session(session)

    return {
        "status": "complete",
        "eligible_schemes": eligible,
        "explanation": explanation
    }
