from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ticket Service", version="1.0.0")

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

@app.get("/")
def root():
    return {"message": "Ticket Service is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ticket-service"}

@app.post("/tickets", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        created_by=current_user
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@app.get("/tickets", response_model=list[schemas.TicketResponse])
def get_tickets(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    tickets = db.query(models.Ticket).all()
    return tickets

@app.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.patch("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(ticket_id: int, update: schemas.TicketUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if update.status:
        ticket.status = update.status
    if update.priority:
        ticket.priority = update.priority
    db.commit()
    db.refresh(ticket)
    return ticket