#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2003 by  Frank Lübeck  and   Max Neunhöffer
#
# This script is part of OKUSON.
#
# It distributes people into tutoring groups, according to their wishes.
# Input is an ASCII file with one line for each person in the format:
#  id:last name:first name:semester:studiengang:wishlist:pdata1-9
# where wishlist is a list of id's of people, separated by commas,
# and pdata1-9 are the 9 extra personal data fields, separated by :
# characters.
# Such a file is exported by OKUSON with the menu point 
#  "Export people for tutoring groups".
# Empty lines indicate the separation of parts, like for example if you
# export "separated by studiengang".
# Lines beginning with a "#" sign are ignored as comments.
# 
# Command line arguments are as follows:
#  inputfile outputfile numberofgroups {numberofgroups}
# For each part (separated by empty lines) we need a number of groups.
#
# Output is in the same format as above, where groups are separated by
# empty lines. Some comments are added.

import sys,os,string

if len(sys.argv) < 4:
    print """
Usage: distribute.py INPUTFILE OUTPUTFILE NUMBEROFGROUPS {NUMBEROFGROUPS}
       where NUMBEROFGROUPS is the number of groups to be formed.
       There must be one "NUMBEROFGROUPS" for each part in the input.
       Parts in the input are separated by empty lines.
       Format of input file (and output file):
         id:last name:first name:semester:studiengang:wishlist:pdata1-9
       where wishlist is a comma separated list of ids.
"""
    sys.exit(0)

# The following function basically does all the work for one part:

def HandleOnePart(input,output,nr):
    '''Reads in one part of the input (until the first empty line or end
of file is found) and distributes people into nr groups, according to their
wishes.'''
    people = {}
    done = 0
    while not(done):
        line = input.readline()
        if not(line):
            done = 2   # end of file, part is over
            break
        line = line.strip()
        if not(line):
            done = 1   # empty line, part is over
            break
        if line[0] == '#':   # a comment, we ignore line
            continue
        p = line.split(':')
        if len(p) < 7:
            print "Illegal format, offending line:\n  "+line+"\nignoring..."
            continue
        p[5] = p[5].split(',')
        people[p[0]] = p
    if len(people) == 0: return done
    # Now throw out wishes not in this part:
    for k,p in people.iteritems():
        i = 0
        while i < len(p[5]):
            if not(people.has_key(p[5][i])):
                del p[5][i]
            else:
                i += 1
    # We start by calculating finest equivalence class distribution such that
    # all wishes to be in the same equivalence class are fulfilled. This is
    # the symmetric and transitive closure of the relation given by the wishes.
    groups = {}
    for k in people.iterkeys():
        groups[k] = [1,k]
    for k,p in people.iteritems():
        for k2 in p[5]:
            if id(groups[k]) != id(groups[k2]):   # different groups up to now
                groups[k].extend(groups[k2][1:])
                groups[k][0] += groups[k2][0]   # add lengths
                for k3 in groups[k2][1:]: groups[k3] = groups[k]
    # We now have to collect the different groups:
    grouplist = []
    ids = {}
    for k,v in groups.iteritems():
        if not(ids.has_key(id(v))):   # we did not see this group
            ids[id(v)] = 1
            grouplist.append(v)
    # Write out an intermediate result:
    print 'New part:'
    print 'Found',len(grouplist),'equivalence classes in generated '\
          'equivalence relation.'
    print 'Maximal length of one class:',max(map(lambda x:x[0],grouplist))
    # Now we have to reduce this to nr groups. We do this by sorting
    # the list of equivalence classes by length and iteratively put the
    # largest into the smallest group so far.
    result = map(lambda x: [0],range(nr))
    cmplen = lambda a,b: cmp(a[0],b[0])
    cmplenrev = lambda a,b: -cmp(a[0],b[0])
    grouplist.sort(cmplenrev)
    for g in grouplist:
        result[0].append(None)
        result[0].extend(g[1:])
        result[0][0] += g[0]     # add lengths
        result.sort(cmplen)
    # Print out result:
    sys.stdout.write("Formed "+str(nr)+" groups with lengths:\n  ")
    for i in range(nr):
        sys.stdout.write(str(result[i][0])+' ')
    sys.stdout.write('\n')
    # Output result:
    for r in result:
        output.write('# New group, '+str(r[0])+' members:\n')
        for k in r[1:]:
            if k == None:
                output.write('#--- delimiter of equivalence class\n')
            else:
                p = people[k]
                output.write(string.join(p[:5],':')+':'+string.join(p[5],',')+
                             ':'+p[6]+'\n')
        output.write('\n')
             
    return done

input = file(sys.argv[1],"r")
output = file(sys.argv[2],"w")
nrs = []
for i in range(3,len(sys.argv)):
    nrs.append(int(sys.argv[i]))

partnr = 0
while HandleOnePart(input,output,nrs[partnr]) < 2:
    partnr += 1
    if partnr >= len(nrs):
        partnr = len(nrs)-1

