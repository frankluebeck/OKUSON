#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the main executable for the OKUSON server.'''

import os,sys,time,tempfile,traceback,locale

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# try to get correct locale from environment
try:
  locale.setlocale(locale.LC_ALL, '')
except:
  pass

# Fetch the "Utils" and switch error reporting to log file:

from Tools import Utils
Utils.ErrorLogFileName = os.path.join(Config.home,'log/server.log')
Utils.currentError = Utils.ErrorToLogfile
Utils.Error(time.asctime(time.localtime())+
            ' Starting server...',prefix='')

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data


# Now we put some configuration data into the necessary places of our
# generic library routines:

from Tools import LatexImage
LatexImage.LatexTemplate = Config.conf["LaTeXTemplate"]


# Change temporary file location:
tempfile.tempdir = os.path.join(Config.home,'tmp')


# Next we read all available exercises:

Utils.Error('Reading exercises and sheets...',prefix='Info:')

import Exercises

for d in Config.conf['ExerciseDirectories']:
    Exercises.ReadExercisesDirectory(d)

# Next we read all available sheets:

for d in Config.conf['SheetDirectories']:
    Exercises.ReadSheetsDirectory(d)

# Now create all images for web service:
for r in Config.conf['Resolutions']:
    name = os.path.join(Config.home,"html","images",str(r)+"dpi")
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
    Utils.Error('Reading personal data...',prefix='Info:')
    Data.peopledesc.LoadFile()
    Utils.Error('Reading multiple choice data...',prefix='Info:')
    Data.mcresultsdesc.LoadFile()
    Utils.Error('Reading homework data...',prefix='Info:')
    Data.homeworkdesc.LoadFile()
    Utils.Error('Reading exam registration data...',prefix='Info:')
    Data.examregdesc.LoadFile()
    Utils.Error('Reading exam result data...',prefix='Info:')
    Data.examdesc.LoadFile()
    Utils.Error('Reading group data...',prefix='Info:')
    Data.groupdesc.LoadFile()
    Utils.Error('Reading message data...',prefix='Info:')
    Data.messagedesc.LoadFile()
except:
    Utils.Error('Aborting.',prefix='')
    sys.exit(0)

# Now count the statistics for the distribution into exercises classes:
Utils.Error('Counting participants of exercise classes...',prefix='Info:')
Data.MakeGroupStatistic()


# Start our web server:

import WebWorkers           # this initializes the web services
WebWorkers.RegisterAllTpl()

# Just an info:
Utils.Error(' Formatting current time on sheets like: ' + 
            WebWorkers.LocalTimeString(), prefix = 'Info:')

# We are ready, service can begin:
Utils.Error(time.asctime(time.localtime(time.time()))+
            ' Server up and running...',prefix='')

from Tools import BuiltinWebServer

BuiltinWebServer.StartServer(port = Config.conf['Port'])

