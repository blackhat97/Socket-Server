import socket
import threading
import pymysql
from datetime import datetime

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print('Connected by',address)
            client.settimeout(10)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    '''
                    print(data)
                    serial_id = (data[1:16]).decode("utf-8")
                    sensor_type = (data[17:22]).decode("utf-8")
                    sensor_value = float((data[23:33]).decode("utf-8").strip())
                    state =  float((data[34:36]).decode("utf-8").strip())
                    print(serial_id)
                    print(sensor_type)
                    print(sensor_value)
                    print(state)
                    self.insertData(serial_id, sensor_type, sensor_value, state)
                    '''
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def insertData(self):
        #timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        #print(datetime.now().timestamp())

        timestamp = datetime.now().strftime('%s')

        conn = pymysql.connect(host='127.0.0.1', user='', password='', db='', charset='utf8')
        curs = conn.cursor()
        sql = "UPDATE current_sensor_data SET datetime = '%s'" %(timestamp)
        curs.execute(sql)
        conn.commit()
        conn.close()
        curs.close()

if __name__ == "__main__":
    ThreadedServer('0.0.0.0',5005).listen()
