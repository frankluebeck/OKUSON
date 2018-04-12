#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2007 by  Frank Lübeck
#
# This script is part of OKUSON.
# It can be used to create the input of the exam results file
#     data/exams.txt
# with some error checking to minimize problems.

import sys,os,string,readline

if len(sys.argv) != 6 and len(sys.argv) != 7:
    print """
Usage: getexamresults.py peoplefile nrsep examnr maxpoints resultfile [sep]
       where:
       peoplefile    - file with lines starting 'id:lastname:firstname[:]'
                       specifying the participants of the exam 
                       (lines starting with '#' are ignored)
       nrsep         - number of exercises with separated points
       examnr        - exam number
       maxpoints     - maximal number of points in this exam
       resultfile    - name of result file; this has a format such that 
                       it can be concatenated to your okuson/data/exams.txt
                       file; afterwards the server needs a restart
                       (new lines are appended to that file)
       sep           - optional: separator character for input of separated 
                       points (note that '.' is needed if you want to enter 
                       decimal numbers)

Points can be given as integers or floating point numbers (with '.' as
decimal point). Also '-' is allowed, it counts as zero points and means
that no solution was delivered.
"""
    sys.exit(1)

##########################################################################
# read and check arguments
try: 
  sepnr = int(sys.argv[2])
except:
  sys.stdout.write('Second argument must be number of exercises, not '+\
                   sys.argv[2]+'\n')
  sys.exit(2)

try: 
  examnr = int(sys.argv[3])
except:
  sys.stdout.write('Third argument must be exam number, not '+\
                   sys.argv[3]+'\n')
  sys.exit(3)
examnr = sys.argv[3]

try: 
  maxstr = sys.argv[4]
  max = float(maxstr)
except:
  sys.stdout.write('Fourth argument must maximal number of points, not '+\
                   sys.argv[4]+'\n')
  sys.exit(4)

try:
  resfile = sys.argv[5]
  f = open(resfile, "a")
  f.close()
except:
  sys.stdout.write('Cannot open file for writing: '+sys.argv[5]+'\n')
  sys.exit(5)

if len(sys.argv) == 7:
  sep = sys.argv[6]
  if not len(sep) == 1:
    sys.stdout.write('Separator must be a single character, not "'+sep+'"\n')
    sys.exit(6)
  if sep != ',':
    sys.stdout.write('Input for separated points uses separator "'+sep+'"\n')
    sys.stdout.write('But results file will use "," as separator.\n')
else:
  sep = ','

#############################################################################
# read dictionary of known participants from file sys.argv[1]
known = {}
try:
  f = open(sys.argv[1], "r")
except:
  print 'Cannot open file "'+sys.argv[1]+'" for list of participants' 
  f.close()
  exit(1)
l = f.readline()
while l:
  if l[0] != '#':
    l = l.split(':')
    known[l[0]] = string.join([l[2], l[1]])
  l = f.readline()
f.close()

#############################################################################
# the main function to get an entry
def getentry(count):
  sys.stdout.write('-----------\nNew entry number '+str(count)+\
                   ' ("quit" if done).\n')
  # first get id until in known and print name
  l = None
  while not known.has_key(l):
    sys.stdout.write('Id: ')
    l = sys.stdin.readline()
    l = string.join(string.split(l))
    if l == 'quit':
      sys.stdout.write('-------------\nGot '+str(count-1)+' entries. Bye.\n\n')
      exit(0)
  id = l
  sys.stdout.write('Name: '+known[l]+'\n')
  # get points per exercise
  ok = 0
  while not ok:
    ok = 1
    sys.stdout.write('separate points (separator: "'+sep+'"): ')
    l = sys.stdin.readline()
    l = string.strip(l)
    l = string.split(l, sep)
    sum = 0
    if len(l) != sepnr:
      sys.stdout.write('Wrong number of entries, should be '+str(sepnr)+'\n')
      ok = 0
      #continue;
    for a in l:
      a = string.strip(a)
      if a == '-':
        pass
      elif a.find('.') == -1:
        try:
          sum += int(a)
        except:
          sys.stdout.write('Not a number: '+a+'\n')
          ok = 0
      else:
        try:
          sum += float(a)
        except:
          sys.stdout.write('Not a number: '+a+'\n')
          ok = 0
  seppts = string.join(l, ',')
  # get the computed sum for checking
  ok = 0
  while not ok:
    ok = 1
    sys.stdout.write('total number of points: ')
    l = sys.stdin.readline()
    l = string.strip(l)
    if l.find('.') == -1:
      try:
        total = int(l)
      except:
        sys.stdout.write('Not a number: '+l+'\n')
        ok = 0
    else:
      try:
        total = float(l)
      except:
        sys.stdout.write('Not a number: '+l+'\n')
        ok = 0
    if abs(0.0 + sum - total) > 0.1:
      sys.stdout.write('NOT sum of separate points: '+l+' ('+seppts+')\n')
      ok = 0
  sum = l
  # now produce the line for output and write to results file
  line = id+':'+examnr+':'+sum+':'+maxstr+':'+seppts+'\n'
  try:
    f = open(resfile, "a")
    f.write(line)
    f.close()
    sys.stdout.write('saved line:\n'+line)
  except:
    sys.stdout.write('Could not write to file: '+resfile+'\n')
    exit(6)
  return 1


###########################################################################
# main loop with counter
count = 0
l = 1
while 1:
  if l:
    count += 1
  l = getentry(count)

