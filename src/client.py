import socket
import time


def client_program():
    host = 'iot.dymeter.com'  # as both code is running on same pc
    port = 5005  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = 'I am a client'
    while message.lower().strip() != 'bye':
        print('연결 확인 됐습니다.')
        client_socket.send(message.encode('utf-8'))  # send message
        print('메시지를 전송했습니다.')
        time.sleep(5)


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
