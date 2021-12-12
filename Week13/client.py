import datetime
import sys
from socket import *
from threading import Thread

self_port = 0
flag = 0
write_list = []

class Chatter:
    def __init__(self):
        pass

    def recv(name, conn):
        global flag,self_port
        while True:
            data = conn.recv(2048)
            if not data:
                break
            if flag == 0:
                if data.decode('utf-8')[0:12] == '#CLIENT_PORT':
                    self_port = data.decode('utf-8')[12:]
                    flag = 1
                    continue

            if data.decode('utf-8').upper() in ("BYE", "BYEBYE"):
                print("对方提议停止聊天，输入BYEBYE可终止...")
                break
            elif data.decode('utf-8').upper() == "CONNECTED_FAILED":
                print("管理员拒绝了你与服务器的连接,输入BYEBYE可终止...")
                break
            else:
                print("Server-%s-%s" % (str(name[0]), data.decode('utf-8')))

            time = datetime.datetime.now()
            time = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
            write_list.append(str(time) + data.decode('utf-8') + "\n")

    def send(conn):
        while True:
            msg = input()
            if not msg:
                continue
            write_list.append((datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + msg + '\n'))
            conn.send(msg.encode('utf-8'))
            if msg.upper() in ('BYEBYE', 'BYE'):
                break


if __name__ == '__main__':
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    server = socket(AF_INET, SOCK_STREAM)

    addr = (server_ip, server_port)
    conn = server
    server.connect(addr)
    tr = Thread(target=Chatter.recv, args=(addr, conn))
    tr.start()
    ts = Thread(target=Chatter.send, args=(conn,))
    ts.start()
    tr.join()
    ts.join()
    print("\n您已从服务器断开连接\n")
    conn.close()
    server.close()
    
    with open("../Week13/log/%s.txt"%str(self_port),'a+') as f:
        f.writelines(write_list)
