# -*- coding: ISO-8859-1 -*-
# fmTools package                               Frank Lübeck / Max Neunhöffer
# 
# This file contains utilities for processing XML files via a handler 
# object.
# The parser pyRXP used here allows to specify many flags which tell
# what should be evaluated during the parsing.
# For example, one can avoid the evaluation of entities or keep the
# comments in the parser result. This allows to exchange only some
# elements and to rewrite the others essentially as they were read.
#

CVS = '$Id: XMLRewrite.py,v 1.5 2004/05/03 13:11:00 neunhoef Exp $'

import os, sys, types, glob, pyRXPU, cStringIO, threading, traceback, string
import Utils

# We create a pyRXP Lock, because there are global variables in that
# C-module which cannot be shared by threads. So, in an application with
# threads: *Never* call a pyRXP function without having this lock.
pyRXPLock = threading.Lock()

# This is for creating a new parser while locking the pyRXP module. By
# default a parser with the pyRXP default settings is created. The settings
# can be changed by giving a dictionary with the parser attribute names as keys
# as argument 'config'.
def NewParser(config = {}):
  pyRXPLock.acquire()
  res = pyRXPU.Parser()
  for k in config.keys():
    setattr(res, k, config[k])
  pyRXPLock.release()
  return res

def Parse(parser = None, stri = None, file = None, config = None, 
          srcName = 'stringtoparse', reporterror = Utils.Error):
  '''This utility should be used for parsing XML files/strings in a threaded
environment. One can give a parser as argument 'parser' and a string
'stri' as input or a filename by the 'file' argument, then its content is
parsed. If successful, the result of the pyRXP parser are returned,
otherwise None is returned.
'''
  # first get input string, if 'file' given then get its content
  if file != None:
    try:
      stri = Utils.StringFile(file)
      srcName = file
    except:
      stri = ''
  if stri == None or type(stri) != types.StringType:
    reporterror('No string to parse.')
    return None
  # now get parser, either given as argument or newly created if argument
  # 'config' is given
  if config and type(config) == types.DictType:
    parser =  NewParser(config)
  if not parser:
    reporterror('No parser given.')
    return None
  # now parse
  pyRXPLock.acquire()
  try:
    res = parser.parse(stri, srcName = srcName)
  except:
    etype, value, tb = sys.exc_info()
    lines = traceback.format_exception(etype,value,tb)
    reporterror('Problem with XML parsing '+srcName+':\n'+string.join(lines))
    res = None  
  pyRXPLock.release()
  return res
  
# Here is a dictionary of .dtd and .ent file names as keys and a
# corresponding system path as values. By default we use files in 
# the 'dtds' subdirectory of the fmTools package.
DTD_ENT_FILES = {}

def find_dtd_ent_locate():
  '''Find all .dtd and .ent files on local machine via 'locate'.'''
  global DTD_ENT_FILES
  l = commands.getstatusoutput('locate "*.dtd"  "*.ent"')[1].split()
  for a in l:
    DTD_ENT_FILES[os.path.basename(a)] = a

def find_dtd_ent_file(fname):
  '''Read file where each line is the full path to a .dtd or .ent file 
on the local machine.'''
  global DTD_ENT_FILES
  s = Utils.StringFile(fname).split()
  for a in s:
    b = a.strip()
    if len(b) > 0:
      DTD_ENT_FILES[os.path.basename(b)] = b

def find_dtd_ent_default():
  '''Cache paths to .dtd and .ent files in 'dtds' subdirectory.''' 
  global DTD_ENT_FILES
  try: 
    path = os.path.dirname(os.path.abspath(__file__))
    s = glob.glob(os.path.join(path, 'dtds/*.ent')) + \
        glob.glob(os.path.join(path, 'dtds/*.dtd'))
    for a in s:
      DTD_ENT_FILES[os.path.basename(a)] = a
  except:
    pass

# call the default by default (distributed with XHTML, OKUSON and GAPDoc DTDs)
find_dtd_ent_default()

def eoCBfun(url):
  '''A translator of .dtd or .ent URL's in DOCTYPE declarations to
paths to local files, if available in DTD_ENT_FILES.

Store frequently needed DTD's in the 'dtds' subdirectory, or call
'find_dtd_ent_locate' (make sure there are no outdated versions on your
system) or 'find_dtd_ent_file'.
'''
  bname = os.path.basename(url)
  if DTD_ENT_FILES.has_key(bname) and os.path.exists(DTD_ENT_FILES[bname]):
    return DTD_ENT_FILES[bname]
  return url

