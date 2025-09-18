import json
import subprocess
import os

def lambda_handler(event, context):
    try:
        # Extract email from API Gateway event
        body = json.loads(event['body'])
        to_email = body['to_email']

        # Call the Rust CLI tool with the email
        result = subprocess.run(
            ["/usr/local/bin/check_if_email_exists", to_email, "--json"],
            capture_output=True,
            text=True,
            check=True
        )

        output = json.loads(result.stdout)

        return {
            'statusCode': 200,
            'body': json.dumps(output)
        }

    except subprocess.CalledProcessError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to run email check: {e.stderr}"})
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