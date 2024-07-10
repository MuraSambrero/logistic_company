from db.db import DatabaseSessionManager
from db.models import Base


class Repository:
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session_manager = session_manager

    def get_session(self):
        return next(self.session_manager.yield_session())
    
    @property
    def get_new_session(self):
        return self.get_session()
    
    def create_tables(self):
        Base.metadata.create_all(self.session_manager.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.session_manager.engine)

