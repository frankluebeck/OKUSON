# -*- coding: ISO-8859-1 -*-
# BibTeXUtils.py                                                 Frank Lübeck
# 
# This file contains utilities to read in a BibXML-database and to generate
# strings for BibTeX and BibXML versions of the entries.
# 
#  $Id: BibTeXUtils.py,v 1.1 2003/09/23 08:14:40 neunhoef Exp $

import types, string, re, popen2, os

# for XML parsing
import XMLRewrite, Utils
from Utils import NormalizedWhitespace


# This makes a python dictionary from the XML tree of an <entry> element.
# The type of the entry (book, phdthesis, , ...) is in res['bibtype'] and the
# access key is in res['id'], all other keys are what we use in BibTeX
# (res['author'], res['title'] and so on.
def DictEntry(entry):
  # string "bibtex:"
  def b(s):
    return s[7:].encode('latin1')
  d = {}
  i = 0
  while type(entry[2][i]) in types.StringTypes:
    i += 1
  e = entry[2][i]
  d['bibtype'] = b(e[0])
  d['id'] = entry[1]['id'].encode('latin1')
  for i in e[2]:
    if not type(i) in types.StringTypes and len(i[2])>0:
      d[b(i[0]).encode('latin1')] = i[2][0].encode('latin1')
  return d



#  the next three functions are essentially copied from unflatten.py in the
#  bib2xml utility (Johannes Henkel jhenkel@jhenkel.de, GPL code)
# (they are used for normalizing names of authors and editors in Bib
# entries)
def namelex(str):
	"A lexer for the parsePersons method."
	result = []
	pos=0;
	while pos<len(str):
		if str[pos] in string.whitespace:
			pos = pos + 1
		elif str[pos]==',':
			result.append(',')
			pos = pos + 1
		else:
			part = ""
			brackets = 0
			while 1:
				assert(brackets>=0)
				if pos >= len(str):
					break
				elif str[pos]=='{':
					part = part + "{"
					brackets = brackets + 1
					pos = pos + 1					
				elif str[pos]=='}':
					part = part + "}"
					brackets = brackets - 1
					pos = pos + 1
				elif pos+1<len(str) and str[pos:pos+1]=="\{":
					part = part + "\{"
					pos = pos+2
				elif pos+1<len(str) and str[pos:pos+1]=="\}":
					part = part + "\}"
					pos = pos+2
				elif str[pos]==',':
					if brackets>0:
						part = part + ","
						pos = pos + 1
					else:
						break
				elif str[pos] in string.whitespace:
					if brackets>0:
						part = part + " "
						pos = pos + 1
					else:
						break
				else:
					part = part + str[pos]
					pos = pos + 1
			if string.lower(part)=="and":
				result.append("and")
			elif string.lower(part)=="others":
				result.append("Others") # so this will be detecetd as a last name ... ;-)
			else: result.append(part)
	return result


class Person:
	"Models a bibtex name"
	def __init__(self, first, von, last, junior):
		self.first=first;
		self.von=von;
		self.last=last;
		self.junior=junior;
                if '.' in first:
                  self.firstabbrev=first
                else:
                  a=[]
                  for i in string.split(first):
                    a.append(i[0]+'.')
                  self.firstabbrev=string.join(a, ' ')
	def getFirst(self):
		return self.first;
	def getFirstAbbrev(self):
                return self.firstabbrev;
        def getVon(self):
		return self.von;
	def getLast(self):
		return self.last;
	def getJunior(self):
		return self.junior;
	def __repr__(self):
		return "(first: "+self.first+", firstabbrev: "+self.firstabbrev+", von: "+self.von+\
                         ", last: "+self.last+", junior: "+self.junior+")"
  
