from sqlalchemy.sql import expression
from mylib.db.create_table import create_table_if_not
from config.config import SQL_CONNECTION
from ..cfg import TABLE_NAME_RECORD
from sqlalchemy import create_engine, Column, Integer, String, JSON, MetaData, Table, Boolean, Index

if SQL_CONNECTION.find('?') > 0:
    sep = '&'
else:
    sep = '?'

url = SQL_CONNECTION + sep + "charset=utf8mb4"
print(f"连接数据库：{url}")
engine = create_engine(url, future=True, echo=True)
connection = engine.connect()
print(f"  -- OK")

metadata = MetaData()
record_table = Table(TABLE_NAME_RECORD, metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('consumed', Boolean, default=False, nullable=False),
                     Column('hash', String(32), index=True, default="", nullable=False),
                     Column('raw_data', JSON, nullable=False), Column('type', Integer, nullable=False))

Index('my_index', record_table.c.hash, mysql_using='hash', mariadb_using='hash')

create_table_if_not(engine, record_table)
