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

def filterfile(fn,li):
    '''Copies file with name fn to a backup copy (appending '.bak'), then
       copy all those lines that do not start with some entry i in the list
       li to the original file name fn.'''
    print "Working on",fn,"..."
    fnbak = fn + '.bak'
    os.rename(fn,fnbak)
    f = file(fnbak)
    o = file(fn,"w")
    while 1:
        l = f.readline()
        if not(l): break
        docopy = 1
        for i in li:
            if len(i) > 0 and l.startswith(i):
                docopy = 0
        if docopy:
            o.write(l)
        else:
            sys.stdout.write('Deleting: '+l)
    o.close()
    f.close()

li = sys.argv[1:]
if len(li) > 0:
    filterfile(Config.conf['RegistrationFile'],li)
    filterfile(Config.conf['SubmissionFile'],li)
    filterfile(Config.conf['HomeworkFile'],li)
    filterfile(Config.conf['ExamRegistrationFile'],li)
    filterfile(Config.conf['ExamFile'],li)
    filterfile(Config.conf['GroupFile'],li)
    filterfile(Config.conf['MessageFile'],li)

