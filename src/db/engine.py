from tc_npath_monitor.src.lib import config
from tc_npath_monitor.src.db import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class Engine():
    def __init__(self):
        db_conf = config.getDBConf()
        self.engine = create_engine('sqlite:///%s' %db_conf['path'], echo=False, connect_args={'check_same_thread':False}, poolclass=StaticPool)

    def initDB(self):
        models.Base.metadata.create_all(self.engine)

    def getModel(self, name):
        return getattr(models, name)

    def getSession(self):
        return sessionmaker(bind=self.engine)()

if __name__ == '__main__':
    engine = Engine()
    engine.initDB()