# This is a list of flags which allows to write back a file almost identical
# to the input. Text before the first (header) and after the last tag
# are missing. See 'help(pyRXP)' for the list of possible flags. The
# validation is switched off. Just create your own flag combinations.
RewriteParserFlags = {
  'ReturnComments': 1,
  'ReturnCDATASectionsAsTuples': 1,
  'ReturnProcessingInstructions': 1,
  'ExpandGeneralEntities': 0,
  'ExpandCharacterEntities': 0,
  'NormaliseAttributeValues': 0,
  'ReturnDefaultedAttributes': 0,
  'RelaxedAny': 1,
  'SimpleErrorFormat': 1,
  'XMLStrictWFErrors': 0,
  'Validate': 0,
  'ProcessDTD': 0,
  'TrustSDD': 0,
  'ReturnList': 1}

# Create a parser for rewriting with above flags, see the pyRXP documentation 
# for an  explanation of the format of the output of this parser 
# (we append the a section from that doc at the end of this file)
RewriteParser = NewParser(RewriteParserFlags)

# And another list for use for validation with fully resolved of entities
# and info on processing instructions and comments.
ValidatingParserConfig = {
    'NormaliseAttributeValues': 1,
    'WarnOnRedefinitions': 1,
    'ExpandCharacterEntities': 1,
    'CaseInsensitive': 0,
    'XMLLessThan': 0,
    'IgnoreEntities': 0,
    'MergePCData': 1,
    'ErrorOnUnquotedAttributeValues': 1,
    'XMLPredefinedEntities': 1,
    'ReturnCDATASectionsAsTuples': 0,
    'MaintainElementStack': 1,
    'ErrorOnUndefinedElements': 1,
    'AllowUndeclaredNSAttributes': 0,
    'XMLExternalIDs': 1,
    'IgnorePlacementErrors': 0,
    'XMLMiscWFErrors': 1,
    'ReturnList': 1,
    'ErrorOnValidityErrors': 1,
    'AllowMultipleElements': 0,
    'XMLNamespaces': 0,
    'ProcessDTD': 1,
    'ErrorOnBadCharacterEntities': 1,
    'ReturnComments': 1,
    'XMLStrictWFErrors': 1,
    'ExpandEmpty': 0,
    'NoNoDTDWarning': 0,
    'XMLSyntax': 1,
    'ReturnDefaultedAttributes': 1,
    'ReturnProcessingInstructions': 1,
    'ErrorOnUndefinedAttributes': 1,
    'TrustSDD': 1,
    'MakeMutableTree': 0,
    'SimpleErrorFormat': 0,
    'ReturnNamespaceAttributes': 0,
    'RelaxedAny': 0,
    'Validate': 1,
    'XMLSpace': 0,
    'ExpandGeneralEntities': 1,
    'ErrorOnUndefinedEntities': 1,
    'eoCB': eoCBfun,
    }


# Create a validating parser with above flags, see the pyRXP documentation 
# for an explanation of the format of the output of this parser 
# (we append the a section from that doc at the end of this file)
ValidatingParser = NewParser(ValidatingParserConfig)

  
#########################################################################
##
##  Recursive walk through an XMLTree with possible modifications.

def XMLTreeRecursion(node,handlers,res):
    '''This is the dispatcher for a recursive walk through the XMLTree.
It is first called by "ProcessXMLTree" with the root of the tree as "tree"
and can in turn be called by handler routines to work on subtrees.'''
    # node can be string node, a unicode node or a true node
    if type(node) == types.StringType:
        handlers.handleString(node,res)   # default behaviour is a res.write
    elif type(node) == types.UnicodeType:
        handlers.handleString(node.encode('ISO-8859-1','replace'),res)
        # note that we ignore encoding problems here!
    # Now "node" must be a tuple:
    elif node[0] == '<![CDATA[':   # a CDATA section node
        handlers.handleCDATA(node,res)
    elif node[0] == '<!--':        # a comment node
        handlers.handleComment(node,res)
    elif node[0] == '<?':          # a processing instruction
        handlers.handlePI(node,res)
    elif hasattr(handlers,'handle_'+node[0]):
        method = getattr(handlers,'handle_'+node[0])
        method(node,res)
    else:
        handlers.handleDefault(node,res)

# For the processing of XML trees in memory we define a class:

