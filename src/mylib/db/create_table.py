from sqlalchemy import inspect, Table
from sqlalchemy.engine import Engine


def create_table_if_not(engine: Engine, table: Table):
    if not inspect(engine).has_table(table.name):
        print(f"创建数据表：{table.name}")
        table.metadata.create_all(engine)
    else:
        print(f"使用数据表：{table.name}")
