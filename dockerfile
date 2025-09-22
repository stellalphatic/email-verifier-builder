
FROM reacherhq/backend:latest

WORKDIR /var/task

COPY requirements.txt .
COPY proxy.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["proxy.lambda_handler"]