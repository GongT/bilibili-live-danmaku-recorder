from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_connection(url: str):
    global engine
    if url.find('?') > 0:
        sep = '&'
    else:
        sep = '?'

    url = url + sep + "charset=utf8mb4"
    print(f"连接数据库：{url}")
    engine = create_engine(url, future=True, echo=False)
    engine.connect()
    print(f"  -- OK")
    return engine


def get_instance() -> Engine:
    return engine


from sqlalchemy import inspect, Table
from sqlalchemy.engine import Engine

TABLE_SEP = '_'


def create_table_if_not(engine: Engine, table: Table):
    if not inspect(engine).has_table(table.name):
        print(f"创建数据表：{table.name}")
        table.metadata.create_all(engine)
    else:
        print(f"使用数据表：{table.name}")


def table_name(room_id: int, kind: str):
    return str(room_id) + TABLE_SEP + kind
