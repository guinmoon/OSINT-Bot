from sqlalchemy import create_engine
import psycopg2


def db_select_one(connection, query):
    sql = query
    try:
        result = connection.scalar(sql)
        return result
    except Exception as expt:
        print(expt)
        return expt


def db_select_many(connection, query):
    sql = query
    try:
        result = connection.execute(sql)
        return result
    except Exception as expt:
        print(expt)
        return expt


def db_import(connection, query):
    sql = query
    try:
        result = connection.execute(sql)
        return result
    except Exception as expt:
        print(expt)
        return expt


def db_import_many(connection, query, data):
    cur = connection.cursor()
    cur.executemany(query, [data])
    cur.execute('SELECT LASTVAL()')
    # fetching the value returned by ".....RETURNING ___"
    db_run_id = cur.fetchall()[0][0]
    connection.commit()
    if db_run_id:
        return db_run_id
