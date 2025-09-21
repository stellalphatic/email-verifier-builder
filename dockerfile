
FROM public.ecr.aws/lambda/python:3.11

USER root

COPY --from=reacherhq/backend:latest /reacher /usr/local/bin/reacher

# Switch back to the non-privileged user for security best practice.
USER sbx_user1000

# Set the working directory for your application code
WORKDIR /var/task

# Copy your proxy and requirements files
COPY requirements.txt .
COPY proxy.py .

# Install Python dependencies. This will now work without the error because
# we are using an AWS Lambda-optimized base image.
RUN pip install --no-cache-dir -r requirements.txt

# This sets your Lambda handler as the entrypoint. The Lambda runtime
# will automatically call this handler.
# The handler is located in the `proxy.py` file, with the function `lambda_handler`.
CMD ["proxy.lambda_handler"]