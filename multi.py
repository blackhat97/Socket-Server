import selectors
import socket
from datetime import datetime
import json
import sys
import types
import pymysql
from DBUtils.PooledDB import PooledDB


sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, selectors.EVENT_READ, data=data)

def service_connection(key, mask):
    conn = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ:
        json_bytes = conn.recv(1024).decode()  # Should be ready to read
        if json_bytes:
            data = json.loads(json_bytes)

            if(bool(data["serial_code"])):
                print(data)
                for i in range(len(data["sensor"])):
                    if(data["sensor"][i]["type"] != 'NONE'):
                        items = data["sensor"][i]
                        pymysqlcon(i+1, data["serial_code"], items)


        else:
            print("closing connection to", data.addr)
            sel.unregister(conn)
            conn.close()


def pymysqlcon(num, serial_code, items):

    timestamp = datetime.now().strftime('%s')
    print("timestamp", timestamp)
    print("serial_code, number", serial_code, num)
    print(items)
    
    pool = PooledDB(creator = pymysql, read_default_file='./mysql.cnf')
    dbconn = pool.connection()
    try:
        with dbconn.cursor() as curs:
            sql = "SELECT id AS sid FROM appdb.sensor WHERE serial_code = %s AND num = %s;";
            curs.execute(sql, (serial_code, num))
            for sid in curs.fetchone():
              sensor_id = sid

        with dbconn.cursor() as curs:
            sql = "INSERT INTO appdb.realtime (sensor_id, timestamp, type, unit, state, value, temp) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE timestamp=VALUES(timestamp), state=VALUES(state), value=VALUES(value), temp=VALUES(temp);"
            curs.execute(sql, (sensor_id, timestamp, items["type"], items["unit"], items["state"], items["value"], items["temp"]))
  
        dbconn.commit()
    finally:
        curs.close()
        dbconn.close()

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5005  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2000)
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("closing connection to")
        sys.exit()
    finally:
        sel.close()


if __name__ == '__main__':
    server_program()