def parsePersons(str):
	"returns a list of name objects."
	lexed = namelex(str)
	ast1 = []
	while lexed.count("and")>0:
		andIndex = lexed.index("and")
		ast1.append(lexed[0:andIndex])
		del lexed[0:andIndex+1]
	ast1.append(lexed)
	ast = []
	for name in ast1:
		namelist = []
		while name.count(",")>0:
			commaIndex = name.index(",")
			namelist.append(name[0:commaIndex])
			del name[0:commaIndex+1]
		namelist.append(name)
		ast.append(namelist)
	result = []
	for name in ast:
		assert len(name)>0 and len(name)<=3
		first=von=last=junior=""
		partlist = name[0]
		lastitem = partlist.pop()
		if len(name)<3 and (lastitem=="Jr." or lastitem=="Jr"):
			junior=lastitem
			lastitem = partlist.pop()
		last=lastitem
		vonBegin=len(partlist)
		while vonBegin>0 and partlist[vonBegin-1][0] in string.lowercase:
			vonBegin = vonBegin - 1
		von = string.join(partlist[vonBegin:len(partlist)])
		del partlist[vonBegin: len(partlist)]
		if len(name)==1: first = string.join(partlist)
		if len(name)==3: von = name[1]
		if len(name)==2:
			partlist = name[1]
		if len(name)==3:
			partlist = name[2]
		if len(name)==2 or len(name)==3:
			vonBegin = len(partlist)
			while vonBegin>0 and partlist[vonBegin-1][0] in string.lowercase:
				vonBegin = vonBegin-1
			von = string.join(partlist[vonBegin:len(partlist)])+von
			del partlist[vonBegin: len(partlist)]
			first = string.join(partlist)
		result.append(Person(first,von,last,junior))
                
	return result
#####################################################


# using the utilities above, we can normalize author and editor tags
def normedNamesString(s):
  l = parsePersons(s)
  res = []
  for a in l:
    b = [a.getFirstAbbrev()]
    if len(a.getVon()) > 0:
      b.append(a.getVon())
    b.append(a.getLast())
    if len(a.getJunior()) > 0:
      b.append(a.getJunior())
    res.append(string.join(b, ' '))
  return string.join(res, ' and ')

# these use the dictionaries
StandardBibTeXOrder =  ['author','editor','title','subtitle','publisher',\
                        'series','volume','number','edition','type','school',\
                        'year','address','ldfm','buchstabe']

# translate a Bib entry into a string for a BibTeX file
def BibTeXString(d):
  res = ['@'+d['bibtype']+ '{ ' + d['id'] + ',']
  inner = []
  fill = '                         '
  for n in StandardBibTeXOrder:
    if d.has_key(n):
      if len(NormalizedWhitespace(d[n])) > 0:
        if n in ['author','editor']:
          inner.append('  '+n+' = '+fill[0:16-len(n)]+'{'+normedNamesString(d[n])+'}')
        else:
          inner.append('  '+n+' = '+fill[0:16-len(n)]+'{'+d[n]+'}')
  for n in d.keys():
    if not n in StandardBibTeXOrder and not n in ['bibtype', 'id']:
      inner.append('  '+n+' = '+fill[0:16-len(n)]+'{'+d[n]+'}')
  res.append(string.join(inner, ',\n'))
  res.append("}\n")
  return string.join(res, "\n")

# (re)translate a Bib entry into a string for a BibXML file
def BibTeXXMLString(d):
  res = ['<bibtex:entry id="' + d['id'] + '">\n  <bibtex:' + d['bibtype'] + '>\n']
  for n in StandardBibTeXOrder:
    if d.has_key(n):
      if len(NormalizedWhitespace(d[n])) > 0:
        if n in ['author','editor']:
          try:
            nnam = normedNamesString(d[n])
          except:
            nnam = d[n]
          res.append('    <bibtex:' + n + '>' + nnam + '</bibtex:' + n + '>\n')
          if nnam != d[n]:
            res.append('    <bibtex:orig' + n + '>' + d[n] + '</bibtex:orig' + n + '>\n')
        else:
          res.append('    <bibtex:' + n + '>' + d[n] + '</bibtex:' + n + '>\n')
  for n in d.keys():
    if not n in StandardBibTeXOrder and not n in ['bibtype', 'id']:
      res.append('    <bibtex:' + n + '>' + d[n] + '</bibtex:' + n + '>\n')
  res.append("  </bibtex:" + d['bibtype'] + '>\n</bibtex:entry>\n\n')
  return string.join(res, "")

