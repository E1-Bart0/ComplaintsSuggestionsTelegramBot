import os
from contextlib import contextmanager

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

dotenv.load_dotenv()


def get_url_to_db():
    db_name = os.getenv("DB_NAME", "bot_db")
    db_user = os.getenv("DB_USER", "librarian")
    db_password = os.getenv("DB_PASSWORD", "librarian_password")
    db_port = os.getenv("DB_PORT", "5432")
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_type = os.getenv("DB_TYPE", "postgresql")
    return f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


engine = create_engine(get_url_to_db())
Base = declarative_base()

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
