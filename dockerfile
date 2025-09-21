
FROM reacherhq/backend:latest

USER root

RUN apk add --no-cache python3 py3-pip

WORKDIR /var/task

COPY proxy.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

CMD ["proxy.lambda_handler"]