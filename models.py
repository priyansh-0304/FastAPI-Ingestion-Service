from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Call(Base):
    __tablename__ = "calls"

    call_id = Column(String, primary_key=True, index=True)
    state = Column(String, nullable=False, default="IN_PROGRESS")
    last_sequence = Column(Integer, nullable=False, default=0)

    transcription = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )