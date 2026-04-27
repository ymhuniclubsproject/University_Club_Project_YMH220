from pydantic import BaseModel

class MembershipBase(BaseModel):
    club_id: int

class MembershipCreate(MembershipBase):
    user_id: int

class MembershipUpdate(BaseModel):
    status: str

class MembershipResponse(BaseModel):
    id: int
    user_id: int
    club_id: int
    status: str

    class Config:
        from_attributes = True