#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank L�beck and Max Neunh�ffer

'''This is the script to check OKUSON sheets.'''

import sys,os,time,tempfile,locale,shutil,getopt

tmp = getopt.getopt(sys.argv[1:], 'o:t:hn')
opt = {}
for a in tmp[0]: opt[a[0]] = a[1]
files = tmp[1]

if len(files) == 0 or opt.has_key('-h'):
  print '''
Usage: 
  testsheet [-h] [-n] <a>.bla [<b>.bla ...]

If option -h or no .bla sheet file is given, this help is shown.

If the option -n is given, the PDFTemplateNoTable template (see
Config.xml) is used and interactive exercises are printed as "???".
This is meant for courses with homework exercises only.

All arguments <x>.bla are checked as sheet files.

For a sheet in <x>.bla with name <name> a LaTeX file <x>_<name>.tex 
and a PDF file <x>_<name>.pdf are generated, if no error occurs.
These contain all variants of all questions and on an extra page the
solutions for the MC-like exercises are given.

Error messages hopefully make it easy to correct mistakes. Please first check  
the exercise files needed by these sheets with "testexercise".
'''

import Config         # this automatically determines our home dir
                      # but does not read the configuration file

# Now we can read our configuration file with proper error reporting
# (note that this might fail miserably):

Config.ReadConfig()
Config.PostProcessing()    # some postprocessing of configuration data

try:
  locale.setlocale(locale.LC_ALL, '')
except:
  pass

import Exercises
from  WebWorkers import LocalTimeString

from fmTools import Utils, LatexImage, SimpleTemplate
LatexImage.LatexTemplate = Config.conf["LaTeXTemplate"]

tempfile.tempdir = 'tmpsheettest'

if not os.path.exists('tmpsheettest'):
  os.mkdir('tmpsheettest')


print 'Reading all available exercises ...'
for d in Config.conf['ExerciseDirectories']:   
  Exercises.ReadExercisesDirectory(d)

for a in files:
  if not os.path.exists(a):
    print '\nWARNING:  '+a+' does not exist!'
    break
  print '\n\n############  Checking sheet file '+a+' ...'
  
  if not(len(a) >= 4 and a[-4:] == '.bla'):
    print 'ERROR: sheet files must have the extension ".bla".'
    break
  else: 
    fname = a[:-4]

  Exercises.AllSheets = []
  Exercises.ReadSheetsFile(a)
  for sheet in Exercises.AllSheets:
    # produce a PDF sheet with *all* variants of MC-like questions
    # (compare QuerySheet in WebWorkers)
    values = {}
    values['SheetName'] = sheet.name
    values['IdOfPerson'] = 'CHECKING ALL VARIANTS'
    for a in ['CourseName', 'Semester', 'Lecturer', 'ExtraLaTeXHeader']:
      values[a] = Config.conf[a]
    if Config.conf.has_key('ConfigData'):
      for a in Config.conf['ConfigData'].keys():
        values['ConfigData.'+a] = Config.conf['ConfigData'][a]
    values['OpenTo'] = LocalTimeString(sheet.opento, format = Config.conf['DateTimeFormat'])
    if sheet.openfrom:
      values['OpenFrom'] = LocalTimeString(sheet.openfrom, format = Config.conf['DateTimeFormat'])
    else:
      values['OpenFrom'] = ''
    values['CurrentTime'] = LocalTimeString(format = Config.conf['DateTimeFormat'])
    # we add a further page with the solutions
    sol = sheet.AllSolutions().strip()
    values['ExercisesTable'] = sheet.LatexSheetTable('')
    values['ExercisesNoTable'] = sheet.LatexSheetNoTable()
    if len(sol) > 0:
      values['ExercisesTable'] = values['ExercisesTable']+ \
        '\n\\newpage\n\n\\begin{verbatim}\n'+ sol +'\n\\end{verbatim}\n\n'
    latexinput = None
    pdf = None
    if opt.has_key('-n'):
      templ = Config.conf['PDFTemplateNoTable']
    else:
      templ = Config.conf['PDFTemplate']
    try:
      latexinput = SimpleTemplate.FillTemplate(templ, values)
    except:
      print('Cannot produce LaTeX input.')
    if latexinput:
      try:
        pdf = LatexImage.LatexToPDF(latexinput)
      except:
        pdf = None
    if latexinput:
      Utils.FileString(fname+'_'+sheet.name+'.tex',latexinput)
      print 'Wrote LaTeX code to '+fname+'_'+sheet.name+'.tex'
      if pdf:
        Utils.FileString(fname+'_'+sheet.name+'.pdf',pdf)    
        print 'Wrote PDF file to '+fname+'_'+sheet.name+'.pdf'
        shutil.rmtree('tmpsheettest')


