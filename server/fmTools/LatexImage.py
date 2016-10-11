# -*- coding: ISO-8859-1 -*-
# fmTools package                                Frank Lübeck / Max Neunhöffer

"""Translating LaTeX code to .pnm and .png images via LaTeX and ghostscript.
Basic usage:
  t = 'The function $f(x) = x^2$ is not linear.'
  img = LatexToPng(t, width=3, resolution=300)
  ShowImage(img)    # calls xloadimage, which must be available
"""

import sys, os, types, tempfile, shutil
import Utils

tempfile.tempdir = './'

# The following may be overwritten by the user, take care (in particular,
# don't use '%' comment characters!

LatexTemplate = """
\documentclass[german,12pt]{article}

\usepackage[latin1]{inputenc}
\usepackage{babel}
\usepackage{graphicx}
\usepackage{amssymb}
\usepackage{calc}
\usepackage[body={%s-4pt,100in},dvips=true]{geometry}
\\newcommand{\Z}{\mathbb Z}
\\newcommand{\N}{\mathbb N}
\\newcommand{\Q}{\mathbb Q}
\\newcommand{\R}{\mathbb R}
\\newcommand{\C}{\mathbb C}
\\newcommand{\F}{\mathbb F}

%s

\\begin{document}
\pagestyle{empty}
\parindent0pt
\sloppy
%s
\end{document}
"""

def LatexToPnm(text, width = 6.5, resolution = 100, extraheader = '',
               Latexfmt = '', reporterror = Utils.Error, remove = 1):
  '''Convert the LaTeX input in "text" to a pnm file. "width" is in inch
"resolution" in points per inch, it can be an integer or a list
of integers, the result is an image or a list of images accordingly. 
"extraheader" are added in the preamble of the LaTeX source and
"Latexfmt" is added to the the latex command line call. Errors are
reported back via raising an Utils.UtilsError exception and to the user
via Utils.Error.'''

  tmpdir = tempfile.mktemp()
  os.mkdir(tmpdir)
  try:
      name = os.path.join(tmpdir, 'a.tex')
      tex = file(name, 'w')
      tex.write(LatexTemplate % (str(width)+"in", extraheader, text))
      tex.close()
  except:
      msg = "Cannot write temporary latex source file " + name + "."
      reporterror(msg)
      raise Utils.UtilsError, msg
            
  # run latex:
  ret = os.system('cd '+tmpdir+';latex '+Latexfmt+
            ' -interaction=nonstopmode a.tex'+
            ' >/dev/null')
  if ret:
      msg = 'Problem with latex, see '+tmpdir+'/a.tex'
      reporterror(msg)
      raise Utils.UtilsError, msg
      
  # run dvips:
  #ret = os.system('cd '+tmpdir+'; dvips -Pcmz -Pamz -E -q a.dvi -o a.eps')
  ret = os.system('cd '+tmpdir+'; dvips -E -q a.dvi -o a.eps')
  if ret:
      msg = 'Problem with dvips, see '+tmpdir+'/a.dvi'
      reporterror(msg)
      raise Utils.UtilsError, msg

  # Find BoundingBox:
  try:
    f = file(os.path.join(tmpdir, 'a.eps'))
    l = f.readline()
    while l.find('%%BoundingBox') != 0:
      l = f.readline()
    bbox = map(lambda x: int(x), l[15:-1].split())
  except:
    msg = 'Cannot get bounding box, see '+tmpdir+'/a.eps'
    reporterror(msg)
    raise Utils.UtilsError, msg
    
  if type(resolution) == types.IntType:
      resolutions = [resolution]
  else:
      resolutions = resolution
  res = []
  for r in resolutions:
      Utils.FileString(tmpdir+'/b.eps', 
                       str(-bbox[0]+1)+' '+str(-bbox[1]+1)+' translate\n')
      st = 'cd '+tmpdir+'; cat b.eps a.eps | gs -dNOPAUSE -dBATCH '+\
           ' -sDEVICE=pgmraw -r'+str(r)+' -g'+\
           str(int(width*r))+'x'+\
           str(int(1.0*(bbox[3]-bbox[1]+2)/72.0*r))+' '+\
           ' -dTextAlphaBits=4 -sOutputFile=a.pnm -q -';
      try:
	ret = os.system(st)
	if ret: 
	    msg = 'Problems with ghostscript, see '+tmpdir
	    reporterror(msg)
	    raise Utils.UtilsError, msg
      except:
        msg = 'Cannot translate eps to pnm, see '+tmpdir
        reporterror(msg)
        raise Utils.UtilsError, msg
      res.append(Utils.StringFile(os.path.join(tmpdir, 'a.pnm')))

  # if everything went OK:
  if remove:
      try:
          shutil.rmtree(tmpdir)
      except:
          pass   # we ignore problems here

  if type(resolution) == types.IntType:
      return res[0]
  else:
      return res


