
FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task

COPY requirements.txt .
COPY proxy.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["proxy.lambda_handler"]