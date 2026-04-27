from pydantic import BaseModel

class AttendanceUpdate(BaseModel):
    user_id: int
    event_id: int
    is_present: bool

class AttendanceResponse(AttendanceUpdate):
    id: int
    class Config:
        from_attributes = True