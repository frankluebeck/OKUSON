#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2010 by  Frank Lübeck  and   Max Neunhöffer
#

from startNOSERVER import *

if len(sys.argv) < 6:
  print('''
Usage:  
       ExportToMoodle.py catname sheetnr fromseed nrvariants fname [PDFBaseURL]

Arguments are:
   catname       name of a question category in Moodle (e.g. "sheet1")
   sheetnr       number of sheet in OKUSON  (e.g.   1)
   fromseed      first id for variants (e.g. 100000)
   nrvariants    number of generated Moodle exercises  (e.g. 50)
   fname         name of generated Moodle-XML file (e.g. "variants1.xml")
   PDFBaseURL    optional: if given, pdf-versions of sheets are
                 generated and links with this base URL are added at
                 top of the exercises

The file <fname> can be imported as questions in Moodle, it is in 
Moodle-XML format.
If PDF files were generated, the content of the 'pdfs' subdirectory
must be copied to the given base URL.

''')
  sys.exit(1);

if len(sys.argv) == 7:
  pdfurl = sys.argv[6]
else:
  pdfurl = None

try:
  Exercises.MoodleExport(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], PDFBaseURL=pdfurl)
except:
  print('Something went wrong!')

