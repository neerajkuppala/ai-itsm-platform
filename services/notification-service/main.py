from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import boto3
import json
from datetime import datetime

app = FastAPI(title="Notification Service", version="1.0.0")

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

class NotificationRequest(BaseModel):
    ticket_id: int
    ticket_title: str
    status: str
    user_email: str
    message: str

def send_to_sqs(notification_data: dict):
    try:
        sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = sqs.create_queue(
            QueueName="itsm-notifications",
            Attributes={"DelaySeconds": "0"}
        )["QueueUrl"]
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(notification_data)
        )
        return {"status": "sent", "queue": "itsm-notifications"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/")
def root():
    return {"message": "Notification Service is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "notification-service"}

@app.post("/notify")
def send_notification(
    request: NotificationRequest,
    current_user: str = Depends(get_current_user)
):
    notification_data = {
        "ticket_id": request.ticket_id,
        "ticket_title": request.ticket_title,
        "status": request.status,
        "user_email": request.user_email,
        "message": request.message,
        "sent_at": datetime.utcnow().isoformat(),
        "sent_by": current_user
    }
    result = send_to_sqs(notification_data)
    return {
        "notification": notification_data,
        "delivery": result
    }

@app.get("/queue/status")
def queue_status(current_user: str = Depends(get_current_user)):
    try:
        sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = sqs.get_queue_url(QueueName="itsm-notifications")["QueueUrl"]
        attrs = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=["ApproximateNumberOfMessages"]
        )
        count = attrs["Attributes"]["ApproximateNumberOfMessages"]
        return {"queue": "itsm-notifications", "messages_waiting": count}
    except Exception as e:
        return {"error": str(e)}