#!/usr/bin/env python2.7
import socket
import sys

def SendmsToServer():
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect(('127.0.0.1',8080))
    confirmstr = "send message to mobile telephone by using day9011's function"
    clientsock.send(confirmstr)
    res = ""
    while res != "ack-day9011":
        res = clientsock.recv(1024)
        if res == "finish":
            clientsock.close()
            exit()
    print res
    info = "18674802640"
    # for item in sys.argv[1:]:
    #     info += item + " "
    # print testarr
    clientsock.sendall(info)
    print "send info successfully"
    res = ""
    while res != "get info":
        res = clientsock.recv(10)
        if res == "finish":
            clientsock.close()
            exit()
    print res
    clientsock.sendall("end info")
    while clientsock.recv(10) != "finish":
        pass
    # data = clientsock.recv(1024)
    # print data
    clientsock.close()

if __name__ == '__main__':
    SendmsToServer()
