from typing import Optional
from pydantic import BaseModel


class RoomSummary(BaseModel):
    room_id: int
    room: str
    next_class: Optional[str]
    subject: Optional[str]


class Session(BaseModel):
    time_start_str: str
    room_id: int
    room: str
    subject: str
    time_start_int: int
    time_end_int: int
