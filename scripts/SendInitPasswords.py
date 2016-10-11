#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2010 by  Frank Lübeck  and   Max Neunhöffer
#

from startNOSERVER import *
import smtplib, time
from email.mime.text import MIMEText

if len(sys.argv) < 6:
  print('''
Usage:  SendInitPasswords.py  AlreadySentIDs MailTemplate Subject From AlsoTo\n
           This script does nothing if the information about the registered
           participants does not contain a persondata['InitPasswd'] entry.

           Otherwise it sends an email to all participant which have such 
           an entry and whose id is not listed in the file AlreadySentIDs.
           The id's of such participants are appended to AlreadySentIDs.

           The email is composed from the content of the file MailTemplate;
           the string INITPASSWD is substituted by persondata['InitPasswd']
           and the string EMAILHEADER is substituted by the
           result of the function in <EMailHeader> of Config.xml.

           The subject and from address should be given in argument Subject
           and From.

           Each mail is also sent to the address AlsoTo. This script sleeps
           for 5 seconds after sending a mail. (Such that if anything goes
           wrong not too much damage is done in a short time.)
''')
  sys.exit(1);


# read the id's which were handled before
try:
  f = open(sys.argv[1])
  s = f.read()
  f.close()
  doneids = s.split() 
except:
  if not os.path.exists(sys.argv[1]):
    print "Creating empty file "+sys.argv[1]
    f = open(sys.argv[1],"a")
    f.close()
    doneids = []
  else:
    print("Cannot open file "+sys.argv[1])
    sys.exit(2);

# read the mail template
try:
  f = open(sys.argv[2]);
  mail = f.read()
  f.close()
except:
  print("Cannot open file "+sys.argv[2])
  sys.exit(3);

# a short plausibility check
if mail.find('INITPASSWD') < 0:
  print "Mail template file "+sys.argv[2]+" contains no string 'INITPASSWD'."
  sys.exit(4)

def toutf8(str):
  return unicode(str, "iso-8859-1").encode("utf-8")

for k in Data.people.keys():
  p = Data.people[k]
  if not p.id in doneids:
    if p.persondata.has_key('InitPasswd'):
      print 'Sending to '+p.id
      body = mail.replace('INITPASSWD', p.persondata['InitPasswd'])
      body = body.replace('EMAILHEADER', toutf8(Config.conf['EMailHeaderFunction'](p)))
      msg = MIMEText(body)
      msg['Subject'] = sys.argv[3]
      msg['From'] = sys.argv[4]
      msg['To'] = p.email+', '+sys.argv[5]
      msg['Content-Type'] = 'text/plain; charset=utf-8'
      try:
        f = open(sys.argv[1], "a")
        f.write("\n"+p.id)
        f.close()
      except:
        print("Can not open file "+sys.argv[1]+" for appending.")
        sys.exit(5);
      server = smtplib.SMTP('localhost')
      try:
        check = server.sendmail(sys.argv[4], 
                              [p.email, sys.argv[5]], msg.as_string())
      except:
        print "Could not send mail for id: "+p.id
      if check <> {}:
        print "Problems with id: "+p.id+"\n"+str(check)
      server.quit()
      time.sleep(5)


