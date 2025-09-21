# Use the official AWS Lambda Python base image.
FROM public.ecr.aws/lambda/python:3.11

# The Lambda base image includes a user `sbx_user1000`. Switch to root to
# have permission to install system packages and copy the Reacher executable.
USER root

# This is the corrected COPY command. The executable is simply named `reacher`
# and is located in the root of the source image.
COPY --from=reacherhq/backend:latest /reacher /usr/local/bin/reacher

# Install a required package.
# The ReacherHQ backend uses curl, which is a common dependency.
# This ensures it's available for the backend process.
RUN yum install -y curl

# Switch back to the non-privileged user for security best practice.
USER sbx_user1000

# Set the working directory for your application code
WORKDIR /var/task

# Copy your proxy and requirements files
COPY requirements.txt .
COPY proxy.py .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# This sets your Lambda handler as the entrypoint.
CMD ["proxy.lambda_handler"]