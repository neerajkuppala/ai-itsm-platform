from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "medium"

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_by: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None