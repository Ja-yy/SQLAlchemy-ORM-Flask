from sqlalchemy import (
    Table,
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    func,
    select,
    Text
)
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete

from app.models.db_engine import db


class BaseModel:
    """Basic model class."""

    def __repr__(self):
        return f"{self}"

    def save(self):
        """Save given instance"""
        db.add(self)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        return self

    @classmethod
    def create(cls, **kwargs):
        """Create record."""
        instance = cls(**kwargs)
        db.add(instance)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        return instance

    @classmethod
    def update(cls, uid, **kwargs):
        """Update record."""
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == uid)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        db.execute(query)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        return cls.get(uid)

    @classmethod
    def get(cls, uid):
        """Fetch record."""
        query = select(cls).where(cls.id == uid)
        instances = db.execute(query)
        try:
            (instance,) = instances.first()
        except Exception:
            return None
        return instance

    @classmethod
    def get_all(cls):
        """Fetch all records."""
        query = select(cls)
        instances = db.execute(query)
        instances = instances.scalars().all()
        return instances

    @classmethod
    def delete(cls, uid):
        """Delete record."""
        query = sqlalchemy_delete(cls).where(cls.id == uid)
        db.execute(query)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        return True

    @classmethod
    def count(cls, **kwargs):
        """Count records."""
        query = select(func.count(cls.id))
        instance_count = db.execute(query)
        return instance_count.scalar_one()
