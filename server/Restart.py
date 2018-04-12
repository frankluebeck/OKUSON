#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to make the OKUSON server restart.'''

import os,sys,getpass,urllib,time,signal

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# Fetch the "Utils" and switch error reporting to log file:

from fmTools import Utils

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data


# Now we know the port we are running on, so we only need the
# administrator password to have a go...

print "Please enter the administrator password to restart OKUSON server:"
p = getpass.getpass("Administrator password: ")

pid = os.fork()
if pid == 0:
    time.sleep(0.1)   # Let the parent get hold of the log file
    # Now send the request:
    u = urllib.urlopen('http://localhost:'+str(Config.conf['Port'])+
                       '/AdminWork?Action=Restart&passwd='+p)
    u.close()
    sys.exit(0)  # Terminate this child process

# Set an alarm in 5 seconds:
def raus(a,b):
    print "\nWrong password! Server not restarting!"
    sys.exit(0)
signal.signal(signal.SIGALRM,raus)
signal.alarm(5)

f = file("log/server.log","r")
f.seek(0,2)     # seek to end of file
p = f.tell()

while 1:
    f.seek(0,2)
    np = f.tell()
    if np > p:
        f.seek(p)
        s = f.readlines()
        p = f.tell()
        for l in s:
            if l.find("passwd=") < 0: sys.stdout.write(l)
            if l[-25:] == 'Server up and running...\n':
                sys.exit(0)
            elif l == 'Aborting.\n':
                sys.exit(0)
    time.sleep(0.5)


