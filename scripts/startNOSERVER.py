#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2010 by  Frank Lübeck  and   Max Neunhöffer
#
'''Start OKUSON without actually starting the webserver (for scripts
which want to use the data from this server.
'''

import sys,os,time

homedir = os.path.abspath(sys.path[0])
os.environ["OKUSONHOME"] = os.path.join(homedir, "..")

sys.path = [os.path.join(os.environ["OKUSONHOME"], "server")] + sys.path

import Config
Config.NOSERVER = 1
from Server import *


