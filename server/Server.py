#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the main executable for the OKUSON server.'''

import os,sys,string,time,tempfile,traceback,locale,signal

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# try to get correct locale from environment
try:
  locale.setlocale(locale.LC_ALL, '')
except:
  pass

# Fetch the "Utils" and switch error reporting to log file:
from fmTools import Utils
Utils.ErrorLogFileName = os.path.join(Config.home,'log/server.log')
Utils.currentError = Utils.ErrorToLogfile
Utils.Error(time.asctime(time.localtime())+
            ' Starting server...',prefix='')

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data

# We perform a few sanity checks and give appropriate messages:
if not(os.path.isdir(Config.conf['DocumentRoot'])):
    Utils.Error('Cannot find DocumentRoot directory: '+
                Config.conf['DocumentRoot']);
    Utils.Error('Aborting.',prefix='')
    sys.exit(0)
if not(os.path.isdir(os.path.join(Config.conf['DocumentRoot'],'images'))):
    Utils.Error('DocumentRoot directory does not contain an "images" '
                'subdirectory.')
    Utils.Error('Aborting.',prefix='')
    sys.exit(0)
if not(os.path.isdir(os.path.join(Config.home,'tmp'))):
    Utils.Error('Cannot find "tmp" subdirectory in OKUSON home directory.')
    Utils.Error('Aborting.',prefix='')
    sys.exit(0)
    
# Now we put some configuration data into the necessary places of our
# generic library routines:

from fmTools import LatexImage
LatexImage.LatexTemplate = Config.conf["LaTeXTemplate"]


# Change temporary file location:
tempfile.tempdir = os.path.join(Config.home,'tmp')


# Next we read all available exercises:

Utils.Error('Reading exercises and sheets...',prefix='Info: ')

import Exercises

for d in Config.conf['ExerciseDirectories']:
    Exercises.ReadExercisesDirectory(d)

# Next we read all available sheets:

for d in Config.conf['SheetDirectories']:
    Exercises.ReadSheetsDirectory(d)

# Now create all images for web service:
for r in Config.conf['Resolutions']:
    name = os.path.join(Config.conf['DocumentRoot'],"images",str(r)+"dpi")
    if not(os.path.isdir(name)):
        try:
            os.mkdir(name)
        except:
            Utils.Error('Cannot create directory for images in resolution '+
                        str(r)+':\n  '+name+'\nAborting.')
            sys.exit(0)
Exercises.CreateAllImages()


# Now we load personal data, we begin with the registrations:

import Data

try:
    Utils.Error('Reading personal data...',prefix='Info: ')
    Data.peopledesc.LoadFile()
    Utils.Error('Reading multiple choice data...',prefix='Info: ')
    Data.mcresultsdesc.LoadFile()
    Utils.Error('Reading homework data...',prefix='Info: ')
    Data.homeworkdesc.LoadFile()
    Utils.Error('Reading exam registration data...',prefix='Info: ')
    Data.examregdesc.LoadFile()
    Utils.Error('Reading exam result data...',prefix='Info: ')
    Data.examdesc.LoadFile()
    Utils.Error('Reading group data...',prefix='Info: ')
    Data.groupdesc.LoadFile()
    Utils.Error('Reading message data...',prefix='Info: ')
    Data.messagedesc.LoadFile()
    Data.cleanRevokedMessages()   # clean revoked messages
    Utils.Error('Reading group information...',prefix='Info: ')
    Data.groupinfodesc.LoadFile()
except:
    Utils.Error('Aborting.',prefix='')
    sys.exit(0)

# Now count the statistics for the distribution into tutoring groups:
Utils.Error('Counting participants of tutoring groups...',prefix='Info: ')
Data.MakeGroupStatistic()


# Start our web server:
# (switching XHTML validation of html files on.) 
from fmTools import BuiltinWebServer
BuiltinWebServer.ValidateHTMLAsXHTML = 1
def NoValidFunction(req, res, e):
    # We save the result in a temporary directory as well as the exception
    # message. Then we remove the ValidatorIcon. 
    tmp = tempfile.mktemp()
    os.mkdir(tmp)
    fn = 'novalid_'+os.path.basename(req.path)
    Utils.FileString(os.path.join(tmp, fn), res[1])
    Utils.Error('Saved in dir '+tmp, prefix = 'See: ')
    Utils.FileString(os.path.join(tmp, 'message'), str(e))
    # Remove ValidatorIcon:
    res[1] = string.replace(res[1], WebWorkers.ValidatorIconText, '')
    # Adjust Content-length:
    res[0]['Content-length'] = str(len(res[1]))

BuiltinWebServer.NoValidFunction = NoValidFunction
Utils.Error('Preparsing all web page templates...',prefix='Info: ')
import WebWorkers           # this initializes the web services

WebWorkers.RegisterAllTpl()

# Just an info:
Utils.Error('Formatting current time on sheets like: ' + 
            WebWorkers.LocalTimeString(), prefix = 'Info: ')

# We are ready, service can begin:
try:
    Utils.Error(time.asctime(time.localtime(time.time()))+
                ' Ready to start service ...',prefix='')
    BuiltinWebServer.StartServer(port = Config.conf['Port'])
except:
    Utils.Error(' Cannot start service! (Port in Use? Server running?)')


