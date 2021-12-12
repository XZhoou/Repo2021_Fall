import datetime
import os
import sys
from socket import *
from threading import Thread

BUFFERS = 1024
MAXC = 64

write_list = []

class Manager(Thread):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.server_ip, int(self.server_port)))
        self.server.listen(64)
        self.init_status_success()

        self.link_dict = {}

    def init_status_success(self):
        print("The server is started")

    def run(self):
        while True:
            conn, addr = self.server.accept()
            permission = input("一位新用户想要加入，是否同意？[Y/N]")
            if permission.upper() in ('Y', 'YES'):
                conn.send("管理员允许了你与服务器的连接".encode('utf-8'))
                client_ip, client_port = addr
                self.link_dict[str(client_port)] = conn
                client_thread = Thread(target=Manager.speak, args=(
                    self, "Client-" + client_ip + '-' + str(client_port), conn, client_port))
                self.refresh_port_list()
                client_thread.start()
            elif permission.upper() in ('N', 'NO'):
                conn.send("CONNECTED_FAILED".encode('utf-8'))
                continue
        self.server.close()

    def speak(self, name, conn, port):
        print("欢迎{}进入聊天室...".format(name))
        conn.send(("#CLIENT_PORT" + str(port)).encode('utf-8'))
        # with open("../Week13/log/Manager.txt","a+") as f:
        write_list.append(str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')) + "欢迎{}进入聊天室...\n".format(name))
        while True:
            try:
                msg = conn.recv(2048)
                if not msg:
                    break
                if msg.decode('utf-8').upper() in ("#FINDALL", "#ALL", "#ALL USERS"):
                    self.broadcast_to_active_user(port)
                elif msg.decode('utf-8')[0] == '@':
                    receiver = msg.decode('utf-8').split(' ')[0][1:]
                    self.post_to_specific_user(
                        receiver, (str(port) + ":" + msg.decode('utf-8')))
                    write_list.append(str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')) +"-"+ str(port) + ":" + msg.decode('utf-8') + "\n")

                else:
                    print("{}:{}".format(name, msg.decode('utf-8')))
                    self.broadcast(
                        port, (str(port) + ":" + msg.decode('utf-8')))
                    write_list.append(str(datetime.datetime.strftime(
                                datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')) +  ("-" + str(port) + ":" + msg.decode('utf-8') + "\n"))
                if msg.decode('utf-8').upper() in ('BYEBYE', 'BYE'):
                    print("{}离开了聊天室...".format(name))
                    write_list.append((str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')) + "{}离开了聊天室...\n".format(name)))
                    del self.link_dict[str(port)]
                    self.refresh_port_list()
                    break

            except Exception as e:
                print("server error %s" % e)
                break
        conn.close()

    def refresh_port_list(self):
        message = "当前在线用户发生变化,刷新用户列表,目前在线的用户为:\n"
        # print(message,end = '')
        # port_list = list(self.link_dict.keys())
        # print(*port_list, sep='\n')

        for i in list(self.link_dict.keys()):
            message += "%s\n" % i
        for port, conn in self.link_dict.items():
            conn.send(message.encode('utf-8'))
        self.write_in()

    def post_to_specific_user(self, receiver, message):
        self.link_dict[str(receiver)].send(message.encode('utf-8'))

    def broadcast(self, sender, message):
        for port, conn in self.link_dict.items():
            if str(port) == str(sender):
                pass
            else:
                conn.send(message.encode('utf-8'))

    def broadcast_to_active_user(self, sender):
        message = "目前在线的用户有：\n"
        for i in list(self.link_dict.keys()):
            message += "%s\n" % i
        for port, conn in self.link_dict.items():
            if str(port) == str(sender):
                conn.send(message.encode('utf-8'))
                break
            else:
                pass


    def write_in(self):
        global write_list
        with open("../Week13/log/Manager.txt","a+") as f:
            f.writelines(write_list)
            write_list = []

if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]

    server = Manager(ip, port)
    server.start()
    # status = True
    # try:
    #     while status:
    #         status = input()
    #         # print(status)
    #         if status.upper() not in ("EXIT","LEAVE","SHUTDOWN"):
    #             continue
    #         else:
    #             os._exit(0)
    # except Exception as e:
    #     pass
    # ip = sys.argv[1]
    # port = sys.argv[2]

    # server = socket(AF_INET, SOCK_STREAM)
    # server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # server.bind((ip, int(port)))

    # server.listen(MAXC)

    # while True:
    #     conn, addr = server.accept()
    #     client_ip, client_port = addr
    #     client_thread = Thread(target=speak, args=(
    #         "Client-" + client_ip + '-' + str(client_port), conn))

    #     client_thread.start()
    # server.close()