def LatexToPDF(text, repeat = 2, reporterror = Utils.Error, remove = 1):
  '''Convert the LaTeX input in "text" which must be a complete LaTeX input
file to a PDF file with pdflatex. '''

  tmpdir = tempfile.mktemp()
  os.mkdir(tmpdir)
  try:
      name = os.path.join(tmpdir, 'a.tex')
      Utils.FileString(name, text)
  except:
      msg = "Cannot write temporary latex source file " + name + "."
      reporterror(msg)
      raise Utils.UtilsError, msg
            
  # run latex:
  for i in range(repeat):
    ret = os.system('cd '+tmpdir+
                    ';pdflatex -interaction=nonstopmode a.tex >/dev/null')
  if ret:
      msg = 'Problem with latex, see '+tmpdir+'/a.tex'
      reporterror(msg)
      raise Utils.UtilsError, msg

  try:
      name = os.path.join(tmpdir, 'a.pdf')
      res = Utils.StringFile(name)
  except:
      msg = "Cannot read temporary PDF file " + name + "."
      reporterror(msg)
      raise Utils.UtilsError, msg
      
  if res:
      if remove:
          try:
              shutil.rmtree(tmpdir)
          except:
              pass   # we ignore problems here
      return res
  else:
      return None
  
# This could be done in the Image module, but it seems to ignore a
# compression argument and always compresses with level 1 only.
def PnmToPng(pnmstring, reporterror = Utils.Error):
  '''Convert a pnm file into a png file by piping through "pnmtopng".
"pnmstring" can either be a string or a list of strings. Accordingly,
one png in a string or a list of pngs in strings is returned.'''
  if type(pnmstring) == types.ListType:
      res = []
      for p in pnmstring:
          res.append(PnmToPng(p,reporterror))
      return res
  if type(pnmstring) != types.StringType:
    return pnmstring
  try:
      inp,out = os.popen2('pnmtopng -compression 9 -background white '+
                          '-transparent white', bufsize=len(pnmstring)+1024)
      inp.write(pnmstring)
      inp.close()
      res = out.read()
      out.close()
  except:
      msg = 'Problems during call to "pnmtopng".'
      reporterror(msg)
      raise Utils.UtilsError, msg

  return res

def LatexToPng(text, width = 6.5, resolution = 100, extraheader = '',
             Latexfmt = '', reporterror = Utils.Error, remove = 1):
  '''Convert latex input to png format. Uses "LaTeXToPnm" and "PnmToPng".
The semantics of the arguments is as in LaTeXToPnm. Escpecially "resolution"
can be an integer or a list of integers and the return value is either
one png image or a list of such accordingly.'''
  pnm = LatexToPnm(text, width=width, resolution=resolution,
                   extraheader=extraheader, Latexfmt=Latexfmt,
                   reporterror=reporterror, remove=remove)
  if type(pnm) == types.ListType:
      for p in range(len(pnm)):
          pnm[p] = PnmToPng(pnm[p],reporterror)
  else:
      pnm = PnmToPng(pnm,reporterror)
  return pnm

def ShowImage(imstring):
  '''Show an image using external "xloadimage". Mainly for debugging 
purposes.'''
  inp,out = os.popen2('xloadimage stdin')
  inp.write(imstring)
  out.close()
  inp.close()

def Show(text, res=100, width=8.5):
  '''Convert a LaTeX input to pnm and directly show it using "xloadimage".'''
  res = LatexToPnm(text, resolution=[res], width=width)
  ShowImage(res[0])

