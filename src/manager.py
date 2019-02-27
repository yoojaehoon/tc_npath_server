from db.engine import Engine

class Manager(object):
    def __init__(self):
        self.engine = Engine()
        self.db_session = self.engine.getSession()
