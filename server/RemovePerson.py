#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to remove one person from all data files. Please use
this only when the server is *NOT* running!'''

import os,sys

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# Fetch the "Utils" and switch error reporting to log file:

from fmTools import Utils

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data

if len(sys.argv) <= 1:
    print "Doing nothing. Please give IDs of people to remove on command line."
    sys.exit(0)

def filterfile(fn,i):
    '''Copies file with name fn to a backup copy (appending '.bak'), then
       copy all those lines that do not start with i to the original file
       name fn.'''
    print "Working on",fn,"..."
    fnbak = fn + '.bak'
    os.rename(fn,fnbak)
    f = file(fnbak)
    o = file(fn,"w")
    while 1:
        l = f.readline()
        if not(l): break
        if not(l.startswith(i)):
            o.write(l)
        else:
            sys.stdout.write('Deleting: '+l)
    o.close()
    f.close()

for i in sys.argv[1:]:
    # Be a little bit careful:
    if len(i) > 0:
        filterfile(Config.conf['RegistrationFile'],i)
        filterfile(Config.conf['SubmissionFile'],i)
        filterfile(Config.conf['HomeworkFile'],i)
        filterfile(Config.conf['ExamRegistrationFile'],i)
        filterfile(Config.conf['ExamFile'],i)
        filterfile(Config.conf['GroupFile'],i)
        filterfile(Config.conf['MessageFile'],i)

