#!/usr/bin/env python2

import socket

def f():
    for i in range(10000):
        s = socket.socket()
        s.connect(('127.0.0.1',8000))
        s.send("Hi\n")
        a = s.recv(100)
        s.close()
        print i

