# -*- coding: ISO-8859-1 -*-
# fmTools package
#
# Copyright 2003 Max Neunhöffer / Frank Lübeck
#
"""This  module implements a generic approach to building a web server into
a Python application.
"""


CVS = '$Id: BuiltinWebServer.py,v 1.6 2003/11/03 21:46:08 neunhoef Exp $'


__version__ = "0.2"

import SocketServer, BaseHTTPServer
import os, sys, shutil, cgi, types, threading, time, urllib, string, select
import traceback,signal,socket
import Utils

# For all URL paths (without a query part in a GET request) which need special
# handling this dictionary must have an entry with the path as key and an
# instance of the WebResponse class as value. Other values lead to a "not
# found" error response. For all paths not contained in the keys of this 
# dictionary a 'DefaultWebResponse' is called (we define one as example and
# often useful default below).
Site = {}
# for the threading we need a lock to protect assignments to 'Site'
SiteLock = threading.Lock()

# can be delivered for killing
PID = os.getpid()

# The document root for the fallback to the filesystem:
DocRoot = '.'  # default is current dir of server, should not end in slash,
               # either relative to current dir or absolute

# List of file extensions that indicate a certain content type. In the
# default handler we only serve files whose extension is mentioned here.
TypeDict = { 'html' : 'text/html',
             'htm'  : 'text/html',
             'txt'  : 'text/plain',
             'bib'  : 'text/plain',
             'g'    : 'text/plain',
             'gd'   : 'text/plain',
             'gi'   : 'text/plain',
             'tex'  : 'text/plain',
             'gif'  : 'image/gif',
             'png'  : 'image/png',
             'jpg'  : 'image/jpeg',
             'pdf'  : 'application/pdf',
             'ps'   : 'application/ps',
             'dvi'  : 'application/dvi',
             'css'  : 'text/css',
           }


# In this dictionary one can specify file extensions as keys and assign 
# to them an initialization function which installs an entry in 'Site'
# for a file with such extension. (See below.)
# The install functions get arguments:     req, name_of_ext_file
# One can use the following automatic installation of requested URL's
# via a file with special extensions.
# A call 'add_special_extension(ext, spext, initfun)' causes the following:
# If a request for an URL with extension ext cannot be answered by
# delivering a corresponding file, then ext is substituted by the extension
# spext and it is checked if such a file exists. If yes the function initfun
# is called. This function gets the request and the path to the file with
# extension spext as arguments. It should produce an appropriate entry in
# Site under the requested URL path. 
# Example: the SimpleTemplate.py installs an entry
#    AddSpecialExtension('html', 'templ', InitSite_templ)
# where the init function parses and caches the template file, puts this into 
# a WebResponse object, and stores that in Site.
SpecialExtensionsDict = {}
def AddSpecialExtension(ext, spext, initfun):
  if not SpecialExtensionsDict.has_key(ext):
    SpecialExtensionsDict[ext] = []
  SpecialExtensionsDict[ext].append([spext, initfun])
  

# The prototype of a 'WebResponse': a class with one main method
#     .getresult(self, req, onlyhead)
# which gets a web server request req as argument.
# Entries in Site must be derived from this class.
# This method should return a 2-tuple, first a dictionary of
# HTTP headers and then the actual content of the response.
# The content can be either a string or an open file.
# In case of an error, a 'not found' message is returned.
# If 'onlyhead != 0' then the content can be None and should not be an open
# file.
# The data entry 'access_list' is a list of IP ranges that may connect
# to this page. Every IP range is described as a pair of two strings
# with 4 bytes, the first being the network's IP address and the second
# being the network's netmask. See 'verify_request' in the BuiltinWebServer
# class for details.
class WebResponse:
  access_list = [(socket.inet_aton('0.0.0.0'),socket.inet_aton('0.0.0.0'))]
  def getresult(self, req, onlyhead = 0):
    pass

