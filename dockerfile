# Stage 1: The official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Switch to the root user for installation and copying.
USER root

# This is the crucial step. We mount the entire ReacherHQ image
# and copy its entire filesystem into our build.
COPY --from=reacherhq/backend:latest / /

# Install the `yum` package manager as a dependency.
RUN yum install -y yum

# Now we install curl, which the ReacherHQ backend depends on.
RUN yum install -y curl

# Set the working directory for your application code.
WORKDIR /var/task

# Copy your Python files into the container.
COPY requirements.txt .
COPY proxy.py .

# Install Python dependencies as root. This avoids the "user not found" error.
RUN pip install --no-cache-dir -r requirements.txt

# Now, we switch to the non-privileged user. It's a security best practice to
# run the final application as a non-root user.
USER sbx_user1000

# The Lambda handler is set as the entrypoint.
CMD ["proxy.lambda_handler"]