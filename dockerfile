FROM reacherhq/backend:latest

USER root

RUN apk add --no-cache python3 py3-pip

WORKDIR /var/task

COPY proxy.py .
COPY run.sh .

COPY requirements.txt .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

RUN chmod +x run.sh

CMD ["./run.sh"]