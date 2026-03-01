"""
Session management for user interactions.
"""
import boto3
from src.config import SESSIONS_TABLE

dynamodb = boto3.resource('dynamodb')
sessions_table = dynamodb.Table(SESSIONS_TABLE)


def get_or_create_session(session_id):
    """
    Retrieve existing session or create a new one.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Session dictionary with profile and messages
    """
    response = sessions_table.get_item(Key={"session_id": session_id})
    
    if "Item" in response:
        return response["Item"]
    
    new_session = {
        "session_id": session_id,
        "profile": {
            "occupation": None,
            "income": None,
            "age": None,
            "rural": None
        },
        "messages": []
    }
    
    sessions_table.put_item(Item=new_session)
    return new_session


def save_session(session):
    """
    Persist session data to DynamoDB.
    
    Args:
        session: Session dictionary to save
    """
    sessions_table.put_item(Item=session)
