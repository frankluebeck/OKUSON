#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the script to check OKUSON exercises.'''

import sys,os,time,tempfile,shutil,getopt

tmp = getopt.getopt(sys.argv[1:], 'v:h')
opt = {}
for a in tmp[0]: opt[a[0]] = a[1]
if not opt.has_key('-v'):
  opt['-v'] = 'xloadimage'
files = tmp[1]
  
if len(files) == 0 or opt.has_key('-h'):
  print '''
Usage: 
  testexercise [-h] [-v <viewprog>] <file1> [<file2> ...]

If option -h or no filename is given this help is shown.

The arguments <file1>, ... must be names of OKUSON exercise files with
extension .tex or .auf.

The program tries to convert each exercise text piece into an image as it
would be generated for the web version of the exercise in your OKUSON setup.

So, you can check the validity of the TeX code and also detect layout
problems like bad line breaks.

With the -v option you can specify a program <viewprog> that can display
image files in .png format. The default is 'xloadimage'.
'''

if opt.has_key('-h'):
  sys.exit(0)

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data

import Exercises

from fmTools import Utils, LatexImage
LatexImage.LatexTemplate = Config.conf["LaTeXTemplate"]

tempfile.tempdir = 'tmptestimages'

def handletext(t):
  print "\n\n==========================\n"
  if not os.path.exists('tmptestimages'):
    os.mkdir('tmptestimages')
  if not os.path.exists('tmptestimages/100dpi'):
    os.mkdir('tmptestimages/100dpi')
  t.MakeImages('tmptestimages', [100])
  if os.path.exists('tmptestimages/100dpi/'+t.md5sum+'.png'):
    os.system('/bin/sh -c \''+opt['-v']+' tmptestimages/100dpi/*.png\'')
    # remove temp dir
    shutil.rmtree('tmptestimages')
    #os.system('rm -rf tmptestimages')
  else:
    os.system('/bin/sh -c \'less +"/^l\." tmptestimages/@*/a.log\'')

    
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
