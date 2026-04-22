from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from passlib.context import CryptContext
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

@app.get("/")
def root():
    return {"message": "Auth Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth-service"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"users": users}

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user