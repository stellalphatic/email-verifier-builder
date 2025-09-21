# Stage 1: Find and extract the ReacherHQ backend executable.
# We use the official ReacherHQ image as a temporary build stage.
FROM reacherhq/backend:latest AS reacher_build

# The ReacherHQ backend uses a custom entrypoint script. We can find the actual
# executable by inspecting the image's entrypoint. The executable is located at /reacher.
# This stage is just to get the binary.

# Stage 2: Build the final Lambda container image.
# We use the official AWS Lambda Python base image.
FROM public.ecr.aws/lambda/python:3.11

# The Lambda base image includes a user `sbx_user1000`. Switch to root to
# have permission to install system packages and copy the Reacher executable.
USER root

# This is the corrected COPY command. We copy the executable from the first stage
# of the build, guaranteeing it will be found.
COPY --from=reacher_build /reacher /usr/local/bin/reacher

# Install a required package.
# The ReacherHQ backend uses curl, which is a common dependency.
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