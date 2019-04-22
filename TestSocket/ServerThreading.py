import threading,socket

#ip地址, 0.0.0.0 指本机上所有可连接的地址
HOST = '0.0.0.0'
#端口号，一般为大于1024的端口，以防端口被占用
PORT = 23333
BUFSIZE = 1024
ADDR = (HOST, PORT)

def on_new_client(clinetsocket,addr):
    while True:
        data = clinetsocket.recv(BUFSIZE)

        if not data:
            print('%s 关闭了连接'%addr )
            break

        rstr = data.decode()

        print('%s : %s' %(addr,rstr))
        clinetsocket.send(data)

    clinetsocket.close()

serversocket = socket.socket()

#绑定地址和端口
serversocket.bind(ADDR)

#使socket处于监听状态，参数值允许等待连接的客户端的最大数量
serversocket.listen(5)

while True:
    clinetsocket, addr = serversocket.accept()
    addr = str(addr)
    print('来自%s的连接' % addr)
    th = threading.Thread(target=on_new_client, args=(clinetsocket,addr)) #使用多线程
    th.start()
