# -*- coding: ISO-8859-1 -*-
#!/usr/bin/env python
##  SimpleTemplate.g                              
##  
##  
##  This  file  contains  utility  functions  for  substituting  parts  of
##  template  files in  an  easy way.  In many  applications  this may  be
##  simpler  and  faster  than  the  more  sophisticated  XML-approach  in
##  'XMLRewrite.py'.
##  
##  Copyright 2003  Frank Lübeck / Max Neunhöffer
##  
"""
A template file for this module looks as follows. 

Special parts of the file are marked by one of the sequences
  (%<key>%)    or    (%<key>!<val>%)
where <key> and <val> can be any strings not containing the substring
'%)', and <key> doesn't contain a '!' character.
The first form is an abbreviation for the case (%<key>!%) with an empty
<val>.

Assuming that the content of such a file is assigned to a string str,
this string can be processed to return another string new by:

  new = FillTemplate(str, dict)

Here <dict> is a dictionary. 
If <dict> has a key <key> then
  If <dict>[<key>] is a string then any occurence of
     (%<key>!<val>%) in <str> is replaced by this string, non-recursively
  If <dict>[<key>] is a function f then each (%<key>!<val>%) is replaced
     by f(<key>, <val>, <dict>) which should return a string

Those (%<key>!<val>%) with no key <key> in <dict> are substituted by <val>.

Remarks: Note that <val> is used as a default substitution or, in case 
of a function in <dict>[<key>] as a function argument.
The rules tell that the string '(%' can be included in the result 
by '(%!(%%)' (provided there is no entry with key '' in  dict).
"""

CVS = '$Id: SimpleTemplate.py,v 1.1 2003/09/23 08:14:40 neunhoef Exp $'

import types, time, os, string
import Utils

# The named arguments BSEP and ESEP allow to use other delimiters to mark
# the key!val pairs. 
def ParseString(str, BSEP = '(%', ESEP = '%)'):
  """Here str should be a string holding the content of a template file.
This function parses the string and returns a list res. Each entry of
res is either a string is it corresponds to text outside any (%...%),
or a list with two elements [key, val] for a key-value-pair in str.
"""
  lstr = len(str)
  res = []
  pos = 0
  while pos != -1 and pos < lstr:
    bpos = str.find(BSEP, pos)
    if bpos == -1:
      # done, no more key-val-pairs
      res.append(str[pos:])
      return res
    epos = str.find(ESEP, bpos+2)
    if epos == -1:
      # also done, a last BSEP without ESEP is part of text
      res.append(str[pos:])
      return res
    res.append(str[pos:bpos])
    part = str[bpos+2:epos]
    excl = part.find('!')
    if excl != -1:
      res.append([part[:excl], part[excl+1:]])
    else:
      res.append([part, ''])
    pos = epos+2
  return res


def ParseFile(fname, reporterror = Utils.Error):
  "Reads file fname into a string and calls ParseString.\n"
  str = Utils.StringFile(fname, reporterror=reporterror)
  return ParseString(str)

# A dictionary for FillTemplate, containing a few functions of possible
# general interest.
def filterLang(key, val, dict):
  if dict.has_key('LANG') and key == dict['LANG']:
    return val
  else:
    return ''

def dateTime(key, val, dict):
  return time.ctime()

def callFunc(key, val, dict):
  try:
    fu = dict[FUNCS][val]
    return fu(key, val, dict)
  except:
    return ''

DefaultDict = {
  'FUNCS' : {},
  'LANG': 'en',
  'de': filterLang,
  'fr': filterLang,
  'en': filterLang,
  'date': dateTime,
  'func': callFunc,
}

# Overwrite with your own dictionary if necessary.
Dict = DefaultDict

def FillTemplate(l, dict):
  """Here l must be a string or have the form as produced by ParseString, 
and dict must be a dictionary. Then l is processed as explained in the 
help for this module. 

The return value is the string new.
"""
  if types.StringType == type(l):
    l = ParseString(l)
  res = []
  for a in l:
    if types.StringType == type(a):
      res.append(a)
    else:
      if not dict.has_key(a[0]):
        res.append(a[1])
      else:
        b = dict[a[0]]
        if types.StringType == type(b):
          res.append(b)
        elif types.FunctionType == type(b):
          try:
            c = b(a[0], a[1], dict)
          except:
            c = None
          if types.StringType == type(c):
            res.append(c)
          else:
            res.append(a[1])
  return string.join(res, '')


# This is an interface to the BuiltinWebServer module for automatic 
# installation of template files. We assume the extension .templ for
# such files and we tell the web server to look for such template 
# xxx.templ if a requested xxx.html file is not available.
# For producing a response from a .templ file the dictionary Dict above is
# used.
# Make sure that Dict contains all you need before this install function is 
# used.

import BuiltinWebServer

# A derived WebResponse class. The getresult method is a call of
# FillTemplate. The necessary pre-parsed .templ file and dictionary
# are bound to the object in components .templ and .dict. As header 
# we generate the Content-length, Content-type (stored in component .type)
# and an Expires line (stored in component .expires).
class SimpleTemplateWebResponse(BuiltinWebServer.WebResponse):
  def __init__(self, templ, dict, type='text/html', expires='now'):
    self.templ = templ
    self.dict = dict
    self.type = type
    self.expires = expires
    
  def getresult(self, req, onlyhead):
    str = FillTemplate(self.templ, self.dict)
    header = {'Content-type': self.type,
              'Content-length': len(str),
              'Expires': self.expires}
    return (header, str)
  
# This init function gets the web request and the name of the file with
# the template code as arguments. It assumes that the result becomes
# of a type found via the extension in BuiltinWebServer.TypeDict,
# and that the result expires immediately. 
# Write your own variant of this function if you want another behaviour.
def InitSimpleTemplateWebResponse(req, nam):
  l = ParseFile(nam)
  resp = SimpleTemplateWebResponse(l, Dict)
  ext = os.path.splitext(req.path)[1][1:]
  resp.type = BuiltinWebServer.TypeDict[ext]
  # cache this in BuiltinWebServer.Site, be careful because of threads,
  # note that we hold the lock as shortly as possible
  BuiltinWebServer.SiteLock.acquire()
  BuiltinWebServer.Site[req.path] = resp
  BuiltinWebServer.SiteLock.release()
  

# Now tell the web server to use the init function above for automatic
# installation of html-files via .templ templates.
BuiltinWebServer.AddSpecialExtension('html', 
                                     'templ', InitSimpleTemplateWebResponse)

