#!/usr/bin/env python

import socket,threading

def handler(t,a):
    r = t.makefile("r")
    w = t.makefile("w")
    l = r.readline()
    try:
        w.write("Hi there!\n"*10000)
    except:
        pass
    t.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1',8000))
s.listen(5)

while 1:
    (t,a) = s.accept()
    th = threading.Thread(target=handler,args=(t,a))
    try:
        th.start()
    except:
        pass
    print threading.activeCount()


