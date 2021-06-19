from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Engine, Column, Integer, String
from mylib.cfg import TABLE_NAME_NORMAL


def create_table_danmaku(engine: Engine):
    Base = declarative_base()

    class FilePaths(Base):
        __tablename__ = TABLE_NAME_NORMAL
        __table_args__ = {'mysql_engine': 'InnoDB'}

        id = Column(Integer, primary_key=True, autoincrement=True)
        hash = Column(String(32), unique=True,index=tr)
        fullpath = Column(String(255))
        filename = Column(String(255))
        extension = Column(String(255))
        created = Column(String(255))
        modified = Column(String(255))
        size = Column(Integer)
        owner = Column(String(255))
        permissions = Column(Integer)

    FilePaths.metadata.create_all(engine)
