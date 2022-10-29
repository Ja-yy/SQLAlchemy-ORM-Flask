"""user's schema file database"""
from pydantic import BaseModel, Field,validator,EmailStr
from datetime import datetime
from app.constants.http_status_code import HTTP_400_BAD_REQUEST
from pydantic.schema import Optional

class UserBase(BaseModel):
    """User Base Schema"""

    username:Optional[str] 
    email: Optional[EmailStr]
    password: Optional[str]

    @validator('password')
    def validate_passwords(cls, v):
        return "Password too short" if  len(v)<6 else v
        # return v
    
    @validator('username')   
    def validate_username(cls,v): 
        return  "User name too short" if len(v)<4 else v
        # return v

    # @validator('username')
    # def username_alphanumeric(cls, v):
    #     return "must be alphanumeric" if  v.isalpha() else None
        # return v

    



class UserCreate(UserBase):
    """User Create Schema"""

    pass


class User(UserBase):
    """User Schema"""

    id: int = Field(default=None)

    class Config:
        """Config Class to update behaviour of pydantic"""

        orm_mode = True