def DeliverResponseMethod(req, onlyhead = 0, contenttype = ''):
    '''This is the getresult method for WebResponse objects that just deliver
a file.

In this implementation it does the following:
  - check if req.path is an existing file and if the real path starts with
    the real path of the 'DocRoot' (so, don't follow soft links to outside,
    and don't accept ..'s
    - if it is a directory that contains an 'index.html' file, then append
      '/index.html' to req.path and call self.do_WORK again
    - if not existing then return None
  - create header entries: Content-type, Last-modified, Content-length
    and open file to return

  - in case of appending something to the requested path, we generate a 
    'Location' header, in this case the generic server below sends an
    answer code 301 for 'permanently moved'
  - in case of a delivered file, this function returns the header dictionary
    and the open file. So, we don't load the file as a string but just copy
    the contents to the answer stream.
  - if no appropriate file was found we substitute the extension of the
    requested path by the extensions given in 'special_extensions' above.
    If this leads to an existing file, the init function from that
    dictionary is called and the do_WORK is redone. 
'''  
    
    realpath = os.path.realpath(DocRoot + req.path)

##  WARNING: if you modify this, don't forget to add a test like the
##  following, we do this is the default WebResponse below.  
##      docrootreal = os.path.realpath(DocRoot)
##      if realpath.find(docrootreal) != 0:
##        # not allowed to ask for files not really below the DocRoot
##        return
    if os.path.isdir(realpath):
      # handle directory in URL
      if len(req.path) == 0 or req.path[-1] != '/':
        req.path += '/'
      req.path += 'index.html'
      # recurse
      try:
        res = DeliverResponseMethod(req, onlyhead)
        res[0]['Location'] = req.path
        return res
      except:
        Utils.Error('Appending /index.html not successful, path: '+req.path)
        etype, value, tb = sys.exc_info()
        lines = traceback.format_exception(etype,value,tb)
        Utils.Error(string.join(lines),prefix="")
        return
    f = open(realpath, 'rb')
    if f:
      head = {}
      if contenttype == '':
        ext = os.path.splitext(req.path)[1][1:]
        head['Content-type'] = TypeDict.get(ext, 'text/plain')
      else:
        head['Content-type'] = contenttype
      head['Last-modified'] = req.date_time_string(os.path.getmtime(realpath))
      head['Content-length'] = str(os.path.getsize(realpath))    
      if onlyhead:
        f.close()
        f = None 
      return (head, f)

# The default WebResult instance, used when a path is not contained in the
# keys of 'Site'.
# Here, we check if requested path is a directory or has an extension
# contained in TypeDict. In that case deliver file with function above, 
# otherwise return None.
#
# This can be overwritten in applications (for example with functionality to
# (re)load entries into 'Site').
class DeliverWebResponse(WebResponse):
    def __init__(self, contenttype = ''):
      self.contenttype = contenttype
      
    def getresult(self, req, onlyhead = 0): 
      realpath = os.path.realpath(DocRoot + req.path)
      docrootreal = os.path.realpath(DocRoot)
      if realpath.find(docrootreal) != 0:
        # not allowed to ask for files not really below the DocRoot
        return
      if (not os.path.exists(realpath)):
        # nothing found, let's try other extensions
        main, extorig = os.path.splitext(realpath)
        if len(extorig) > 0:
          extorig = extorig[1:]
        if self.contenttype == '' and SpecialExtensionsDict.has_key(extorig):
          for k in SpecialExtensionsDict[extorig]:
            nam = main + '.' + k[0]
            if os.path.exists(nam):
              # found, so try to call init function to create an entry in 'Site'
              # and then call that entry (next time it is called directly in 
              # do_WORK)
              try: 
                k[1](req, nam)
                return Site[req.path].getresult(req, onlyhead)
              except:
                Utils.Error( 'Automatic Site install not successful, path:'+
                             req.path+', extension: '+k[0]+' .' )
                etype, value, tb = sys.exc_info()
                lines = traceback.format_exception(etype,value,tb)
                Utils.Error(string.join(lines),prefix="")
                pass

        return
      # for existing files we restrict delivery to files with extensions 
      # mentioned in 'TypeDict' and directories (i.e., <dir>/index.html)
      # or to files with given contenttype
      if self.contenttype != '':
        return DeliverResponseMethod(req, onlyhead, self.contenttype)
      if os.path.isdir(realpath) or \
                         TypeDict.has_key(os.path.splitext(req.path)[1][1:]):
        return DeliverResponseMethod(req, onlyhead)   

DefaultWebResponse = DeliverWebResponse()


