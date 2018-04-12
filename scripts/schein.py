#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to make the Scheins.'''

import string,sys,getopt

if len(sys.argv) == 1:
    print """
Usage: schein.py [-t DELIMITER] [-f FIELDS] [-l LECTURER]
                 [-c COURSE] [-s SEMESTER] [-d DATE] [-b BANNER]
DELIMITER:  field delimiter for input lines
FIELDS:     three field numbers in input lines for id, name, first name, resp.
            separated by commas, field numbers are starting with 1, that is
            the first field in the line has number 1.
"""
    sys.exit(0)

optlist,args = getopt.getopt(sys.argv[1:],'t:f:c:l:s:b:d:')

# defaults:
delim = ':'
fieldsst = "1,2,3"   # this means matrikel, name, vorname
fields = [0,1,2]
vorlesung = "Lineare Algebra I"
dozent = "Prof.~Dr.~Gerhard Hiß"
semester = "Wintersemester 2001/2002"
datum = "\\today"
banner = ""

for (k,v) in optlist:
    if   k == "-t": delim = v
    elif k == "-c": vorlesung = v
    elif k == "-l": dozent = v
    elif k == "-s": semester = v
    elif k == "-b": banner = v
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
    elif k == "-d": datum = v


print r"""\documentclass[12pt,german]{article}

\pagestyle{empty}
\parindent0pt

\usepackage{babel}
\usepackage[latin1]{inputenc}
\usepackage[a4paper,width=6in,top=0mm,bottom=0mm,noheadfoot]{geometry}
\usepackage{times}

\newcommand{\schein}[6]{%
\begin{minipage}[t][146mm][t]{6in}
\vspace*{2cm}
\textbf{\large\sffamily Lehrstuhl D für Mathematik \hfill RWTH Aachen}

\vspace*{1cm}
\begin{flushright}
Aachen, den #1
\end{flushright}

\vspace*{5mm}

\begin{center}
\Large\sffamily Bescheinigung
\end{center}

\vspace*{1cm}
\textbf{#2}, Matrikelnummer #3, hat im 
#4 erfolgreich an den Übungen zur
Vorlesung \textbf{#5} teilgenommen.

\vspace*{2.5cm}
\hspace*{10cm} (#6)

\vfill
\hspace*{-1in}\rule{4mm}{0.1mm}\hspace*{1in}
\end{minipage}\par}

\begin{document}"""

if banner != "":
    print "\\vspace*{\\fill}\\par\\begin{center}\\Huge\n"+ \
    banner+"\n\\par\\end{center}\\vspace*{\\fill}\\pagebreak\n"
    
linelist = sys.stdin.readlines()
nr = len(linelist)
if nr % 2 == 1:
    linelist.append("\n")
    nr += 1
offset = nr / 2
linelist2 = []
for i in xrange(offset):
    linelist2.append(linelist[i])
    linelist2.append(linelist[i+offset])

for line in linelist2:
    line = string.strip(line)
    if not(line): continue
    l = string.split(line,delim)
    print r"\schein{%s}{%s}{%s}{%s}{%s}{%s}" % \
          (datum,l[fields[2]]+" "+l[fields[1]],l[fields[0]],semester,
           vorlesung,dozent)

print """\end{document}
"""
