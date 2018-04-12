#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to make stickers for the (paper) database.'''

import sys,string,re,getopt
from sys import stdin
from sys import stdout
from string import strip

if len(sys.argv) == 1:
    print '''
Usage: makestickers.py [-t DELIMITER] [-f FIELDS] [-l LECTURER]
                       [-c COURSE] [-s SEMESTER] [-r RANGE]
       where: DELIMITER:   field delimiter for input lines
              FIELDS:      for id, name, first name, score (one based)
              LECTURER:    lecturer of course
              COURSE:      course
              SEMESTER:    semester
              RANGE:       two numbers, separated by commas, lower and upper
                           bound of the range of the scores

'''
    sys.exit(0)

optlist,args = getopt.getopt(sys.argv[1:],'t:f:l:c:s:r:')

# defaults:
delim = ':'
fieldsst = "1,2,3,4"   # this means matrikel, name, vorname, score
fields = [0,1,2,3]
vorlesung = "LA I"
dozent = "Hiß"
semester = "WS 03/04"
rangelow = 50
rangehigh = 100

for (k,v) in optlist:
    if   k == "-t": delim = v
    elif k == "-c": vorlesung = v
    elif k == "-l": dozent = v
    elif k == "-s": semester = v
    elif k == "-f":
        fieldsst = v
        l = string.split(fieldsst,",")
        fields = []
        for s in l:
            p = string.find(s,"-")
            if p == -1:
                fields.append(int(s)-1)
            else:
                for i in range(int(s[:p])-1,int(s[p+1:])): fields.append(i)
    elif k == "-r":
        p = string.find(v,",")
        if p == -1:
            sys.stderr.write("Range has no , !\n")
        else:
            rangelow = int(v[:p])
            rangehigh = int(v[p+1:])

leute = []

line = stdin.readline()
while line:
    line = string.strip(line)
    if len(line) > 0 and line[0] != '#':
        t = string.split(line,delim)
        person = [t[fields[0]],t[fields[1]],t[fields[2]],t[fields[3]]]
        leute.append(person)
    line = stdin.readline()

def byname(a,b):
    if a[1] < b[1]: return -1
    elif a[1] > b[1]: return 1
    else: return 0

leute.sort(byname)

print r"""\documentclass[german,11pt]{article}
\pagestyle{empty}
\parindent0pt
\usepackage{babel}
\usepackage{times}
\usepackage[latin1]{inputenc}

\newcommand{\person}[3]{%%
\begin{minipage}[t][36.9mm][t]{10cm}%%
\vspace*{1mm}%%
\hspace*{1cm}%%
\begin{minipage}[c]{8cm}%%
#1\hfill #2\par
%s (%s) \hspace*{1cm} #3\hfill %s\par
\end{minipage}%%
\hspace*{9mm}%%
\end{minipage}}

\voffset-1in
\hoffset-1in
\topmargin5mm
\headheight0pt
\headsep0pt
\topskip0pt
\oddsidemargin0pt
\evensidemargin0pt
\textheight304mm
\textwidth207mm
\footskip0pt
\parsep0pt

\begin{document}
""" % (vorlesung, dozent, semester)

even=0
for p in leute:
    stdout.write("\\person")
    stdout.write("{"+string.strip(p[1])+", "+string.strip(p[2])+\
                 "}{"+strip(p[0])+"}{")
    stdout.write("$"+str(rangelow)+" \\le "+str(p[3])+" \\le "+str(rangehigh))
    stdout.write("$}\n")
    if even: stdout.write("\n")
    even = 1-even
    
print r"\end{document}"

