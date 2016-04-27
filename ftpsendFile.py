#!/usr/bin/env python2.7
#coding = utf8
import os
import sys
# Import SOCKS module if it exists, else standard socket module socket
try:
    import SOCKS; socket = SOCKS; del SOCKS # import SOCKS as socket
    from socket import getfqdn; socket.getfqdn = getfqdn; del getfqdn
except ImportError:
    import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT

CRLF = '\r\n'

class ftp:
    def __init__(self, host='', user='', passwd=''):
        self.port = 21
        self.host = host
        self.user = user
        self.passwd = passwd
        self.sock = None
        self.CRLF = '\r\n'
        self.maxline = 100


    def login(self):
        resp = self.sendcmd('USER ' + self.user)
        resp = self.sendcmd('PASS ' + self.passwd)
        return resp

    def connect(self):
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=_GLOBAL_DEFAULT_TIMEOUT)
            self.af = self.sock.family
            self.file = self.sock.makefile('rb')
            print "connect successfully"
        except Exception, e:
            print str(e)

    def getline(self):
        line = self.file.readline(self.maxline + 1)
        if not line: raise EOFError
        if line[-2:] == self.CRLF: line = line[:-2]
        elif line[-1:] in self.CRLF: line = line[:-1]
        return line

    def getmultiline(self):
        line = self.getline()
        if line[3:4] == '-':
            code = line[:3]
            while 1:
                nextline = self.getline()
                line = line + ('\n' + nextline)
                if nextline[:3] == code and \
                                nextline[3:4] != '-':
                    break
        return line

    def sendcmd(self, command):
        command = command + self.CRLF
        self.sock.sendall(command)
        resp = self.getmultiline()
        print resp + "\n\n\n\n"
        return resp

    def dir(self, *args):
        cmd = 'LIST'
        func = None
        if args[-1:] and type(args[-1]) != type(''):
            args, func = args[:-1], args[-1]
        for arg in args:
            if arg:
                cmd = cmd + (' ' + arg)
        self.retrlines(cmd, func)

    def retrlines(self, cmd, callback = None):
        if callback is None: callback = print_line
        resp = self.sendcmd('TYPE A')
        conn = self.transfercmd(cmd)
        fp = conn.makefile('rb')
        try:
            while 1:
                line = fp.readline(self.maxline + 1)
                if len(line) > self.maxline:
                    raise Error("got more than %d bytes" % self.maxline)
                if self.debugging > 2: print '*retr*', repr(line)
                if not line:
                    break
                if line[-2:] == CRLF:
                    line = line[:-2]
                elif line[-1:] == '\n':
                    line = line[:-1]
                callback(line)
            # shutdown ssl layer
            if isinstance(conn, ssl.SSLSocket):
                conn.unwrap()
        finally:
            fp.close()
            conn.close()
        return self.voidresp()


# bashcommand = "ls /"
# print os.popen(bashcommand).read()
# print subprocess.Popen(bashcommand, stdout=subprocess.PIPE, shell=True).stdout.read()
test = ftp(host="home.ustc.edu.cn", user="sa615494", passwd="5673914")
test.connect()
test.login()
test.dir()