# -*- coding: ISO-8859-1 -*-
# OKUSON package                               Frank Lübeck / Max Neunhöffer

"""Here we collect a few very common utility functions:
   ...
"""

CVS = '$Id: Utils.py,v 1.1 2003/09/23 08:14:40 neunhoef Exp $'

import string, sys, re, exceptions, traceback, types

#
# We have our own Exception type:
#
class UtilsError(exceptions.Exception):
    '''Our own exception class for the Utils module.'''
    pass

#
# The following function transforms a position in an XML document as 
# specified by the pyRXP parser into human readable form:
#
def StrPos(pos):
    if pos[1] != None:   # element is non-EMPTY:
        return 'line '+str(pos[0][1])+' column '+str(pos[0][2])+' of '+ \
               pos[0][0].encode('ISO-8859-1','replace')+ \
               ' until line '+str(pos[1][1])+ ' column '+str(pos[1][2])
    else:
        return 'line '+str(pos[0][1])+' column '+str(pos[0][2])+' of '+ \
               pos[0][0].encode('ISO-8859-1','replace')


#
# The following function is used if we are in serious trouble:
#

def Panic(panicmsg, msg):
    '''Function for panic times. Program is aborted.'''
    sys.stderr.write("Panic: "+panicmsg+'\n')
    sys.stderr.write("Wanted to log message:\n"+msg+'\n')
    sys.exit(13)
    
#
# The following functions all report errors in some way or another. All 
# functions take the message as first argument and have an optional second
# argument "prefix" which defaults to "Error: " and is written in front of
# the message. 
# The default behaviour of this module can be overwritten by changing
# "Error" below:
#

def Error(msg, prefix="Error: "):
    '''This is just a wrapper to make it configurable.'''
    currentError(msg,prefix)

def ErrorToStderr(msg, prefix="Error: "):
    '''Function to report an error via stderr. Returns nothing.'''
    sys.stderr.write(prefix+msg+'\n')

def DoNothing(msg, prefix="Error: "):
    '''Function used to switch off error reporting.'''
    pass

ErrorLogFileName = "error.log"

import Lockfile

def ErrorToLogfile(msg, prefix="Error: "):
    '''Function to report errors in a logfile with NFS-safe file locking.
The global variable "ErrorLogFileName" in the module "Utils" contains
the name of the logfile used.'''
    try:
        res = Lockfile.Lock(ErrorLogFileName,reporterror = DoNothing)
        # The "reporterror = DoNothing" is required to avoid infinite
        # recursion!
        # Note that if we run into timeout, we log anyway, such that no
        # error message is really lost!
    except:
        # This is now the time to panic:
        traceback.print_exc()
        Panic("Cannot acquire lock for log file.",msg+prefix)
    try:
        f = file(ErrorLogFileName,"a")
        f.write(prefix+msg+'\n')
        if res == -2:    # we got a timeout:
            f.write("Warning: could not acquire lock for log file!\n")
        f.close()
    except:
        # Again nothing works any more:
        Panic("Cannot write to log file.",msg+prefix) 
    Lockfile.Unlock(ErrorLogFileName)
    # Note that this releases the lock, even if we did not acquire it
    # ourselves! With this policy the system recovers automatically
    # from a stale lock file, which is probably OK for a log file.

# A mechanism to switch standard behaviour:
currentError = ErrorToStderr

#
# Tools to read and write whole text files:
#

def StringFile(fname,reporterror=Error):
  try:
    f = open(fname)
  except:
    msg = 'Cannot open file '+str(fname)+' for reading.'
    reporterror(msg)
    raise UtilsError, msg
  try:
    s = f.read()
    f.close()
  except:
    msg = 'Cannot read file '+str(fname)+'.'
    reporterror(msg)
    raise UtilsError, msg
  return s

def FileString(fname, s, reporterror=Error):
  try:
    f = open(fname, 'w')
  except:
    msg = 'Cannot open file '+str(fname)+' for writing.' 
    reporterror(msg)
    raise UtilsError, msg
  try:
    f.write(s)
    f.close()
  except:
    msg = 'Cannot write to file '+str(fname)+'.'
    reporterror(msg)
    raise UtilsError, msg

# delete whitespace at beginning and end and substitute consecutive
# whitespace by single space
def NormalizedWhitespace(s, reporterror=Error):
  return string.strip(re.sub('['+string.whitespace+']+',' ',s))

# generic __repr__ method for class instances
indent = 0
def ReprInstance(obj):
  global indent
  s = ['Instance of ', obj.__module__, '.', obj.__class__.__name__, ':\n']
  indent += 2
  for a in dir(obj):
    if not (len(a) > 1 and a[:2] == '__'):
      s.append(indent*' ')
      s.append(a)
      s.append(' = ')
      s.append(repr(getattr(obj, a)))
      s.append('\n')
  indent -= 2
  return string.join(s, '')
  

class WithNiceRepr:
    def __repr__(self):
        global indent
        s = ['<Instance of ',self.__module__,'.',self.__class__.__name__,':\n']
        indent += 2
        for a in dir(self):
            if not (len(a) > 1 and a[:2] == '__'):
                s.append(indent*' ')
                s.append(a)
                s.append(' = ')
                o = getattr(self,a)
                if type(o) == types.MethodType:
                    s.append("method")
                else:
                    s.append(repr(o))
                s.append('\n')
        s.append('>')
        indent -= 2
        return string.join(s, '')
    
def PDFLatex(str, repeat=2):
  '''This gets a string as input which is valid input for pdflatex. The
function returns the PDF file produced by pdflatex as a string. It
returns 'None' if something went wrong.

The optional argument 'repeat' tells how many times pdflatex should be
run on the input (to get references an so on right).
'''
  return None