# a string, describing a Bib entry for use in a HTML document
def BibHTMLString(d, LDFM=0):
  def delbr(s):
    return string.translate(s, string.maketrans('',''), '{}')
  res = [];
  if d.has_key('mrnumber'):
    res.append('<a href="http://www.ams.org/mathscinet-getitem?mr=' + d['mrnumber'] + '">' + d['id'] + '</a> ')
  if d.has_key('author'):
    res.append('<b>' + string.replace(normedNamesString(d['author']), ' and', ',') + '</b> ')
  if d.has_key('editor'):
    res.append('(' + string.replace(normedNamesString(d['editor']), ' and', ',') + ', Ed.)')
  if d.has_key('title'):
    if d.has_key('author') or d.has_key('editor'):
      res.append(', ')
    res.append('<i>' + delbr(d['title']) + '</i>')
  if d.has_key('booktitle'):
    if d['bibtype'] in ['inproceedings', 'incollection']:
      res.append(' in ')
    res.append(', <i>' + delbr(d['booktitle']) + '</i>')
  if d.has_key('subtitle'):
    res.append(', <i> -- ' + delbr(d['subtitle']) + '</i>')
  for n in ['journal', 'organization', 'publisher', 'school', 'edition', 'series', 'volume', 'number', 'address']:
    if d.has_key(n):
      res.append(',  ' + d[n])
  if d.has_key('year'):
    res.append(' (' + d['year'] + ')')
  if d.has_key('pages'):
    res.append(', p. ' + d['pages'])
  if d.has_key('chapter'):
    res.append(', Chapter ' + d['chapter'])
  if d.has_key('note'):
    res.append(', <br />(' + d['note'] + ')')
  if d.has_key('notes'):
    res.append(', <br />(' + d['notes'] + ')')
  if LDFM:
    if d.has_key('ldfm'):
      res.append(', LDfM Nr.' + d['ldfm'])
    if d.has_key('buchstabe'):
       res.append(', (einsortiert unter ' + d['buchstabe'] + ')')
  res.append('\n')
  return string.join(res, '')


# before searching in the database we apply certain transformations to the
# text we search and the query strings: 
# - translate german umlaut and ß in the standard way
# - translate non-ascii letters to ascii approximation
# - translate non-(letters or decimals) to whitespace
# - normalize the whitespace

from translist import translist

# for normalzing strings as above
def NormalizedSearchString(str):
  x = string.translate(str, string.maketrans('',''),'{}')
  x = string.replace(x, '\xe4', 'ae')
  x = string.replace(x, '\xf6', 'oe')
  x = string.replace(x, '\xfc', 'ue')
  x = string.replace(x, '\xc4', 'ae')
  x = string.replace(x, '\xd6', 'oe')
  x = string.replace(x, '\xdc', 'ue')
  x = string.replace(x, '\xdf', 'ss')
  return NormalizedWhitespace(string.translate(x, translist))

# generates a search string for a Bib entry
def SearchString(d):
  res = []
  for n in d.keys():
    res.append(NormalizedSearchString(d[n]))
  return string.join(res, ' ')

# a global list for collecting Bib entries with the following function,
# several files can be read
BibEntries = []
def AddBibEntries(filename):
  # the [0] because the default Parser setting is ReturnList == 1  
  t = XMLRewrite.ParseFile(filename)[0]
  for e in t[2]:
    if not type(e) in types.StringTypes:
      BibEntries.append(DictEntry(e));
      
# produce one line for each Bib entry that can be searched by agrep
# each line contains the number of the entry in BibEntries, so that the
# matching numbers are easily recovered from the agrep result
BibEntriesSearchString = ''
def MakeAgrepInput():
  global BibEntriesSearchString
  res = []
  fill = "################"
  for i in range(len(BibEntries)):  
    res.append('####'+str(i))
    res.append(fill[0:12-len(res[-1])])
    res.append(SearchString(BibEntries[i]))
    res.append('\n')
  BibEntriesSearchString = string.join(res, '')

# the input for agrep can be big, so we feed it with a separate thread to
# avoid locking because of overrun buffers for the result
import threading
def WriteThread(tofile, str):
  tofile.write(str)
  tofile.close()

# this calls the external program agrep
def FindEntriesWithAgrep(search, fuzzy=0):
  search = NormalizedSearchString(search)
  (o,i) = popen2.popen2('agrep -' + str(fuzzy) + ' -e "' + search + '"')
  threading.Thread(target = WriteThread, args = (i, BibEntriesSearchString)).start()
  res = []
  res = o.read()
  res = string.split(res, '\n')
  num = []
  for a in res:
    try: 
      b = string.replace(a[4:12], '#', '')  
      n = int(b)
      num.append(n)
    except:
      pass
  return num

# a utility for LDfM, calls a script for printing a reference card for new
# a new book
def BibMachKarte(d):
  if d.has_key('author'):
    nam = d['author']
  else:
    nam = d['editor']
  nam = string.replace(nam, ' and', ',')
  os.system('./machkarte "' + nam + '" "' + d['ldfm'] + '" "' + d['title'] + '" "' + d['publisher'] + '" "' + d['year']  + '"')

