from datetime import datetime
import  random
from app.models.db_engine import Base
import string
from app.models.base import *

#bookmark model
class Bookmarks(BaseModel,Base):
    __tablename__='bookmarks'
    id = Column(Integer,primary_key=True)
    body = Column(Text,nullable=True)
    url = Column(Text,nullable=True)
    short_url = Column(String(3),nullable=True)
    visits = Column(Integer,default=0)
    user_id=Column(Integer,ForeignKey('user.id'))
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,onupdate=datetime.now())

    def generate_short_characters(self):
        characters=string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(characters,k=3))

        link=self.filter(short_url=picked_chars,is_first=True)

        if link:
            self.generate_short_characters()

        else:
            return picked_chars

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.short_url=self.generate_short_characters()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})({self.short_url})"

    @classmethod
    def add_visit_count(cls,bookmark):
        bookmark.visits = bookmark.visits + 1
        db.commit()

    @classmethod
    def filter(cls,is_first=False,**kwargs):

        try:
            filters=[]

            if kwargs.get("id"):
                filters.append(cls.id == kwargs["id"])

            if kwargs.get("url"):
                filters.append(cls.url == kwargs["url"])

            if kwargs.get("short_url"):
                filters.append(cls.short_url == kwargs["short_url"])

            if kwargs.get("user_id"):
                filters.append(cls.user_id == kwargs["user_id"])

            query = select(cls).filter(*filters)
            instances = db.execute(query)
            if is_first:
                return instances.scalars().first()
            return instances.scalars().all()

        except Exception:
            return None

