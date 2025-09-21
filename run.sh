#!/bin/bash

# Start the Reacher backend in the background.
# The `exec` command is not needed here as we want it to run in the background.
# The `find` command is used to locate the executable anywhere in the container
# and the `exec` option will run it.
find / -name 'reacherhq-backend' -exec {} \; &

# Wait for the backend to start and become available.
# This is a good practice to ensure the backend is listening before the proxy connects.
sleep 5

# Execute the Python proxy script in the foreground.
# This is the main process that will handle the Lambda function's lifecycle.
exec python3 /var/task/proxy.py