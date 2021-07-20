from mylib.constants import DB_COL_EX_FIELD, DB_COL_HASH, DB_COL_PK, DB_COL_TIME

def is_special_key(k: str):
    return k == DB_COL_PK or k == DB_COL_HASH or k == DB_COL_EX_FIELD or k == DB_COL_TIME
