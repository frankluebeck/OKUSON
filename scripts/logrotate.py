#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to rotate the log file. Just call it with the
   full absolute path name of the log file. Uses file locking. Typically
   this will be called from a daily cron job.'''

import os,sys,exceptions,time

VersionsToKeep = 100
CompressFrom = 2

# The following is copies from okuson/server/fmTools/Locking.py to make
# this script stand-alone:

timeout = 60

class Error(exceptions.Exception):
    '''Our own exception class for here.'''
    pass


def Lock(filename,printing = 0, reporterror = sys.stderr):
    '''Aquires a lock on filename. This is done in an NFS-safe way.
       Returns 0 if it works and raises an exception Error,
       if an error occurs. If the lock does not succeed until timeout,
       -2 is returned.'''
    counter = 0
    uniquename = filename+".LOCK."+str(os.getpid())+str(time.time())
    try:
        open(uniquename,"w").close()
    except:
        msg = 'Cannot acquire lock for "'+filename+'"'
        reporterror(msg)
        raise Error, msg

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

def Unlock(filename, reporterror = sys.stderr):
    try:
        os.unlink(filename+".LOCK")
    except:
        reporterror("Warning: Could not unlink lock file: "+filename+".LOCK")


# =======================================================================
# Here the real script starts:
# =======================================================================

if len(sys.argv) < 2:
    print "Usage: logrotate.py LOGFILENAME"
    sys.exit(0)

fullname = sys.argv[1]
dir = os.path.dirname(fullname)
name = os.path.basename(fullname)

os.chdir(dir)

l = os.listdir(".")
i = 0
while i < len(l):
    if l[i][:len(name)] != name:
        del l[i]
    else:
        i += 1

l.sort()


# First delete all that are too old:
i = 0
n = name+"."+ ("%03d" % (VersionsToKeep-1,) )
while i < len(l) and l[i] < n:
    i += 1
while i < len(l):
    os.unlink(l[i])
    del l[i]
# now i == len(l) in any case

# Secondly, we move everything from VersionsToKeep-1 down to 0 up by one,
# seeing to compression where applicable:
for i in xrange(VersionsToKeep-1,0,-1):
    n1 = name+"."+ ("%03d" % (i-1,))
    n2 = name+"."+ ("%03d" % (i,))
    try: 
        j = l.index(n1)
        # we have an uncompressed version here, just move and compress:
        os.rename(n1,n2)
        if i >= CompressFrom:
            os.system("gzip -9 "+n2)
            l[j] = n2+".gz"
        else:
            l[j] = n2
    except:
        try:
            j = l.index(n1+".gz")
            # we have a compressed version here, just move and decompress:
            os.rename(n1+".gz",n2+".gz")
            if i < CompressFrom:
                os.system("gzip -d "+n2+".gz")
                l[j] = n2
            else:
                l[j] = n2+".gz"
        except:
            pass

# Now we can touch the real file, but we use locking:

if Lock(name) < 0:
    print "Panic: Cannot acquire lock, aborting."
    sys.exit(1)

n2 = name+".000"
os.rename(name,n2)
f = file(name,"w")
f.close()
Unlock(name)

if 0 >= CompressFrom:
    os.system("gzip -9 "+n2)

