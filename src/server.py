import socket
import pymysql
from datetime import datetime
import json
import sys


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5005  # initiate port no above 1024
    timeout = 30

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(100)
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, accept)


    try:
      while True:
        conn, address = server_socket.accept()  # accept new connection
        conn.settimeout(timeout)
        print("Connection from: " + str(address))
        while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
          try:
            json_bytes = conn.recv(1024).decode('utf8')
            data = json.loads(json_bytes)
            print(data)
        
            serial_code = data["serial_code"]
            sensor_type = data["sensor"][0]["type"]
            state = data["sensor"][0]["state"]
            value = data["sensor"][0]["value"]
            temp = data["sensor"][0]["temp"]
            print(serial_code)
            print(sensor_type)
            print(len(data["sensor"]))
            #updateTable(serial_code, sensor_type, state, value, temp)

          except socket.timeout:
            print('socket timeout')
          if not data:
            print('Connection lost. Listening for a new controller.')
            break

    except KeyboardInterrupt:
        conn.close()  # close the connection
        sys.exit()



def updateTable(serial_code, sensor_type, state, value, temp):
    timestamp = datetime.now().strftime('%s')
    conn = pymysql.connect(read_default_file='./mysql.cnf',)   
 
    try: 
        with conn.cursor() as curs:
            sql = "INSERT INTO realtime2 (serial_code, timestamp, type, state, value, temp) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE timestamp='%s', state='%s', value='%s', temp='%s'"
            #sql = "UPDATE realtime3 SET timestamp = %s, state = %s, value = %s, temp = %s WHERE serial_code = %s"
            curs.execute(sql, (serial_code, timestamp, sensor_type, state, value, temp, timestamp, state, value, temp))
        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    server_program()
