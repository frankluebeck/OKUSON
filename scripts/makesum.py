#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is a rather simple script which adds two numbers on each input line.
Probably nobody will ever use this again!'''

import sys,string

lines = sys.stdin.readlines()
for l in lines:
    t = l.split(":")
    if len(t) == 4:
        tt = t[3].split(";")
        p = int(tt[0])+int(tt[2])
        t[3] = str(p)
        sys.stdout.write(string.join(t,":")+"\n")
