from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


Base = declarative_base()


class DatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        """Initializing Database"""
        self._engine = create_engine('postgresql://admin:admin@postgres:5432/flask_app',future=True,echo=False)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False
        )()
        Base.metadata.create_all(self._engine)

db = DatabaseSession()