def check_address(ipranges,ipadr):
    '''Checks whether ipadr is an IP address in one of the IP ranges in the
       list ipranges. Each iprange is specified as a pair of two strings
       of length 4, the first being the network's IP address and the second
       being the netmask. ipadr is given as a string in dot notation.''' 
    ipadr = socket.inet_aton(ipadr)
    for adr,mask in ipranges:
        #print repr(adr),repr(mask),repr(ipadr)
        if ord(ipadr[0]) & ord(mask[0]) == ord(adr[0]) and \
           ord(ipadr[1]) & ord(mask[1]) == ord(adr[1]) and \
           ord(ipadr[2]) & ord(mask[2]) == ord(adr[2]) and \
           ord(ipadr[3]) & ord(mask[3]) == ord(adr[3]):
            return 1
    return 0

# Global access_list for pages not registered in Site:
access_list = [(socket.inet_aton('0.0.0.0'),socket.inet_aton('0.0.0.0'))]


# Here is the RequestHandler class:
# If this is set then text/html results are sent through an XHTML
# validation. If a result is not valid, the function NoValidFunction
# is called with the request, the result (header dict, content as string) 
# and the exception e from the parser.
ValidateHTMLAsXHTML = 0
def NoValidFunction(req, res, e):
    # default behaviour is to write an error message
    Utils.Error(str(e))

class WebServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''A RequestHandler class for our generic web server.'''

    # Make the 'date_time_string' method of a
    # BaseHTTPServer.BaseHTTPRequestHandler instance more general to
    # allow optional time argument (seconds since epoch, now=0 is changed
    # to current time).
    def date_time_string(self, now=0):
        """Return date and time formatted for a message header."""
        if now == 0:
          now = time.time()
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(now)
        s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
        return s
    

    server_version = "BuiltinWebServer/" + __version__
    
    rbufsize = 0    # no buffering of input for POSTs, overwrites base class
    query = {}      # here we collect possible query information

    def do_WORK(self, onlyhead=0):
        '''In this method we really send the header and possibly data away.
