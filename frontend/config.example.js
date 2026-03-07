/**
 * Frontend Configuration Example
 * Copy this file to config.js and update with your actual API Gateway endpoint
 */

const CONFIG = {
    // API Gateway endpoint - UPDATE THIS with your actual endpoint
    API_ENDPOINT: 'https://your-api-id.execute-api.region.amazonaws.com/prod/ask',
    
    // Default language
    DEFAULT_LANGUAGE: 'en',
    
    // Maximum conversation history to maintain
    MAX_HISTORY: 10,
    
    // Request timeout in milliseconds
    REQUEST_TIMEOUT: 30000
};
