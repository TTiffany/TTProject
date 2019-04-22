from socket import *

#ip地址, 0.0.0.0 指本机上所有可连接的地址
HOST = '127.0.0.1'
#端口号，一般为大于1024的端口，以防端口被占用
PORT = 23333
BUFSIZE = 1024
ADDR = (HOST, PORT)

#创建socket，指明协议
tcpCliSock = socket(AF_INET,SOCK_STREAM)

#连接远程地址和端口，发送syn,等待syn ack，阻塞式的
tcpCliSock.connect(ADDR)

while True:
    data = input('>> ')

    if not data:
        break
    tcpCliSock.send(data.encode())

    data = tcpCliSock.recv(BUFSIZE)

    print(data.decode())

tcpCliSock.close()