class XMLElementHandlers(Utils.WithNiceRepr):
    '''Objects of this class are basically containers to hold methods
for elements of an XML tree. For an element of type XYZ the method
"handle_XYZ" is responsible. Exceptions of this rule are comment nodes,
processing instruction nodes, and CDATA section nodes, which have
special names, see below, because their names in the parse TREE contain
characters that are not valid in Python method names. Usually one will
inherit from this class, add methods and possibly data fields. All
handler methods by definition write on "out", their 3rd argument.'''
    wholeTree = None       # might be useful, is set by user of object
    def handleString(self,st,out):
        out.write(st)
        return 
    def handleComment(self,node,out):
        out.write('<!--')
        for n in node[2]:
            XMLTreeRecursion(n,self,out)
        out.write('-->')
    def handleCDATA(self,node,out):
        out.write('<![CDATA[')
        for n in node[2]:
            XMLTreeRecursion(n,self,out)
        out.write(']]>')
    def handlePI(self,node,out):
        out.write('<?')
        if node[1].has_key('name'):
            out.write(node[1]['name'] + ' ')
        for n in node[2]:
            XMLTreeRecursion(n,self,out)
        out.write('?>')
    def handleDefault(self,node,out):
        out.write('<')
        out.write(node[0])
        if node[1] != None:
            for k in node[1].keys():
                out.write(' '+k+'=')
                s = node[1][k]
                if s.find('"') == -1:
                    out.write('"'+s+'"')
                else:
                    out.write("'"+s+"'")
        if node[2] == None:
            out.write(' />')
        else:
            out.write('>')
            for n in node[2]:
                XMLTreeRecursion(n,self,out)
            out.write('</'+node[0]+'>')
                

def ProcessXMLTree(treeorlist, handlers, begin='', end=''):
    '''This utility gets a parse tree of an XML document and an
XMLElementHandlers object. The result is a string. If the handler object
has a method "handle_"+name of an element then the corresponding method
is called for that node of the tree. Standard methods see to it that the
element is just written out. Strings in the tree are just written out,
except if the handler method with name 'handleString' is overloaded.
Each handler function must take three arguments: self, node, res Here,
self is the handler object itself it has at least one data component
with name "wholeTree", which holds the full tree being processed. node
is a subelement inside the tree and res a (StringIO) file to which the
resulting string from that handler should be written.
"treeorlist" is either a tuple (root node) or a list of nodes (which
comes from setting 'ReturnList' to 1 in the parser attributes.
This is for the case that the result should contain some text before 
(e.g., a DOCTYPE declaration) or behind the outer element, such additional
texts can be given as arguments begin and end. Note that you have to
give the "<?xml ..." declaration at "begin" if the result should be
a valid XML document.'''
    res = cStringIO.StringIO()
    res.write(begin)
    handlers.wholeTree = treeorlist
    if type(treeorlist) == types.ListType:
        for ob in treeorlist:
            XMLTreeRecursion(ob,handlers,res)
            res.write('\n')   # looks nicer
    else:
        XMLTreeRecursion(treeorlist,handlers,res)
    res.write(end)
    result = res.getvalue()
    res.close()
    return result


# Here is now an interface to the BuiltinWebServer. This module can be
# used to apply sophisticated transformations to an XML file for
# delivery by a Web server.

import BuiltinWebServer

# A new WebResponse class. 
class XMLRewriteWebResponse(BuiltinWebServer.WebResponse):
  """This WebResponse class contains an  attribute 'tree' with a
parse tree of some XML code. 

Its 'getresult' method  constructs the results content by  running 
through this 'tree'  and calling  a handler for  each element that 
produces a replacement for that element in the input string. 
There must be an  attribute 'elementHandler' which contains an object
from the class "XMLElementHandlers". It is used by "ProcessXMLTree"
of functions  - the keys are element  names and they get as arguments  
      (self, current_node, req, onlyhead, result),
where result is an output stream (a StringIO).
These handlers append data  to result substituting this element
in the input XML code. If there is no handler for some element then the
default is to append the input code (something equivalent to it) for 
that element to result. 

If there is an attribute 'beginresult' it is used to initialize
'result' above. If there is an 'endresult' it is appended in the end.

(So, the {} elementHandler should basically return the input code, but 
parts before and after the main element are lost, like processing
instructions, comments or a DOCTYPE entry.)

The type of the result can be given as argument 'type' when an instance is
created, default is text/html. One should add an 'Expires' header line in 
an application.
"""
  
  def __init__(self, tree, type = 'text/html', handler = {}, \
                                      beginresult = '', endresult = ''):
    self.tree = tree
    self.type = type
    self.elementHandler = handler
    self.beginresult = beginresult
    self.endresult = endresult
  
  def getresult(self, req, onlyhead):
    res = ProcessXMLTree(self.tree, self.elementHandler, 
                         begin = self.beginresult, end = self.endresult)
    return ({'Content-type': self.type, 'Content-length': len(res),
              'Expires': 'now'},
            res)

# here is an empty handler object, make sure you fill it with an
# object from a derived class before it is used for automatic 
# installation of files.
ElementHandlers_tpl = XMLElementHandlers()

# init function for .tpl extensions in webserv, here we assume that .tpl
# files become XHTML 1.0 strict files after the rewrite.
# With the entry in webserv.site we cache the parsed XML tree.
def InitXHTMLRewriteWebResponse(req, nam):
  try:
    tree = Parse(RewriteParser, file = nam)
    response = XMLRewriteWebResponse(tree, handler = ElementHandlers_tpl,
               beginresult = '''<?xml version=1.0 encoding="ISO-8859-1"?>

<!DOCTYPE html
     PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

''',
               endresult = '\n')
  except:
    return

  BuiltinWebServer.SiteLock.acquire()
  BuiltinWebServer.Site[req.path] = response
  BuiltinWebServer.SiteLock.release()
  
