FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn boto3 python-jose[cryptography] python-multipart

EXPOSE 8004

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