We know that - if applicable - the query data is in self.query, 
otherwise self.query is {}. self.path is the path.'''
        
        # do we know this path in 'Site'?
        SiteLock.acquire()
        inSite = Site.has_key(self.path)
        SiteLock.release()
        if not inSite:
            if not(check_address(access_list,self.client_address[0])):
                self.send_error(403,"Access denied.")
                return

            # call the default WebResponse instance
            try:
              res = DefaultWebResponse.getresult(self, onlyhead)
            except:
              Utils.Error( 'Error in DefaultWebResponse.' )
              etype, value, tb = sys.exc_info()
              lines = traceback.format_exception(etype,value,tb)
              Utils.Error(string.join(lines),prefix="")
              res = None
        else:
            if not(check_address(Site[self.path].access_list,
                                 self.client_address[0])):
                self.send_error(403,"Access denied!")
                return

            try:
              res = Site[self.path].getresult(self, onlyhead)
            except:
              Utils.Error('No success with .getresult of: '+self.path)
              etype, value, tb = sys.exc_info()
              lines = traceback.format_exception(etype,value,tb)
              Utils.Error(string.join(lines),prefix="")
              res = None
        if res == None or type(res[0]) != types.DictType:
            self.send_error(404,"Not found")
            return
       
        # on the fly validation:
        if ValidateHTMLAsXHTML and res[0]['Content-type'] == 'text/html':
            import XMLRewrite, pyRXPU, tempfile
            if type(res[1]) != types.StringType:
                try:
                    dummy = res[1]
                    res = (res[0], dummy.read())
                    dummy.close()
                except:
                    res = (res[0], '')
            #Utils.Error('Validating '+str(self.path), prefix='Check: ')
            t = None
            try:
                t = XMLRewrite.ValidatingParser(res[1])
            except pyRXPU.error, e:
                res = [res[0], res[1]]
                NoValidFunction(self, res, e)
                res = (res[0], res[1])
            if not t:
                Utils.Error('NO SUCCESS on '+str(self.path), 
                             prefix='Validation: ')
        # Now send the header:
        try:
            if res[0].has_key('Location'):
              self.send_response(301)
            else:
              self.send_response(200)
            self.send_header('Accept-Ranges', 'bytes')
            for a in res[0].keys():
                self.send_header(a, res[0][a])
            self.end_headers()
            if onlyhead:
                return
        except:
            Utils.Error('Could not send header for '+str(self.path),
                         prefix='Warning: ')
        # send content away 
        if type(res[1]) == types.StringType:
            try:
                self.wfile.write(res[1])
            except:
                Utils.Error('Peer closed connection before all data '
                            'was sent.',prefix="Warning: ")
        else:
            try:
              shutil.copyfileobj(res[1], self.wfile)
              res[1].close()
            except:
              Utils.Error('No file object copied.')
              etype, value, tb = sys.exc_info()
              lines = traceback.format_exception(etype,value,tb)
              Utils.Error(string.join(lines),prefix="")
              pass
        return

    def do_HEAD(self):
        self.path = urllib.url2pathname(self.path)
        self.do_WORK(onlyhead=1)

    def do_GET(self):
        self.path = urllib.url2pathname(self.path)
        pos = self.path.find('?')
        if pos >= 0:
            self.query = cgi.parse_qs(self.path[pos+1:])
            self.path = self.path[0:pos]
        else:
            self.query = {}
        self.do_WORK()

    def do_POST(self):
        self.path = urllib.url2pathname(self.path)
        x = self.rfile.read(int(self.headers.getheader('content-length')))

        # The following throws away two extra bytes sent by IE, if we would
        # not do this, POSTs from IE would not work: [see bug #427345]
        try:
            while select.select([self.rfile], [], [], 0)[0]:
                if not self.rfile.read(1):
                    break
        except:
            Utils.Error("Select hack raised exception.",prefix="Warning")
        
        self.query = cgi.parse_qs(x)
        self.do_WORK()


    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client host and current date/time are prefixed to
        every message.
        """

        msg = ("%s - - [%s] %s" % 
           (self.address_string(), self.log_date_time_string(), format%args))
        Utils.Error(msg,"Log:")

class BuiltinWebServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    def get_request(self):
        """Get the request and client address from the socket.  """
        s = self.socket.accept()
        s[0].settimeout(30)
        return s

    raus = 0
    restartcommand = ''
    allow_reuse_address = 1
    request_queue_size = 5
    daemon_threads = 1

SERVER = None

# number of seconds we are willing to wait for threads to terminate:
TERMWAIT = 5

def sigusr1handler(sig,sta):
    '''Signal handler for SIGUSR1.'''
    SERVER.raus = 1

def StartServer(port = 8000):
    '''Starts the server.'''
    global SERVER
    server_address = ('',port)
    httpd = BuiltinWebServer(server_address, WebServerRequestHandler)
    SERVER = httpd
    # We need the following two to be able to interrupt the accept
    # call, such that the server really terminates:
    SERVER.ourpid = os.getpid()
    signal.signal(signal.SIGUSR1,sigusr1handler)   # handle signal USR1
    while not(httpd.raus):
        httpd.handle_request()
    Utils.Error("Waiting for threads to terminate...", prefix="Info: ")
    wait = TERMWAIT
    while threading.activeCount() > 1 and wait > 0:
        time.sleep(1)
        wait = wait - 1
    if httpd.restartcommand != '':
      # for freeing the port the new server will listen
      Utils.Error("Restarting...", prefix="Info: ")
      httpd.server_close()
      os.execl(httpd.restartcommand, httpd.restartcommand)
    Utils.Error("Terminating...", prefix="Info: ")
     

# finally, we add here a few more WebResponse classes of general interest

# a WebResponse with a cached result
class CachedWebResponse(WebResponse):
  def __init__(self, headers, content):
    if not headers.has_key('Content-length'):
      headers['Content-length'] = str(len(content))
    self.headers = headers
    self.content = content

  def getresult(self, req, onlyhead=0):
    return [self.headers, self.content]

# a WebResponse that calls a function which should produce the result
class FunctionWebResponse(WebResponse):
  def __init__(self, func):
    self.function = func

  def getresult(self, req, onlyhead=0):
    return self.function(req, onlyhead)


# a no WebResponse for marking certain URLs explicitly as 'Not found'
class NoWebResponse(WebResponse):
  def getresult(self, req, onlyhead=0):
    return None


