#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This a universal sorting and selecting script for line-oriented data.
Call without arguments for instructions.'''

import string,sys,getopt,types,re

if len(sys.argv) == 1:
    print """
Usage: sortselect.py [-t DELIMITER] [-f FIELDS] {SELECTSPECS} {SORTSPECS}
       DELIMITER: field delimiter for input lines
       FIELDS:    fields to consider (like "cut"):
                    comma-separated list of ranges, where ranges can be:
                    N   : one field (zero based)
                    M:  : all fields from the Mth on (including the Mth)
                    :N  : all fields up to the Nth (not including the Nth)
                    M:N : all fields from the Mth to the Nth (including the
                          Mth but not the Nth)
                    (default is all fields in their natural order)
       SELECTSPECS: A selecting specifier can be one of the following:
                    (N always stands for a field number in the original
                     lines and XYZ for a string)
                    N==XYZ  specifies that the entry in field number N must 
                            be equal to the string XYZ
                    N!=XYZ  ... must not be equal to XYZ
                    N~~XYZ  ... must match the regexp XYZ
                    N>=XYZ  ... must be (string-) greater or equal to XYZ
                    N>-XYZ  ... must be numerically greater or equal to XYZ
                    N<=XYZ  ... must be (string-) less or equal to XYZ
                    N<-XYZ  ... must be numerically less or equal to XYZ
                    N>>XYZ  ... must be (string-) greater than XYZ
                    N>+XYU  ... must be numerically greater than XYZ
                    N<<XYZ  ... must be (string-) less than XYZ
                    N<+XYZ  ... must be numerically less than XYZ
                    If more than one selecting specifier is given, a logical
                    "or" is performed, so only one of them must be fulfilled.
                    Beware of input-/output redirection of your shell!
       SORTSPECS:   A sorting specifier is either n+N n-N or s+N or s-N where 
                    N is replaced by a (zero based) field number (in the
                    output selection of fields), a leading 
                    "n+" specifies numerically ascending sorting, a leading
                    "n-" specifies numerically descending sorting, a leading
                    "s+" specifies string ascending sorting, a leading
                    "s-" specifies string descending sorting.
                    If more than one sort specifier is given, the first takes
                    precedence and the second is only considered for equal
                    values of the first sort specifier.
       Comment: All field numbers in sorting specifiers are within the
                    list of fields specified with -f.
"""
    sys.exit(0)

optlist,args = getopt.getopt(sys.argv[1:],'t:f:')

# defaults:
delim = ':'
fieldsst = ""   # this means all fields
fields = None

for (k,v) in optlist:
    if   k == "-t": delim = v
    elif k == "-f":
        fieldsst = v
        l = string.split(fieldsst,",")
        fields = []
        for s in l:
            p = string.find(s,":")
            if p == -1:
                fields.append(int(s))
            elif p == 0:
                fields.extend(range(int(s[1:])))
            elif p == len(s):
                fields.append( (int(s[:-1]),None) )
            else:
                fields.extend( range(int(s[:p]),int(s[p+1:])) )


# Now we parse the arguments for selecting and sorting specifications:

allcomparers = ["==","!=","~~",">=",">-","<=","<-",">>",">+","<<","<+"]
allnumcomparers = [">-","<-",">+","<+"]
allsorters = ["n+","n-","s+","s-"]

selectspecs = []
sortspecs = []

for x in args:
    if x[:2] in allsorters:
        sortspecs.append( (x[:2],int(x[2:])) )
    else:
        N = 0
        i = 0
        while i < len(x) and x[i] >= '0' and x[i] <= '9':
            N = N * 10 + int(x[i])
            i += 1
        c = x[i:i+2]
        if c in allcomparers:
            if c == '~~':
                selectspecs.append( (N,c,re.compile(x[i+2:])) )
            elif c in allnumcomparers:
                selectspecs.append( (N,c,float(x[i+2:])) )
            else:
                selectspecs.append( (N,c,x[i+2:]) )

# First select the lines to survive:

linelistin = sys.stdin.readlines()
linelist = []
for l in linelistin:
    # Maybe we skip the line:
    ls = l.strip()
    if ls == '': continue
    if ls[:1] == '#': continue
    
    # Now we split it:
    ll = ls.split(delim)
    
    # Now we select:
    if len(selectspecs) == 0:
        takeit = 1
    else:
        takeit = 0
        for s in selectspecs:
            if   s[1] == '==':
                if ll[s[0]] == s[2]: 
                    takeit = 1
                    break
            elif s[1] == '!=':
                if ll[s[0]] != s[2]: 
                    takeit = 1
                    break
            elif s[1] == '>=':
                if ll[s[0]] >= s[2]:
                    takeit = 1
                    break
            elif s[1] == '<=':
                if ll[s[0]] <= s[2]:
                    takeit = 1
                    break
            elif s[1] == '>>':
                if ll[s[0]] > s[2]:
                    takeit = 1
                    break
            elif s[1] == '<<':
                if ll[s[0]] < s[2]:
                    takeit = 1
                    break
            elif s[1] == '>-':
                if float(ll[s[0]]) >= s[2]:
                    takeit = 1
                    break
            elif s[1] == '<-':
                if float(ll[s[0]]) <= s[2]:
                    takeit = 1
                    break
            elif s[1] == '>+':
                if float(ll[s[0]]) > s[2]:
                    takeit = 1
                    break
            elif s[1] == '<+':
                if float(ll[s[0]]) >= s[2]:
                    takeit = 1
                    break
            elif s[1] == '~~':
                if s[2].search(ll[s[0]]): 
                    takeit = 1
                    break
            
    if not(takeit): continue
    
    # Now we collect the fields of interest:
    if fields == None:
        lll = ll
    else:
        lll = []
        for f in fields:
            if type(f) == types.IntType:
                if f >= len(ll):
                    sys.stderr.write("Warning: No field "+str(f)+
                                     " in line:\n"+l)
                    continue
                lll.append(ll[f])
            else:   # this must be a tuple with None in second position
                if f[0] >= len(ll):
                    sys.stderr.write("Warning: No field "+str(f[0])+
                                     " in line:\n"+l)
                    continue
                lll.extend(ll[f[0]:])
    linelist.append(lll)

# Now sort survivors:
def universalsort(a,b):
    i = 0
    while i < len(sortspecs):
        (s,n) = sortspecs[i]
        if s == 'n+':
            c = cmp(float(a[n]),float(b[n]))
            if c != 0: return c
        elif s == 'n-':
            c = cmp(float(b[n]),float(a[n]))
            if c != 0: return c
        elif s == 's+':
            c = cmp(a[n],b[n])
            if c != 0: return c
        else:  # can only be "s-":
            c = cmp(b[n],a[n])
            if c != 0: return c
        i += 1
    return 0

linelist.sort(universalsort)

# Then output it:
for lll in linelist:
    print string.join(lll,delim)


