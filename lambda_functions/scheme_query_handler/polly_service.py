"""
AWS Polly text-to-speech service for generating audio responses.
"""
import json
import uuid
import logging
import boto3
from config import AWS_REGION, POLLY_S3_BUCKET

logger = logging.getLogger(__name__)


def get_polly_client():
    """
    Initialize and return AWS Polly client.
    
    Returns:
        boto3.client: Polly client
    """
    return boto3.client("polly", region_name=AWS_REGION)


def get_s3_client():
    """
    Initialize and return AWS S3 client for audio storage.
    
    Returns:
        boto3.client: S3 client
    """
    return boto3.client("s3", region_name=AWS_REGION)


def text_to_speech(text, language="en"):
    """
    Convert text to speech using AWS Polly and store in S3.
    
    Args:
        text: Text to convert to speech
        language: Language code ("en" or "hi")
        
    Returns:
        str: S3 URL of the generated audio file, or None if error
    """
    try:
        polly_client = get_polly_client()
        s3_client = get_s3_client()
        
        # Choose voice based on language
        voice_id = "Aditi" if language == "hi" else "Joanna"
        lang_code = "hi-IN" if language == "hi" else "en-US"
        
        # Generate speech
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId=voice_id,
            LanguageCode=lang_code
        )
        
        audio_stream = response["AudioStream"].read()
        
        # Generate unique file name
        audio_file_name = f"polly_outputs/{str(uuid.uuid4())}.mp3"
        
        # Upload to S3
        s3_client.put_object(
            Bucket=POLLY_S3_BUCKET,
            Key=audio_file_name,
            Body=audio_stream,
            ContentType="audio/mpeg"
        )
        
        # Return S3 URL
        audio_url = f"https://{POLLY_S3_BUCKET}.s3.amazonaws.com/{audio_file_name}"
        logger.info(f"Audio generated successfully: {audio_url}")
        
        return audio_url
        
    except Exception as e:
        logger.error(f"Polly text-to-speech error: {str(e)}", exc_info=True)
        return None
