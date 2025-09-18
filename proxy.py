import json
import requests
import os

def lambda_handler(event, context):
    try:
        # The URL for the Reacher backend's API endpoint.
        # It runs on localhost at port 8080.
        url = "http://127.0.0.1:8080/v0/check_email"

        # Extract the email from the API Gateway event body.
        body = json.loads(event['body'])
        to_email = body['to_email']
        
        # Prepare the payload for the API request.
        payload = {
            "to_email": to_email
        }
        
        # Send a POST request to the Reacher backend.
        response = requests.post(url, json=payload)
        response.raise_for_status() 

        output = response.json()

        return {
            'statusCode': 200,
            'body': json.dumps(output)
        }

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to connect to the email verification backend: {str(e)}"})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': "Invalid JSON input."})
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': "Missing 'to_email' field in request body."})
        }