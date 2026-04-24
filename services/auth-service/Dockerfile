FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart email-validator bcrypt==4.0.1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]