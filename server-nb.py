#!/usr/bin/env python2.7
#coding=utf-8
import socket
import threading
import select
import Queue

running_t = 0
num_t = 4
lock_run = False

class ServerTest(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    #overwrite the run function
    def run(self):
        global running_t
        global lock_run
        while lock_run:
            pass
        lock_run = True
        self.sendMs()
        running_t -= 1
        lock_run = False

    def sendMs(self):
        for item in self.data:
            if self.data[item] == Server.confirmstr:
                # print "confirm successfully"
                while Server.lock_dict:
                    pass
                Server.lock_dict = True
                Server.data_dict[item]["auth"] = True
                Server.lock_dict = False
                item.sendall("ack-day9011")
            elif Server.data_dict[item]["auth"] == False:
                # print "confirm failed"
                while Server.lock_dict:
                    pass
                Server.lock_dict = True
                Server.data_dict[item]["auth"] = "del"
                Server.lock_dict = False
                return
            elif self.data[item] == "end info":
                # print "end socket"
                message = Server.data_dict[item]["mes"]
                while Server.lock_dict:
                    pass
                Server.lock_dict = True
                Server.data_dict.pop(item)
                Server.lock_dict = False
                item.sendall("finish")
                item.close()
                print "message:", message
                # mes_arr = message.strip().split(' ')
                # param = ""
                # phonenumbers = []
                # i = 1
                # for item in mes_arr:
                #     if len(item) == 11 and item.isdigit():
                #         phonenumbers.append(item)
                #         i += 1
            else:
                if item not in Server.data_dict:
                    while Server.lock_dict:
                        pass
                    Server.lock_dict = True
                    Server.data_dict[item]["mes"] = self.data[item]
                    Server.lock_dict = False
                else:
                    while Server.lock_dict:
                        pass
                    Server.lock_dict = True
                    Server.data_dict[item]["mes"] += self.data[item]
                    Server.lock_dict = False
                item.sendall("get info")

class Server:
    confirmstr = "send message to mobile telephone by using day9011's function"
    data_dict = {}
    #A lock of global data dict
    lock_dict = False

    def __init__(self, host='', port=8080, max_client=5):
        self._host = host
        self._port = port
        self._max_client = max_client

    def createServer(self):
        global lock_run
        global num_t
        global running_t
        threads = []
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.listen(self._max_client)
        message_queue = Queue.Queue()
        inputs = [sock]
        count = 0
        while True:
            rs, ws, es = select.select(inputs, [], inputs, 20)
            for s in rs:
                if s is sock:
                    conn, addr = sock.accept()
                    count += 1
                    print 'a connection from client', addr, count
                    conn.setblocking(0)
                    inputs.append(conn)
                else:
                    mes = ""
                    data = ""
                    while True:
                        data = s.recv(1024)
                        mes += data
                        if len(data) < 1024:
                            break
                    if mes:
                        # print "mes:", mes
                        if s in Server.data_dict and Server.data_dict[s]["auth"] == "del":
                            print "delete element in inputs"
                            inputs.remove(s)
                            s.sendall("finish")
                            s.close()
                            Server.data_dict.pop(s)
                        else:
                            if mes == "end info":
                                inputs.remove(s)
                            if s not in Server.data_dict:
                                Server.data_dict[s] = {"mes": "", "auth": False}
                            message_queue.put({s: data})
            for s in es:
                print "exception condition on ", s.getpeername()
                inputs.remove(s)
                s.sendall("finish")
                s.close()
            #Get a data from message queue when poller finish job once until message queue is empty
            while not message_queue.empty():
                if running_t <= num_t:
                    while lock_run:
                        pass
                    lock_run = True
                    message = message_queue.get()
                    t = ServerTest(message)
                    threads.append(t)
                    t.start()
                    running_t += 1
                    lock_run = False
                else:
                    for t in threads:
                        t.join()
                        threads.remove(t)
                    break

if __name__ == "__main__":
    host = '127.0.0.1'
    server = Server(host,max_client=10)
    server.createServer()