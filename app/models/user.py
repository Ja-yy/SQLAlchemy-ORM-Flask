from datetime import datetime
from app.models.db_engine import Base
from app.models.base import *
from sqlalchemy.orm import relationship

#user model
class User(BaseModel,Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    username = Column(String(80),unique=True,nullable=True)
    email = Column(String(120),unique=True,nullable=True)
    password = Column(Text(),nullable=True)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,onupdate=datetime.now())
    bookmark = relationship('Bookmarks',backref='user')

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})({self.username})"

    @classmethod
    def filter(cls,is_first=False,**kwargs):

        try:
            filters=[]

            if kwargs.get("id"):
                filters.append(cls.id == kwargs["id"])

            if kwargs.get("username"):
                filters.append(cls.username == kwargs["username"])

            if kwargs.get("email"):
                filters.append(cls.email == kwargs["email"])

            query = select(cls).filter(*filters)
            instances = db.execute(query)
            if is_first:
                return instances.scalars().first()
            return instances.scalars().all()
            
        except Exception:
            return None