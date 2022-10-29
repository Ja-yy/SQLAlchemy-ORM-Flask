"""Bookmarks's schema file database"""
from email.policy import default
from pydantic import BaseModel, Field,HttpUrl


class BookmarkBase(BaseModel):
    """Bookmark Base Schema"""

    body: str = Field(example="body")
    url: HttpUrl = Field(example="www.google.com")
    short_url: str = Field(default=None)
    visits: int = Field(default=None, example="1")
    


class BookmarkCreate(BookmarkBase):
    """Bookmark Create Schema"""

    user_id:int = Field(default=None)
    pass


class Bookmark(BookmarkBase):
    """Bookmark Schema"""

    id: int = Field(default=None)
    
    class Config:
        """Config Class to update behaviour of pydantic"""

        orm_mode = True
