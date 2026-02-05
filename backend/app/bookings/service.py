from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta

from app.database.models import Booking, Space

def create_booking(db: Session, user, data):
    space = db.query(Space).filter(Space.id == data.space_id).first()

    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space not found"
        )

    if space.status != "AVAILABLE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Space is not available"
        )