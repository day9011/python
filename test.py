#!/usr/bin/env python2.7
#coding=utf-8

# def func1(func):
#     def func_re(text, s):
#         print "func1"
#         return "<func1>%s</func1>"%(text) + s
#     return func_re
#
# #####装饰器使得fun2 = func1(func2),现在func2等于func1的返回值,及func_re
#
# @func1
# def func2():
#     print "func2"
#
# print func2("test", "123")
import client
import time
import threading

total = 0
lock_total = False
running = 0
lock_run = False

class TestThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global total
        global lock_total
        global running
        global lock_run
        print total
        while lock_total:
            pass
        lock_total = True
        total += 1
        lock_total = False
        client.SendmsToServer()
        while lock_run:
            pass
        lock_run = True
        running -= 1
        lock_run = False


if __name__ == '__main__':
    starttime = time.time()
    threads = []
    while total < 2000:
        if running <= 4:
            t = TestThread()
            threads.append(t)
            t.start()
            while lock_run:
                pass
            lock_run = True
            running += 1
            lock_run = False
            # t.join()
        else:
            pass
    for item in threads:
        item.join()
    stoptime = time.time()
    print "%s sec"%(stoptime - starttime)