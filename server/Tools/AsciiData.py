# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This module allows easy access to line-based ASCII data. The code
here is generic, the data structures on mass storage and in memory can
be configured via a certain type of straight line programs as described
below. It is safe to import * from this module. The following identifiers
will be imported:
  LineTuple, TupleLine, FileDescription, NewNode, TypeOfNode.
'''

CVS = '$Id: AsciiData.py,v 1.2 2003/09/26 21:35:05 luebeck Exp $'

import string, os, sys, types, exceptions, threading
import Utils

# Our exception class:
class DataError(exceptions.Exception):
    pass

# First we provide two basic functions to encode and decode string tuples
# into ascii lines:

def LineTuple(t,delimiter = ':'):
    '''The first argument t must be a tuple or a list of strings. The
delimiter can be an arbitrary string not containing backslashes.
This function basically joins the strings in t to one string by
putting the delimiter between any two strings. However, occurences
of the delimiter in the strings are encoded, as are line ends, 
carriage returns and hash (#) characters. The function returns the 
encoded string.
'''
    l = []
    for s in t:
        # we first protect backspaces:
        ss = s.replace('\\','\\e')
        ss = ss.replace(delimiter,'\\d')
        ss = ss.replace('\n','\\n')
        ss = ss.replace('#','\\c')
        ss = ss.replace('\r','\\r')
        # now there are only backslashes in ss followed by c, d, e, n, or r
        l.append(ss)
    return string.join(l,delimiter)

def TupleLine(l,delimiter = ':'):
    '''The first argument l must be a string in which the character
after each backslash is either c, d, e, n or r. The delimiter can be
an arbitrary string not containing backslashes. 
This function basically splits l into substrings at all occurences of
delimiter. A trailing newline is discarded. For each substring the
encoding from the function LineTuple is reversed. The list of decoded
substrings is returned.
'''
    if (len(l) > 0 and l[-1] == '\n'): l = l[:-1]
    ll = l.split(delimiter)
    for i in range(len(ll)):
        s = ll[i].replace('\\d',delimiter)
        s = s.replace('\\n','\n')
        s = s.replace('\\r','\r')
        s = s.replace('\\c','#')
        ll[i] = s.replace('\\e','\\')
    return ll

# Description of straight line programs:
#
# Assumptions and conventions: 
#
# * The memory representation is a tree with one root, where each node
#   is either a dictionary, an instance (member of a class) or a vector (a
#   list), and each leaf is a string or an integer.
# * A straight line program (SLP) is a tuple.
# * A SLP describes, how the tree of the memory representation is traversed
#   and modified to store the data coming from one line of data in the 
#   external representation.
# * Each "command" consists of one from {"STORE", "ENTER", "FILL", "LEAVE", 
#   "HOME"},
#   followed by a fixed number of arguments as described below.
# * During the execution of a SLP the tree in memory is extended with
#   the information from the input line.
# * Fields in the input line (seperated by the delimiter) are numbered
#   beginning with 0
# * During the execution of a SLP a "current" location as well as the
#   path from the root to it are kept.
# * At the beginning of the execution of a SLP the current location is
#   at the root of the memory representation.
#
# The commands:
# "STORE" - Followed by 3 arguments: n, f, t
#         n is a number of a field in the input line, f is a string or 
#         integer and t is either "STRING "or "INT".
#         This command is used to store a value in the tree.
#         It stores the value in field number n in the entry named f of the
#         current location in the tree. The value is stored as a string
#         or as an integer, depending on t.
#         If there is a vector at the current location then f must be 
#         an integer or "NEXT", otherwise a string. If f is "NEXT" then
#         the value is appended to the vector at the current position.
# "ENTER" - Followed by 3 arguments: n, f, t
#         n is a number of a field in the input line, f is either a string
#         or an integer or "KEY" and t is either "DICT", "VECT "or a Python 
#         class. This command is used to enter a subtree.
#         The current location in the tree is changed to the subtree that
#         is described by f. If there is a dictionary or instance at the
#         current position, f must be a string and names the field where
#         the subtree is stored. If there is a vector at the current
#         location, f must be the index, where the subtree is stored.
#         If f is equal to "KEY", then the entry where the subtree is
#         stored is selected by the field with number n from the input
#         line (possibly converted to an integer in case of a vector at
#         the current location). t is used if the corresponding subtree
#         does not yet exist. In this case a new node is created. If
#         t is "DICT", a dictionary is created, if t is "VECT", a vector
#         (a Python list) is created, if t is a Python class, a new 
#         instance is created with a call to the constructor method of
#         this class without arguments.
# "FILL"  - Followed by 3 arguments: n, f, t
#         n is a number of a field in the input line, f is a string or
#         integer and t is either "STRING "or "INT".
#         This command is used to store the rest of an input line into
#         a vector in the tree.
#         It stores the values in the fields from number n up to the end
#         of the input line into a vector stored under the entry named f
#         if the current location in the tree. The values are stored as 
#         strings or as a integers, depending on t.
#         If there is a vector at the current location then f must be an
#         integer, otherwise a string.
# "LEAVE" - Not followed by any argument.
#         This command is used to leave a subtree.
#         The current location in the tree is changed to the last location
#         that was current before the "ENTER "command that led to the current
#         location.
# "HOME"  - Not followed by any argument.
#         This command is used to leave all subtrees and start again at the
#         root.
#         The current location is set to the root of the tree and all earlier
#         "current locations" are forgotten.


# Some helper functions:
def TypeOfNode(o,reporterror=Utils.Error):
    '''Determines type of node, possible values: "DICT", "VECT", "OBJ".'''
    if type(o) == types.DictType:
        return "DICT"
    elif type(o) == types.ListType:
        return "VECT"
    elif type(o) == types.ClassType:
        return type(o)
    elif type(o) == types.InstanceType:
        return o.__class__
    else:
        msg = "Unknown node type."
        reporterror(msg)
        raise DataError, msg

def NewNode(t):
    '''Creates and returns a new node of type t, possible values: "DICT",
"VECT", or a Python class.'''
    if t == "DICT": return {}     # a new empty dictionary
    elif t == "VECT": return []   # a new empty vector/list
    else: return t()              # this creates a new instance

# The following class is for objects describing external storage and
# access to data structures in memory:
class FileDescription:
    '''Objects in this class describe a line based ascii data file
and a corresponding representation in memory. Generic methods to
parse and load single lines or complete files are given. The
description language is that of certain straight line programs
as described above.
''' 
    filename = ""      # name of the data file
    root = {}          # root object in memory representation
    delimiter = ":"    # delimiter, arbitrary string not containing backslashes
    slp = ()           # straight line program, description see below
    lock = None        # a lock object to allow multi-threaded access to file

    def __init__(self,filename,root,slp = None,delimiter = ':'):
        self.filename = filename
        self.root = root
        self.delimiter = delimiter
        if slp == None:
            self.slp = ()   # this has to be assigned later!
        else:
            self.slp = slp
        self.lock = threading.Lock()    # for locking between different threads

    def LoadLine(self,l,reporterror=Utils.Error):
        '''Parses the line l and loads data into memory representation.'''
        ls = l.strip()
        if len(ls) == 0 or ls[0] == '#': return  # we ignore comments

        # First we split the current line and decode the parts:
        ll = TupleLine(l,self.delimiter)

        # Initialize data structures:
        locstack = [self.root]
        typstack = [TypeOfNode(self.root,reporterror=reporterror)]

        # Now execute the slp:
        ip = 0                   # instruction pointer
        while ip < len(self.slp):
            tos = locstack[-1]
            tost = typstack[-1]
            # "STORE":
            if self.slp[ip] == "STORE":
                # Get arguments:
                n = self.slp[ip+1]
                f = self.slp[ip+2]
                t = self.slp[ip+3]
                ip += 4
                # A check:
                if n >= len(ll):
                    msg = 'Error: Too few fields ( <'+str(n+1)+')\nLine:'+l
                    reporterror(msg)
                    raise DataError, msg
                # Determinte result type and result:
                if t == "INT":
                    try:
                        v = int(ll[n])
                    except:
                        msg = 'Warning: Not an integer: '+ll[n]+ \
                              ' (assuming 0)\nLine:'+l
                        reporterror(msg)
                        v = 0
                else:
                    v = ll[n]
                # Store it, depending on node type:
                #print "Storing",v,"into",tos,f
                if tost == "DICT":
                    tos[f] = v
                elif tost == "VECT":
                    if f == "NEXT":
                        i = len(tos)
                    else:
                        i = int(f)
                    while len(tos) <= i: tos.append(None)
                    tos[i] = v
                else:   # an instance
                    setattr(tos,f,v)
            # "ENTER":
            elif self.slp[ip] == "ENTER":
                # Get arguments:
                n = self.slp[ip+1]
                f = self.slp[ip+2]
                t = self.slp[ip+3]
                ip += 4
                if f == "KEY":     # data determines where to go
                    # A check:
                    if n >= len(ll):
                        msg = 'Error: Too few fields ( <'+str(n+1)+ ')\n' + \
                              'Line:'+l
                        reporterror(msg)
                        raise DataError, msg
                    f = ll[n]
                # now determine the subtree:
                if tost == "DICT":
                    if not(tos.has_key(f)): # We have to create a new subtree:
                        tos[f] = NewNode(t)
                    sub = tos[f]
                elif tost == "VECT":
                    try:
                        i = int(f)
                    except:
                        msg = 'Error: No number: '+f+'\n' + 'Line:'+l
                        reporterror(msg)
                        raise DataError, msg
                    if i >= len(tos):   # nothing there
                        while i >= len(tos): tos.append(None)
                    sub = tos[i]
                    if sub == None:
                        tos[i] = NewNode(t)
                        sub = tos[i]
                    elif TypeOfNode(sub,reporterror=reporterror) != t:
                        msg = 'Error: Tree already incorrect!\nLine:'+l+ \
                              'Tree:'+str(sub)
                        reporterror(msg)
                        raise DataError, msg
                else:   # an instance
                    try:
                        sub = getattr(tos,f)
                        if TypeOfNode(sub,reporterror = reporterror) != t:
                            msg = 'Error: Tree already incorrect!\nLine:'+l+ \
                                  'Tree:'+str(sub)
                            reporterror(msg)
                            raise DataError, msg
                    except DataError:
                        raise
                    except:
                        sub = NewNode(t)
                        setattr(tos,f,sub)
                locstack.append(sub)
                typstack.append(TypeOfNode(sub,reporterror=reporterror))
            # "LEAVE":
            elif self.slp[ip] == "LEAVE":
                ip += 1
                del locstack[-1]
                del typstack[-1]
            # "HOME":
            elif self.slp[ip] == "HOME":
                ip += 1
                locstack = [self.root]
                typstack = [TypeOfNode(self.root,reporterror = reporterror)]
            # "FILL":
            elif self.slp[ip] == "FILL":
                # Get arguments:
                n = self.slp[ip+1]
                f = self.slp[ip+2]
                t = self.slp[ip+3]
                ip += 4
                # collect values:
                v = []
                while n < len(ll):
                    if t == "INT":
                        try:
                            v.append(int(ll[n]))
                        except:
                            msg = 'Warning: Not an integer: '+ll[n]+ \
                                  ' (assuming 0)\nLine:'+l
                            reporterror(msg)
                            v.append(0)
                    else:
                        v.append(ll[n])
                    n += 1
                # Store it, depending on node type:
                if tost == "DICT":
                    tos[f] = v
                elif tost == "VECT":
                    i = int(f)
                    while len(tos) <= i: tos.append(None)
                    tos[i] = v
                else:   # an instance
                    setattr(tos,f,v)
            else:   # not possible
                msg = 'Error: Not a command: '+str(self.slp[ip])
                reporterror(msg)
                raise DataError, msg
        return   # end of method

    def LoadFile(self,fname = None,reporterror = Utils.Error):
        '''Parses the whole file f and loads data into memory representation.
f can either be a Python file object or a file name in which case data
is read from the corresponding file. Called with the default value None
this method will read from the file specified in self.filename.'''
        self.lock.acquire()
        if fname == None: fname = self.filename
        if type(fname) == types.StringType:
            try:
                f = file(fname)
            except:
                msg = 'Cannot read file: "'+fname+'"'
                reporterror(msg)
                self.lock.release()
                raise DataError, msg
        else:
            f = fname
            fname = "[Unknown]"
        try:
            l = f.readline()
            while l:
                self.LoadLine(l,reporterror=reporterror)
                l = f.readline()
            f.close()
        except DataError:
            self.lock.release()
            raise
        except:
            msg = 'Read error for file: "'+fname+'"'
            reporterror(msg)
            self.lock.release()
            raise DataError, msg
        self.lock.release()

    def AppendLine(self,l, reporterror = Utils.Error):
        '''Appends a line to the default file using lock object for
           unique access.'''
        self.lock.acquire()
        if l[-1] != '\n': l = l + '\n'
        try:
            f = file(self.filename,"a")
            f.write(l)
            f.close()
        except:
            msg = 'Error: Cannot append a line to file "'+self.filename+'"'
            reporterror(msg)
            self.lock.release()
            raise DataError, msg
        self.lock.release()

