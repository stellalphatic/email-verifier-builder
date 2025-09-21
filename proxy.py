import json
import requests
import os

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'  # CORS allow
    }
    
    try:
        url = "http://127.0.0.1:8080/v0/check_email"
        body = json.loads(event['body'])
        to_email = body['to_email']
        payload = {"to_email": to_email}
        
        response = requests.post(url, json=payload)
        response.raise_for_status() 

        output = response.json()

        return {
            'statusCode': 200,
            'headers': headers, 
            'body': json.dumps(output)
        }

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f"Failed to connect to the email verification backend: {str(e)}"})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers, 
            'body': json.dumps({'error': "Invalid JSON input."})
        }
    except KeyError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': "Missing 'to_email' field in request body."})
        }