import pymysql
from DBUtils.PooledDB import PooledDB


pool = PooledDB(creator = pymysql, read_default_file='./mysql.cnf')
dbconn = pool.connection()


try:
    with dbconn.cursor() as curs:
        sql = "INSERT INTO appdb.realtime2 (serial_code) VALUES (%s)"
        curs.execute(sql, ('dire'))
    dbconn.commit()
finally:
    dbconn.close()


