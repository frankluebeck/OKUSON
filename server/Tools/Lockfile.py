# -*- coding: ISO-8859-1 -*-
#!/usr/bin/env python

'''Implements locking via files in an NFS-safe way using "link" as
atomic file system operation.'''

CVS = '$Id: Lockfile.py,v 1.1 2003/09/23 08:14:40 neunhoef Exp $'

##########################################################################
##  
##                      AufgabenServer package
##  Authors:  Frank Lübeck
##            Max Neunhöffer
##  
##  Copyright by the authors
##  
##  
##########################################################################

import os,time,sys
import Utils

timeout = 60

def Lock(filename,printing = 0, reporterror = Utils.Error):
    '''Aquires a lock on filename. This is done in an NFS-safe way.
       Returns 0 if it works and raises an exception Utils.UtilsError,
       if an error occurs. If the lock does not succeed until timeout,
       -2 is returned.'''
    counter = 0
    uniquename = filename+".LOCK."+str(os.getpid())+str(time.time())
    try:
        open(uniquename,"w").close()
    except:
        msg = 'Cannot acquire lock for "'+filename+'"'
        reporterror(msg)
        raise Utils.UtilsError, msg
         
    while 1:
        try:
            os.link(uniquename,filename+".LOCK")
            break
        except:
            try:
                if os.stat(uniquename)[3] == 2:
                    break   # this worked despite the error!
            except:
                pass
            if printing:
                sys.stdout.write(".")
                sys.stdout.flush()
            time.sleep(1)
            counter += 1
            if counter > timeout:
                os.unlink(uniquename)
                return -2
    os.unlink(uniquename)
    return 0

def Unlock(filename, reporterror = Utils.Error):
    try:
        os.unlink(filename+".LOCK")
    except:
        reporterror("Warning: Could not unlink lock file: "+filename+".LOCK")


