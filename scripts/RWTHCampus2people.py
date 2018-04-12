#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2010 by  Frank Lübeck  and   Max Neunhöffer
#

from startNOSERVER import *
from fmTools import AsciiData

if len(sys.argv) < 2:
  print("     Usage:       RWTHCampus2people.py Teilnehmer_aus_Campus\n")
  sys.exit(1);

try:
  lines = open(sys.argv[1]).readlines()
except:
  print("Cannot open file "+sys.argv[1])
  sys.exit(2);

# create random passwords
import random, crypt
passwdchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
def randpwd():
  res = ''
  for i in range(8):
    res += random.choice(passwdchars)
  salt = random.choice(passwdchars)+random.choice(passwdchars)
  return [res, crypt.crypt(res, salt)]

known = []
new = []

for l in lines:
  l = l.strip("\n\r")
  s = map(lambda a: a.strip('"'), l.split(";"))
  # now we essentially copy from Webworkers.py
  if s[1] <> 'Matrikelnummer':
    id = s[1]
    if Data.people.has_key(id):
      known.append(id)
    else:
      new.append(id)
      pwd = randpwd()
      # Create a new Person object:
      p = Data.Person()
      p.id = id
      p.lname = s[3]
      p.fname = s[4]
      p.sem = 100 # not used
      p.stud = s[9]
      p.passwd = pwd[1]
      p.email = s[7]
      p.wishes = ''
      p.group = 0
      p.persondata = {'Anrede': s[2], 'Geburtsdatum': s[5],
                      'Geburtsort': s[6], 'Modulreferenz': s[8],
                      'InitPasswd': pwd[0] }

      # Construct data line for people file:
      line = AsciiData.LineTuple( (p.id,p.lname,p.fname,str(p.sem),p.stud,
                p.passwd,p.email, p.wishes,AsciiData.LineDict(p.persondata) ) )
      # Construct data line with group information:
      groupline = AsciiData.LineTuple( (id,str(p.group)) )
      Data.Lock.acquire()
      # Put new person into file on disk:
      try:
          Data.peopledesc.AppendLine(line)
          Data.groupdesc.AppendLine(groupline)
      except:
          Utils.Error('Failed to register person:\n'+l)
      # Put new person into database in memory:
      Data.people[id] = p
      Data.AddToGroupStatistic(p)
      Data.Lock.release()

print "Old: ",known,"\n"
print "New: ",new,"\n"

      
