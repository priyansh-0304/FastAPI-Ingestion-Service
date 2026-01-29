from pydantic import BaseModel

class CallPacket(BaseModel):
    sequence: int
    data: str
    timestamp: float