from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import boto3
import json

app = FastAPI(title="AI Service", version="1.0.0")

SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class TicketAnalysisRequest(BaseModel):
    title: str
    description: str

class TicketAnalysisResponse(BaseModel):
    ticket_type: str
    severity: str
    suggested_fix: str
    summary: str

def analyze_with_bedrock(title: str, description: str) -> dict:
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        prompt = f"""You are an IT support specialist. Analyze this IT ticket and respond in JSON format only.

Ticket Title: {title}
Ticket Description: {description}

Respond with exactly this JSON structure:
{{
    "ticket_type": "hardware/software/network/access/other",
    "severity": "low/medium/high/critical",
    "suggested_fix": "step by step fix suggestion",
    "summary": "one line summary of the issue"
}}"""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        })

        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body
        )

        response_body = json.loads(response["body"].read())
        text = response_body["content"][0]["text"]
        return json.loads(text)

    except Exception as e:
        return {
            "ticket_type": "unknown",
            "severity": "medium",
            "suggested_fix": f"AI analysis unavailable: {str(e)}",
            "summary": "Manual review required"
        }

@app.get("/")
def root():
    return {"message": "AI Service is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-service"}

@app.post("/analyze", response_model=TicketAnalysisResponse)
def analyze_ticket(request: TicketAnalysisRequest, current_user: str = Depends(get_current_user)):
    result = analyze_with_bedrock(request.title, request.description)
    return TicketAnalysisResponse(**result)