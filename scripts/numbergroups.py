#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2003 by  Frank Lübeck  and   Max Neunhöffer
#
#   $Id: numbergroups.py,v 1.3 2004/05/02 12:29:10 neunhoef Exp $
#
# This script is part of OKUSON.
#
# It takes the output of distribute.py, possibly edited by the user,
# collects people from each group and produces output suitable for
# the file data/groups.txt, where only the id and a group number are
# stored. Groups are numbered from 1 on.
#
# Input is an ASCII file with one line for each person in the format:
#  id:last name:first name:semester:studiengang:wishlist:pdata1-9
# where wishlist is a list of id's of people, separated by commas,
# and pdata1-9 are the 9 personal data fields, separated by :
# characters.
# Such a file is produced by distribute.py.
# Empty lines indicate the separation of groups.
# Lines beginning with a "#" sign are ignored as comments.
# 
# Command line arguments are as follows:
#  inputfile outputfile [firstgroupnumber]

import sys,os,string

if len(sys.argv) < 3:
    print """
Usage: numbergroups.py INPUTFILE OUTPUTFILE [FIRSTGROUPNUMBER]
       where FIRSTGROUPNUMBER is the number of the first group, which
       defaults to 1.
       Groups in the input are separated by empty lines.
       Format of input file:
         id:last name:first name:semester:studiengang:wishlist:pdata1-9
       where wishlist is a comma separated list of ids.
"""
    sys.exit(0)

# The following function basically does all the work for one part:

def HandleOnePart(input,output,nr):
    '''Reads in one group of the input (until the first empty line or end
of file is found) and writes out the ids, one per line with the group
number.'''
    while 1:
        line = input.readline()
        if not(line):
            return 2   # end of file, group is over
            break
        line = line.strip()
        if not(line):
            return 1   # empty line, group is over
            break
        if line[0] == '#':   # a comment, we ignore line
            continue
        p = line.split(':')
        if len(p) < 7:
            print "Illegal format, offending line:\n  "+line+"\nignoring..."
            continue
        output.write(p[0]+':'+str(nr)+'\n')

input = file(sys.argv[1],"r")
output = file(sys.argv[2],"w")
firstgroup = 1
if len(sys.argv) > 3:
    firstgroup = int(sys.argv[3])

groupnr = firstgroup
while HandleOnePart(input,output,groupnr) < 2:
    groupnr += 1