BuiltinWebServer.AddSpecialExtension('html', 'tpl', InitXHTMLRewriteWebResponse)


# A second WebResponse class for direct installation into the Site 
# dictionary. Web pages are parsed during installation and not only
# when the page is requested first as for "XMLRewriteWebResponse".

class PreparsedXMLWebResponse(BuiltinWebServer.WebResponse,Utils.WithNiceRepr):
    tree = ('EMPTY', None, None, None)   # a dummy tree
    handlers = XMLElementHandlers()      # information how to process the tree
    filename = ""                        # name of source file
    begin = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
                                         # this is put before each result
    end = ''                             # this is put after each result

    def __init__(self,docroot,filename,handlers,type="text/html",
                 begin=None,end=None):
        '''Reads the file in os.path.join(docroot,filename) and parses it
as XML. Stores the full tree in the "tree" component. If any parse error
occurs the error is reported via "Utils.Error" and an exception is raised.
"handlers" must be an object from the class XMLElementHandlers. The 
"getresult" method uses "ProcessXMLTree" and the "handlers" to produce
a string for delivery. "begin" and "end" are strings which are put before
and after the result respectively.'''
        self.filename = os.path.join(docroot,filename)
        self.mtime = os.path.getmtime(self.filename)
        self.tree = Parse(RewriteParser, file = self.filename)
        self.handlers = handlers
        self.type = type
        if begin != None: self.begin = begin
        if end != None: self.end = end

    def getresult(self, req, onlyhead, handlers = None):
        '''Uses the already parsed tree to produce a response. If the 
optional argument "handlers" is None we use "self.handlers", otherwise
the optional argument.'''
        # check if file has changed, if yes try to parse, if successful 
        # change the tree
        mt = os.path.getmtime(self.filename)
        if  mt > self.mtime:
          new = Parse(RewriteParser, file = self.filename)
          if new:
            self.tree = new
            self.mtime = mt
        if handlers == None: handlers = self.handlers
        res = ProcessXMLTree(self.tree, handlers, 
                             begin = self.begin, end = self.end)
        return ({'Content-type': self.type, 'Content-length': len(res),
                  'Expires': 'now'},
                res)


##  For convenience here is a section from the pyRXP documentation,
##  explaining the output format of the parser.
##  
##  ----------------   begin citation  -------------------------------------
##  1.8 The Tuple Tree structure
##  
##  Most `tree parsers' such as DOM  create `node objects' of some sort. The
##  DOM gives  one consensus of  what such an  object should look  like. The
##  problem is  that "objects"  means "class instances  in Python",  and the
##  moment you start to  use such beasts, you move away from  fast C code to
##  slower  interpreted code.  Furthermore,  the nodes  tend  to have  magic
##  attribute names like "parent" or  "children", which one day will collide
##  with structural names.
##  
##  So,  we defined  the  simplest  structure we  could  which captured  the
##  structure of an XML document. Each tag is represented as a tuple of
##  
##        (tagName, dict_of_attributes, list_of_children, spare)
##  
##  The  dict_of_attributes  can  be  None  (meaning  no  attributes)  or  a
##  dictionary mapping  attribute names to values.  The list_of_children may
##  either be  None (meaning a singleton  tag) or a list  with elements that
##  are 4-tuples or plain strings.
##  
##  A  great advantage  of this  representation -  which only  uses built-in
##  types in Python  - is that you  can marshal it (and then  zip or encrypt
##  the results) with one line of Python code. Another is that one can write
##  fast C code to do things with the structure. And it does not require any
##  classes  installed on  the client  machine,  which is  very useful  when
##  moving xml-derived data around a network.
##  
##  This  does not  capture the  full structure  of XML.  We make  decisions
##  before parsing about whether to expand entities and CDATA nodes, and the
##  parser  deals with  it; after  parsing we  have most  of the  XML file's
##  content, but  we can't get  back to the original  in 100% of  cases. For
##  example both  of the following  will (with default settings)  return the
##  string "Smith & Jones", and you can't tell from the tuple tree which one
##  was in the file:
##  
##     <provider>Smith &amp; Jones<provider>
##  
##  Alternatively one can use
##  
##     <provider><[CDATA[Smith & Jones]]><provider>
##  
##  So  if you  want a  tool  to edit  and  rewrite XML  files with  perfect
##  fidelity, our  model is not rich  enough. However, note that  RXP itself
##  DOES provide all the hooks and could be the basis for such a parser.
##  
##  ----------------   end citation    -------------------------------------

