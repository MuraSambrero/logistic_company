from db.db import DatabaseSessionManager


class Repository:
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session_manager = session_manager

    def get_session(self):
        return next(self.session_manager.yield_session())
    
    @property
    def session(self):
        return self.get_session()