#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2010 by  Frank Lübeck  and   Max Neunhöffer
#
#   $Id:$

from startNOSERVER import *
import smtplib, time
from email.mime.text import MIMEText

if len(sys.argv) < 4:
  print('''
Usage:  SendEmails.py  MailTemplate Subject From\n
   The script sleeps for 1 second after sending a mail.
''')
  sys.exit(1);

# read the mail template
try:
  f = open(sys.argv[1]);
  mail = f.read()
  f.close()
except:
  print("Cannot open file "+sys.argv[2])
  sys.exit(2);

for k in Data.people.keys():
  p = Data.people[k]
  msg = MIMEText(mail)
  msg['Subject'] = sys.argv[2]
  msg['From'] = sys.argv[4]
  msg['To'] = p.email
  server = smtplib.SMTP('localhost')
  try:
    check = server.sendmail(sys.argv[4], 
                          [p.email], msg.as_string())
  except:
    print "Could not send mail for id: "+p.id
  if check <> {}:
    print "Problems with id: "+p.id+"\n"+str(check)
  server.quit()
  time.sleep(1)

