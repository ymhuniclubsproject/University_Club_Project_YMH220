from pydantic import BaseModel

class MembershipBase(BaseModel): # Base schema for membership-related data | Üyelikle ilgili veriler için temel şema
    club_id: int

class MembershipCreate(MembershipBase): # Schema used for creating a new membership record | Yeni bir üyelik kaydı oluşturmak için kullanılan şema
    user_id: int

class MembershipUpdate(BaseModel): # Schema for updating the status of an existing membership | Mevcut bir üyeliğin durumunu güncellemek için kullanılan şema
    status: str

class MembershipResponse(BaseModel): # Schema for returning full membership details | Tam üyelik detaylarını döndürmek için kullanılan şema
    id: int
    user_id: int
    club_id: int
    status: str

    class Config:
        from_attributes = True # Allows compatibility with ORM objects | ORM nesneleriyle uyumluluğu sağlar