import pymysql


def db_select_one(connection,query):
    cursor = connection.cursor()
    sql = query
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        connection.commit()
        return result
    except Exception as expt:
        connection.rollback()
        print(expt)
        return expt

def db_select_many(connection,query):
    cursor = connection.cursor()
    sql = query
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Exception as expt:
        connection.rollback()
        print(expt)
        return expt

def db_import(connection,query):
    cursor = connection.cursor()
    sql = query
    try:
        cursor.execute(sql)
        connection.commit()
        return True
    except Exception as expt:
        connection.rollback()
        print(expt)
        return expt

def db_import_many(connection,query,data):
    cursor = connection.cursor()
    sql = query
    try:
        cursor.executemany(sql,data)
        connection.commit()
        return True
    except Exception as expt:
        connection.rollback()
        print(query)
        msg ="%s"%(expt)
        print(msg)
        return expt