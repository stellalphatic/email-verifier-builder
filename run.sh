#!/bin/bash

# Start the Reacher backend in the background
/usr/local/bin/reacherhq-backend &

# Execute the Python proxy script in the foreground
exec python3 proxy.py