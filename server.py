#!/usr/bin/env python2.7
#coding=utf-
import socket
import threading
import select

class Server:
    def __init__(self, host='', port=8080, max_client=5):
        self._host = host
        self._port = port
        self._max_client = max_client
        self._confirmstr = "send message to mobile telephone by using day9011's function"

    def createServer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self._host, self._port))
        sock.listen(self._max_client)
        # inputs = [server]
        while True:
            # rs, ws, es = select.select(inputs, [], [], 20)
            # for r in rs:
            #     if r is server:
            conn, addr = sock.accept()
            print 'a connection from client', addr
            # inputs.append(conn)
                # else:
            data = conn.recv(100)
            print "data:", data
            if data == self._confirmstr:
                info = ""
                conn.sendall("ack-day9011")
                while True:
                    ret = conn.recv(10)
                    info += ret
                    #until finishing read data
                    if len(ret) < 10:
                        break
                print "info:", info
                conn.sendall("get info")
                while conn.recv(10) != "end info":
                    pass
                conn.sendall("finish")
            conn.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    server = Server(host,max_client=10)
    server.createServer()