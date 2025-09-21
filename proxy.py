import json
import requests

def lambda_handler(event, context):
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
        # The backend service runs on localhost:8080 inside the container.
        url = "http://127.0.0.1:8080/v0/check_email"
        body = json.loads(event['body'])

        # Pass the entire body to the backend, as Reacher's API expects
        # more than just `to_email`.
        response = requests.post(url, json=body)
        response.raise_for_status()

        output = response.json()

        return {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps(output)
        }

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps({'error': f"Backend connection failed: {str(e)}"})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': response_headers,
            'body': json.dumps({'error': "Invalid JSON input."})
        }