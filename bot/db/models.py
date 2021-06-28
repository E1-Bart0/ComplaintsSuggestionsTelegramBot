from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from .core.connect_to_db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, index=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    username = Column(String(40), nullable=False)

    is_bot = Column(Boolean, default=False)
    is_super_user = Column(Boolean, default=False)

    # unique constraints across multiple columns and Indexing by name, year, author

    @hybrid_property
    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_super_user": self.is_super_user,
            "is_bot": self.is_bot,
        }
