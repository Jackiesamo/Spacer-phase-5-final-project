from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BookingCreate(BaseModel):
    space_id: UUID
    start_time: datetime
    end_time: datetime
