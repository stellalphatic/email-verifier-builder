import json
import requests
import subprocess
import os
import time
import logging

# Configure logging for better visibility in CloudWatch logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The backend will run on localhost, so we define the URL here.
# Note: The ReacherHQ backend runs on port 8080 by default.
REACHER_URL = "http://127.0.0.1:8080/v0/check_email"

# A global variable to hold the backend process.
REACHER_PROCESS = None

def start_reacher_backend():
    """
    Starts the ReacherHQ backend as a subprocess and performs a health check.
    This function is designed to be idempotent and only starts the process once.
    """
    global REACHER_PROCESS

    # Check if the process is already running. `poll()` returns None if it's active.
    if REACHER_PROCESS and REACHER_PROCESS.poll() is None:
        logger.info("Reacher backend is already running.")
        return

    logger.info("Starting Reacher backend as a subprocess...")
    try:
        # We need to find the executable inside the container.
        # The `reacherhq/backend` image's entrypoint is `reacher`, but we need to run it as a detached process.
        # We can directly run the executable located at /reacher.
        # This will start the web server on port 8080 by default.
        REACHER_PROCESS = subprocess.Popen(["/reacher"])
        
        # Wait for the backend to start with a health check.
        # This is more reliable than a simple time.sleep()
        for i in range(30): # Wait up to 30 seconds
            try:
                # The backend has a health endpoint, let's use that.
                health_url = "http://127.0.0.1:8080/healthz"
                response = requests.get(health_url, timeout=1)
                if response.status_code == 200:
                    logger.info("Reacher backend is ready.")
                    return
            except requests.exceptions.RequestException:
                time.sleep(1)

        logger.error("Reacher backend failed to start or become ready within the timeout.")
        if REACHER_PROCESS:
            REACHER_PROCESS.terminate()
        REACHER_PROCESS = None
        raise Exception("Backend initialization failed.")
    
    except Exception as e:
        logger.error(f"Failed to start backend process: {e}")
        REACHER_PROCESS = None
        raise

def lambda_handler(event, context):
    """
    The Lambda function handler that proxies requests to the ReacherHQ backend.
    """
    # Ensure the backend is running for every invocation. This is crucial for Lambda.
    try:
        start_reacher_backend()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to initialize ReacherHQ backend: {str(e)}"})
        }

    response_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'OPTIONS,POST'
    }

    # Handle the OPTIONS preflight request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': response_headers,
            'body': ''
        }

    # Handle the POST request
    try:
        # Pass the entire body to the backend, as Reacher's API expects the `to_email` field.
        body = json.loads(event['body'])
        response = requests.post(REACHER_URL, json=body)
        response.raise_for_status()

        output = response.json()

        return {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps(output)
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Backend connection failed: {e}")
        return {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps({'error': f"Backend connection failed: {str(e)}"})
        }
    except json.JSONDecodeError:
        logger.error("Invalid JSON input received.")
        return {
            'statusCode': 400,
            'headers': response_headers,
            'body': json.dumps({'error': "Invalid JSON input."})
        }