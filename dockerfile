FROM reacherhq/backend:latest

USER root

RUN apk add --no-cache python3 py3-pip

WORKDIR /var/task

COPY proxy.py .
COPY requirements.txt .

RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

CMD python3 proxy.py