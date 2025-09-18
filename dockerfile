
FROM reacherhq/backend:latest

WORKDIR /app

COPY proxy.py .
COPY run.sh .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run.sh

CMD ["./run.sh"]