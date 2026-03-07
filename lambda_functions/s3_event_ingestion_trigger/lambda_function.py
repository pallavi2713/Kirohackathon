"""
AWS Lambda Function: S3 Event Ingestion Trigger
================================================
This Lambda function is triggered when a new document is uploaded to S3.
It forwards the S3 event to the FastAPI ingestion service running on EC2.

Flow:
1. S3 event triggers Lambda
2. Lambda extracts bucket and key from event
3. Lambda sends POST request to EC2 FastAPI endpoint
4. EC2 processes the document and indexes it in OpenSearch

Author: AI-For-Bharat-Hackathon Team
"""

import json
import os
import requests


# ============================================
# Configuration - Environment Variables
# ============================================

# EC2 FastAPI ingestion endpoint URL
# REQUIRED: Must be set in Lambda environment variables
EC2_API_URL = os.environ.get("EC2_API_URL")

if not EC2_API_URL:
    raise ValueError("EC2_API_URL environment variable is required but not set")

# Request timeout in seconds
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "50"))


# ============================================
# Lambda Handler Function
# ============================================

def lambda_handler(event, context):
    """
    Main Lambda handler function triggered by S3 events.
    
    Args:
        event (dict): S3 event containing bucket and object information
        context (object): Lambda context object
        
    Returns:
        dict: Response with statusCode and body
    """
    
    try:
        # Extract S3 records from the event
        records = event.get("Records", [])
        
        if not records:
            print("Warning: No records found in event")
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "No records found in event"})
            }
        
        # Process each S3 record
        for record in records:
            # Extract bucket name and object key
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            print(f"Processing S3 event: bucket={bucket}, key={key}")
            
            # Prepare payload for EC2 ingestion API
            payload = {
                "bucket": bucket,
                "key": key
            }
            
            # Send POST request to EC2 FastAPI endpoint
            response = requests.post(
                EC2_API_URL, 
                json=payload, 
                timeout=REQUEST_TIMEOUT
            )
            
            # Log the response
            print(f"Successfully triggered EC2 ingestion for {bucket}/{key}")
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
        
        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "EC2 ingestion triggered successfully",
                "processed_records": len(records)
            })
        }
        
    except KeyError as e:
        # Handle missing keys in event structure
        error_msg = f"Missing required field in event: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": error_msg})
        }
        
    except requests.exceptions.Timeout:
        # Handle request timeout
        error_msg = f"Request to EC2 API timed out after {REQUEST_TIMEOUT} seconds"
        print(f"Error: {error_msg}")
        return {
            "statusCode": 504,
            "body": json.dumps({"error": error_msg})
        }
        
    except requests.exceptions.RequestException as e:
        # Handle other request errors
        error_msg = f"Failed to connect to EC2 API: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "statusCode": 502,
            "body": json.dumps({"error": error_msg})
        }
        
    except Exception as e:
        # Handle any other unexpected errors
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": error_msg})
        }
