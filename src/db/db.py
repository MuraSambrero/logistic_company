from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DatabaseSessionManager:

    def __init__(self, dsn_string: str):
        self.dsn_string = dsn_string
        self.engine = create_engine(self.dsn_string, echo=True)
        self.Sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def yield_session(self) -> Generator[Session, Any, None]:
        db = self.Sessionmaker()
        try:
            yield db
        finally:
            db.close()
