#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to check OKUSON exercises.'''

import sys,os,time,tempfile

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data

import Exercises

from Tools import Utils, LatexImage
LatexImage.LatexTemplate = Config.conf["LaTeXTemplate"]

tempfile.tempdir = 'tmptestimages'

files = sys.argv[1:]

def handletext(t):
  print "\n\n==========================\n"
  if not os.path.exists('tmptestimages'):
    os.mkdir('tmptestimages')
  if not os.path.exists('tmptestimages/100dpi'):
    os.mkdir('tmptestimages/100dpi')
  t.MakeImages('tmptestimages', [100])
  if os.path.exists('tmptestimages/100dpi/'+t.md5sum+'.png'):
    os.system('/bin/sh -c \'xloadimage tmptestimages/100dpi/*.png\'')
  else:
    os.system('/bin/sh -c \'less +"/^l\." tmptestimages/@*/a.log\'')
  # remove temp dir
  os.system('rm -rf tmptestimages')

    
for a in files:
  if not os.path.exists(a):
    print '\nWARNING:  '+a+' does not exist!'
    break
  print '\n\n############  Checking file '+a+' ...'
  if len(a) >= 4 and a[-4:] == '.tex':
    # case of LaTeX code for conventional exercise
    t = Exercises.TeXText(Utils.StringFile(a), a, (1,0,-1,-1),
        width = Config.conf['WidthOfExerciseTextsHTML'])
    handletext(t)

  elif len(a) >= 4 and a[-4:] == '.auf':
    # case of OKUSON MC-like exercise
    Exercises.AllTexts = []
    Exercises.ReadExercisesFile(a)
    for t in Exercises.AllTexts:
      handletext(t)
  else:
    print 'WARNING: can only check .tex and .auf files.'
