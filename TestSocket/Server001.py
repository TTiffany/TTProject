from socket import *

#ip地址, 0.0.0.0 指本机上所有可连接的地址
HOST = '0.0.0.0'
#端口号，一般为大于1024的端口，以防端口被占用
PORT = 23333
BUFSIZE = 1024
ADDR = (HOST, PORT)

#实例化类，AF_INET指IPv4协议，SOCK_STREAN指tcp协议
tcpSerSock = socket(AF_INET,SOCK_STREAM)

#绑定地址和端口
tcpSerSock.bind(ADDR)

#使socket处于监听状态，参数值允许等待连接的客户端的最大数量
tcpSerSock.listen(5)

print('等待连接客户端...')

#这里返回了一个新的socket: tcpCliSock用来和这个连接上来的客户端进行通信
tcpCliSock, addr = tcpSerSock.accept()

print('连接来自：', addr)

while True:

    #阻塞式等待接受消息，BUFSIZE指定了一次最多获取多少byte的消息，返回的也是byte类型
    data = tcpCliSock.recv(BUFSIZE)

    #对方关闭连接，返回空bytes,关闭连接
    if not data:
        tcpCliSock.close()
        break

    # 对方发送连接，接收到的是bytes类型，需要解码，默认是utf-8
    rstr = data.decode()

    print(rstr)  #返回对方发送过来的消息

    tcpCliSock.sendall(f'***{rstr}***'.encode())

tcpSerSock.close()
