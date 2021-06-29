from typing import Optional

from .core.connect_to_db import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=True)
    username = Column(String(40), nullable=True)

    is_bot = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # unique constraints across multiple columns and Indexing by name, year, author

    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        is_superuser: Optional[bool] = False,
        is_admin: Optional[bool] = False,
        is_bot: Optional[bool] = False,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_superuser = is_superuser
        self.is_admin = is_admin
        self.is_bot = is_bot

    @hybrid_property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @hybrid_property
    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_superuser": self.is_superuser,
            "is_bot": self.is_bot,
        }

    def to_dict(self) -> dict:
        return self.as_dict

    def __repr__(self):
        return str(self.as_dict)


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    superuser_password = Column(String(60), nullable=False)
