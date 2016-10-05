# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

"""So far (calling python in ..):
   from fmTools import *
   import Exercises
   Exercises.ReadExercisesDirectory('/home/beteigeuze/luebeck/la2001/LAII/aufgaben')
   Exercises.CreateAllImages('images')
"""

CVS = '$Id: Exercises.py 558 2007-04-16 12:35:07Z luebeck $'

import string, cStringIO, types, re, sys, os, types, glob, traceback, \
       pyRXPU, md5, time

import Config,Data
from fmTools import Utils,LatexImage,SimpleRand,AsciiData,XMLRewrite

# the data structure of sheets and exercises is described in the following 
# class definitions:

##  declaration of 
#C  TeXText  . . . . . . . . . . . . class to hold one text written in TeX
#C  Sheet  . . . . . . . . . . . . . class to hold an exercise sheet
#C  Exercise . . . . . . . . . . . . class to hold an interactive exercise
#C  Question . . . . . . . . . . . . class to hold a question of such exercise
##  
class TeXText(Utils.WithNiceRepr):
    text = ""        # the actual text as TeX input
    filename = ""    # name of file containing the text
    position = (0,0,0,0)  # position as the XML parser gives them, a 4-tuple
    md5sum = ""      # a hexadecimal md5sum string for .text, used as 
                     # filename for images
    def __init__(self,text,filename,position,width=5):
        self.text = text
        self.filename = filename
        self.position = position
        self.width = width
        self.md5sum = md5.new(self.text).hexdigest()

    def MakeImages(self,imagedir,resolutions,remove=1):
        '''This method calculates images for all resolutions in "resolutions"
and stores them under the corresponding subdirectories of "imagedir" in files
with the md5sum as file name. Errors are reported to the user but otherwise
ignored. We assume that for each resolution X there is already a subdirectory
"Xdpi" in the "imagedir" directory.'''
        todo = 0
        for i in range(len(resolutions)):
            fname = os.path.join(imagedir,str(resolutions[i])+"dpi",
                                 self.md5sum+".png")
            if not(os.path.exists(fname)):
                todo = 1
        if todo:
            try:
              imgs = LatexImage.LatexToPng(self.text,width=self.width,
                         resolution=resolutions,
                         extraheader=Config.conf['ExtraLaTeXHeader'],
                         remove=remove)
            except:
              Utils.Error('Offending LaTeX source comes from "'+self.filename+
                          '" line '+str(self.position[0])+'.',prefix='')
              #traceback.print_exc()
              return
            try:
              for i in range(len(resolutions)):
                  Utils.FileString(os.path.join(imagedir,
                                                str(resolutions[i])+"dpi",
                                                self.md5sum+".png"),imgs[i])
            except:
              return
            Utils.Error('Generated image for file '+
                        os.path.basename(self.filename)+
                        ' at line '+str(self.position[0])+'\n  Text: '+
                        self.text.strip()[:30]+' ...',
                        prefix='Info:')

        
def CleanQuotes(st):
    return st.replace('"','&quot;')

def CleanString(s):
    '''Cleans a string for input in an alt-attributes of images.'''
    s = string.strip(s)           # remove leading and trailing whitespace
    s = string.replace(s,'"','')  # remove quotes
    s = string.replace(s,'&','&amp;')
    s = string.replace(s,'<','&lt;')
    s = string.replace(s,'>','&gt;')
    return s

def CleanStringTeXComments(s):
    '''Strips TeX comments and cleans afterwards for alt-attributes.'''
    # split in lines
    sp = string.split(s, '\n')
    # remove lines starting with '%'
    sp = filter(lambda z: len(z) == 0 or z[0] != '%', sp)
    # remove in each line everything after the first '%' without a previous '\'
    for i in range(len(sp)):
      pos = string.find(sp[i], '%')
      while pos > 0 and sp[i][pos-1] == '\\':
        pos = string.find(sp[i], '%', pos+1)
      if pos >= 0:
        sp[i] = sp[i][:pos]
    # concatenate and clean XML characters
    return string.join(sp, '\n')

class Sheet(Utils.WithNiceRepr):
    openfrom = None  # time when sheet is published (None == -infinity)
    opento = 0       # time until sheet is open in secs since epoche
    counts = 1       # if non-zero, the sheet counts for the Schein
    nr = 0           # a number for sorting the sheets of this course
    name = ""        # a name of the sheet, the default is  str(nr)
    first = 1        # number of first exercise on this sheet
                     # the following four lists have equal length:
    maxhomescore=-1  # maximal number of of points in homework
    starhomescore=0  # maximal number of points for optional homework exercises
    starmcscore=0    # maximal number of points for optional mc exercises
    list = []        # sequence of TeXTexts (for texts between exercises) or 
                     # pairs of TeXTexts (for written exercises) or 
                     # Exercise objects
    exnr = []        # None for each TeXText in "list", and a number otherwise
    order = []       # 'p' for permuted and 'f' for fixed for each 
                     # Exercise object, otherwise None
    nrquestions = [] # Number of questions for each Exercise object
    filename = ""    # name of the file where this sheet comes from
    position = ()    # position of element in file
    magic = 1        # number for initializing the pseudo random number
                     # generator
    def __init__(self):        # avoid accidental use of default lists above
        self.list = []
        self.exnr = []
        self.order = []
        self.nrquestions = []
    
    def IsClosed(self):
        '''This function returns 1 if the sheet is already closed now. This
           is done by comparing the current time with the time in the opento
           component.'''
        if time.time() > self.opento: return 1
        else:                         return 0

    def MaxMCScore(self):
        result = 0
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,Exercise):
                nr = 0
                j = 0
                while nr < self.nrquestions[i] and j < len(o.list):
                    if isinstance(o.list[j],Question):
                        result += o.list[j].scorecorrect
                        nr += 1
                    j += 1
                # Note that this provides nonsense, if nrquestions in the
                # sheet is smaller than the actual number of questions 
                # in the exercise and not all questions have the same 
                # scorecorrect! It lies in the responsibility of the user
                # to get this right.
        return result   

    def ChooserFunction(self,seed):
        '''Uses a pseudo random generator to choose which questions in which
order in which variation is taken. seed will usually be a Matrikel number
or some other number derived from the participant's "id". Returns a list
with as many entries as self.list, each entry corresponding to an Exercise
instance e is a list l. Such a list l is a list of pairs, the first entry
being an index in e.list, the second a number of a variant in the question
in e.list at that index. This is used whenever the special version of
a sheet for one certain student is needed.'''

        result = []

        # special case seed=='' should give *all* variants
        if seed == '':
            for i in range(len(self.list)):
                o = self.list[i]
                if isinstance(o,Exercise):
                    l = []
                    ll = []
                    for j in range(len(o.list)):
                        q = o.list[j]
                        if isinstance(q,Question):
                            l.append(j)
                    for k in range(len(l)):
                        ll.append([None,None])
                        for kk in range(o.list[l[k]].nrvariants):
                            ll.append([l[k], kk])
                    result.append(ll)
                else:
                    result.append(None)
            return result       
        
        rand = SimpleRand.RandObj(
                    seed = int((long(self.magic)*seed)% (pow(2,30)+1)))
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,Exercise):
                # Now we collect all questions:
                l = []
                for j in range(len(o.list)):
                    q = o.list[j]
                    if isinstance(q,Question):
                        l.append(j)
                # Now we reduce the number of questions:
                while len(l) > self.nrquestions[i]:
                    n = rand.nextequaldist(len(l))
                    l = l[:n]+l[n+1:]
                # Now we shuffle them if allowed:
                if self.order[i] == 'p': rand.ShuffleList(l)
                # Now we choose a variant randomly:
                for k in range(len(l)):
                    l[k] = [l[k],rand.nextequaldist(o.list[l[k]].nrvariants)]
                # Save the list of pairs:
                result.append(l)
            else:
                result.append(None)
        return result

    def WebSheetTable(self,resolution,seed,f,mcresult):
        '''Creates an xhtml table for the web version in resolution 
"resolution" of the sheet with seed "seed" and writes the result to the
Python file object f. f is *not* closed in the end. "mcresult" must be
either None or equal to the latest mcresult of the participant as found
in the database. In this case it is an instance of the class MCResult in
Data.py. "seed" must be a unique integer that is determined by the "id"
of the participant. Returns 0 if all went well and a negative error code
otherwise.'''
        imagesdir = os.path.join('images',str(resolution)+'dpi')

        choice = self.ChooserFunction(seed)

        # are we before or after the closing date?
        closed = self.IsClosed()

        if mcresult != None:
            sub = AsciiData.TupleLine(mcresult.submission,delimiter='|')
            marks = mcresult.marks
        else:
            sub = None
            marks = None

        counter = 0   # we count questions to index sub and marks

        # Write Table heading:
        # relative widths of columns
        widths = [ 
                  int(100.0*(Config.conf['WidthOfSheetsHTML'] - 
                      Config.conf['WidthOfExerciseTextsHTML']) /
                      Config.conf['WidthOfSheetsHTML']),
                  int(100.0*Config.conf['WidthOfQuestionsHTML'] /
                      Config.conf['WidthOfSheetsHTML']) ]
        widths.append(100-widths[0]-widths[1])
        
        f.write('<table border="1">\n')
        f.write('<colgroup>\n'
                '  <col width="'+str(widths[0])+'%" />\n'
                '  <col width="'+str(widths[1])+'%" />\n'
                '  <col width="'+str(widths[2])+'%" />\n'
                '</colgroup>\n')

        # walk through the list:
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,TeXText):
                f.write('<tr><td colspan="3">')
                f.write('<img src="%s.png" alt="%s" /></td>\n</tr>\n'%
                        (os.path.join(imagesdir,o.md5sum),
                         CleanString(CleanStringTeXComments(o.text))))
            elif type(o) == types.TupleType and isinstance(o[0],TeXText):
                # a conventional exercise
                if closed:
                    o = o[1]   # the version with solution
                else:
                    o = o[0]   # the version without solution
                # a conventional exercise
                f.write('<tr><td align="center" valign="top">'
                        '%d</td>\n' % self.exnr[i])
                f.write('    <td colspan="2" valign="top">')
                f.write('<img src="%s.png" alt="%s" /></td>\n</tr>\n'%
                        (os.path.join(imagesdir,o.md5sum),
                         CleanString(CleanStringTeXComments(o.text))))
            elif isinstance(o,Exercise):
                f.write('<tr><td align="center" valign="top">'
                        '%d</td>\n' % self.exnr[i])
                firstcolDone = 1
                # Now we have to write an exercise, first the prefix:
                if isinstance(o.list[0], TeXText):
                    f.write('    <td colspan="2" valign="top">')
                    f.write('<img src="%s.png" alt="%s" /></td>\n</tr>\n'%
                        (os.path.join(imagesdir,o.list[0].md5sum),
                         CleanString(CleanStringTeXComments(o.list[0].text))))
                    firstcolDone = 0

                # Now we collect all questions:
                l = choice[i]
                # Now we write out the questions:
                for j,k in l:
                    if not(firstcolDone): f.write('<tr><td></td>\n')
                    
                    q = o.list[j]
                    f.write('    <td valign="top">')
                    f.write('<img src="%s.png" alt="%s" /></td>\n' %
                      (os.path.join(imagesdir,q.variants[k].md5sum),
                       CleanString(CleanStringTeXComments(q.variants[k].text))))
                    f.write('    <td valign="top">')
                    if q.type == 'r':
                        checked = 0  # flag, whether something is checked
                        for a in q.answers:
                            ch = ''
                            if sub and a == sub[counter]:
                                # student selected this last time
                                ch = 'checked="checked"'
                                checked = 1
                            f.write(('\n      <input type="radio" name="%s" '
                                     'value="%s" %s/> %s / ') % 
                                    ('B'+self.name+'Q'+str(counter),a,ch,a))
                        if not(checked):
                            ch = 'checked="checked" '
                        else:
                            ch = ''
                        f.write(('\n      <input type="radio" name="%s" '
                                 'value="---" %s/> - ') % 
                                ('B'+self.name+'Q'+str(counter),ch))
                    elif q.type == 'c':
                        checked = 0  # flag, whether something is checked
                        if sub:
                            checkeditems=AsciiData.TupleLine(sub[counter],
                                                             delimiter=',')
                        for a in q.answers:
                            ch = ''
                            if sub and a in checkeditems:
                                ch = 'checked="checked" '
                                checked = 1
                            f.write(('\n      <input type="checkbox" '
                                     'name="%s" value="+" %s/> %s /') % 
                                    ('B'+self.name+'Q'+str(counter)+'.'+a,ch,a))
                        ch = ''
                        if (sub and '' in checkeditems) or not(sub):
                            ch = 'checked="checked" '
                        f.write(('\n      <input type="checkbox" name="%s" '
                                 'value="+" %s/> - ') % 
                                ('B'+self.name+'Q'+str(counter),ch))
                    else:  # type is string:
                        if sub: ch = 'value = "'+CleanQuotes(sub[counter])+'" '
                        else: ch = 'value = "" '
                        f.write('<input size="12" maxlength="'+
                                str(Config.conf['MaxStringInputLength'])+'" '+
                                'name="%s" %s/> ' %
                                ('B'+self.name+'Q'+str(counter),ch))
                    if closed and type(q.solutions[k]) == types.ListType:
                        # We do not write out regular expressions!
                        f.write('<span class="ergplus">['+
                                string.join(q.solutions[k],',')+
                                ']</span>')
                    if marks and \
                       (closed or Config.conf['InteractiveMode'] != 0):
                        f.write('<span class=')
                        if marks[counter] == '+':
                            f.write('"ergplus">&nbsp;&nbsp;('+
                                    str(q.scorecorrect)+')')
                        elif marks[counter] == '-':
                            f.write('"ergminus">&nbsp;&nbsp;('+
                                    str(q.scorewrong)+')')
                        else:
                            f.write('"ergnull">&nbsp;&nbsp;(0)')
                        f.write('</span>\n')
                    f.write('</td>\n</tr>\n')
                    firstcolDone = 0

                    counter += 1

                # Now the postfix:
                if isinstance(o.list[-1],TeXText):
                    f.write('<tr><td></td>\n    <td colspan="2">')
                    f.write('<img src="%s.png" alt="%s" /></td>\n' %
                         (os.path.join(imagesdir,o.list[-1].md5sum),
                          CleanString(CleanStringTeXComments(o.list[-1].text))))
                    f.write('</tr>\n')

        # Write Table end:
        f.write('</table>\n')
        return 0

    def WebSheetTableMathJax(self,resolution,seed,f,mcresult):
        '''Creates an xhtml table for the web version without images 
but with LaTeX code for MathJax of the sheet with seed "seed" and writes
the result to the Python file object f. f is *not* closed in the end.
"mcresult" must be either None or equal to the latest mcresult of the
participant as found in the database. In this case it is an instance of
the class MCResult in Data.py. "seed" must be a unique integer that is
determined by the "id" of the participant. Returns 0 if all went well and
a negative error code otherwise.'''
        choice = self.ChooserFunction(seed)

        # are we before or after the closing date?
        closed = self.IsClosed()

        if mcresult != None:
            sub = AsciiData.TupleLine(mcresult.submission,delimiter='|')
            marks = mcresult.marks
        else:
            sub = None
            marks = None

        counter = 0   # we count questions to index sub and marks

        # Write Table heading:
        # relative widths of columns
        widths = [ 
                  int(100.0*(Config.conf['WidthOfSheetsHTML'] - 
                      Config.conf['WidthOfExerciseTextsHTML']) /
                      Config.conf['WidthOfSheetsHTML']),
                  int(100.0*Config.conf['WidthOfQuestionsHTML'] /
                      Config.conf['WidthOfSheetsHTML']) ]
        widths.append(100-widths[0]-widths[1])
        
        f.write('<table border="1">\n')
        f.write('<colgroup>\n'
                '  <col width="'+str(widths[0])+'%" />\n'
                '  <col width="'+str(widths[1])+'%" />\n'
                '  <col width="'+str(widths[2])+'%" />\n'
                '</colgroup>\n')

        # walk through the list:
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,TeXText):
                f.write('<tr><td colspan="3">')
                f.write(CleanString(CleanStringTeXComments(o.text)))
                f.write('</td>\n</tr>\n')
            elif type(o) == types.TupleType and isinstance(o[0],TeXText):
                # a conventional exercise
                if closed:
                    o = o[1]   # the version with solution
                else:
                    o = o[0]   # the version without solution
                # a conventional exercise
                f.write('<tr><td align="center" valign="top">'
                        '%d</td>\n' % self.exnr[i])
                f.write('    <td colspan="2" valign="top">')
                f.write('%s</td>\n</tr>\n'%
                        (CleanString(CleanStringTeXComments(o.text))))
            elif isinstance(o,Exercise):
                f.write('<tr><td align="center" valign="top">'
                        '%d</td>\n' % self.exnr[i])
                firstcolDone = 1
                # Now we have to write an exercise, first the prefix:
                if isinstance(o.list[0], TeXText):
                    f.write('    <td colspan="2" valign="top">')
                    f.write('%s</td>\n</tr>\n'%
                        (CleanString(CleanStringTeXComments(o.list[0].text))))
                    firstcolDone = 0

                # Now we collect all questions:
                l = choice[i]
                # Now we write out the questions:
                for j,k in l:
                    if not(firstcolDone): f.write('<tr><td></td>\n')
                    
                    q = o.list[j]
                    f.write('    <td valign="top">')
                    f.write('%s</td>\n' %
                      (CleanString(CleanStringTeXComments(q.variants[k].text))))
                    f.write('    <td valign="top">')
                    if q.type == 'r':
                        checked = 0  # flag, whether something is checked
                        for a in q.answers:
                            ch = ''
                            if sub and a == sub[counter]:
                                # student selected this last time
                                ch = 'checked="checked"'
                                checked = 1
                            f.write(('\n      <input type="radio" name="%s" '
                                     'value="%s" %s/> %s / ') % 
                                    ('B'+self.name+'Q'+str(counter),a,ch,a))
                        if not(checked):
                            ch = 'checked="checked" '
                        else:
                            ch = ''
                        f.write(('\n      <input type="radio" name="%s" '
                                 'value="---" %s/> - ') % 
                                ('B'+self.name+'Q'+str(counter),ch))
                    elif q.type == 'c':
                        checked = 0  # flag, whether something is checked
                        if sub:
                            checkeditems=AsciiData.TupleLine(sub[counter],
                                                             delimiter=',')
                        for a in q.answers:
                            ch = ''
                            if sub and a in checkeditems:
                                ch = 'checked="checked" '
                                checked = 1
                            f.write(('\n      <input type="checkbox" '
                                     'name="%s" value="+" %s/> %s /') % 
                                    ('B'+self.name+'Q'+str(counter)+'.'+a,ch,a))
                        ch = ''
                        if (sub and '' in checkeditems) or not(sub):
                            ch = 'checked="checked" '
                        f.write(('\n      <input type="checkbox" name="%s" '
                                 'value="+" %s/> - ') % 
                                ('B'+self.name+'Q'+str(counter),ch))
                    else:  # type is string:
                        if sub: ch = 'value = "'+CleanQuotes(sub[counter])+'" '
                        else: ch = 'value = "" '
                        f.write('<input size="12" maxlength="'+
                                str(Config.conf['MaxStringInputLength'])+'" '+
                                'name="%s" %s/> ' %
                                ('B'+self.name+'Q'+str(counter),ch))
                    if closed and type(q.solutions[k]) == types.ListType:
                        # We do not write out regular expressions!
                        f.write('<span class="ergplus">['+
                                string.join(q.solutions[k],',')+
                                ']</span>')
                    if marks and \
                       (closed or Config.conf['InteractiveMode'] != 0):
                        f.write('<span class=')
                        if marks[counter] == '+':
                            f.write('"ergplus">&nbsp;&nbsp;('+
                                    str(q.scorecorrect)+')')
                        elif marks[counter] == '-':
                            f.write('"ergminus">&nbsp;&nbsp;('+
                                    str(q.scorewrong)+')')
                        else:
                            f.write('"ergnull">&nbsp;&nbsp;(0)')
                        f.write('</span>\n')
                    f.write('</td>\n</tr>\n')
                    firstcolDone = 0

                    counter += 1

                # Now the postfix:
                if isinstance(o.list[-1],TeXText):
                    f.write('<tr><td></td>\n    <td colspan="2">')
                    f.write('%s</td>\n' %
                         (CleanString(CleanStringTeXComments(o.list[-1].text))))
                    f.write('</tr>\n')

        # Write Table end:
        f.write('</table>\n')
        return 0

    def AcceptSubmission(self,p,seed,query):
        '''Accepts a submission from the web page. p is an object of
type Person. The seed is the seed for the current person and the query
is an object from which one can extract form data with the 'get' method.
This method returns 1 on success and 0 on failure. A failure should only
occur if something horrible happens like disk full or manipulation by
the user. Additionally the return value 2 is possible to indicate
success but some dubious (and nearly impossible) submission, most 
probably by a buggy browser.'''
        # Find out the special situation for this person:
        choice = self.ChooserFunction(seed)

        sub = []     # here we collect submissions
        marks = []   # here we collect the mark as strings of length 1
        counter = 0  # we count questions to index sub and marks
        score = 0    # points

        dubioussubmission = 0  # note any dubious submission
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,Exercise):
                # here we have to do something
                exscore = 0
                l = choice[i]
                for j,k in l:
                    q = o.list[j]    # the question object
                    if q.type == 'r':     # a radio button
                        val = query.get('B'+self.name+'Q'+str(counter),[''])[0]
                        if val == '---': val = ''  # we say nothing!
                        if val != '' and not(val in q.answers):
                            # something is wrong! Write a log entry and
                            # assume empty answer!
                            Utils.Error('Radio button value "'+val+'" found,'
                                ' which should not be possible!',
                                prefix="Warning:")
                            dubioussubmission = 1
                            val = ''
                        sub.append(val)
                        if val == '': 
                            marks.append('0')
                        elif val in q.solutions[k]:   # this list has always
                                                      # length 1
                            marks.append('+')
                            exscore += q.scorecorrect
                        else:
                            marks.append('-')
                            exscore += q.scorewrong
                    elif q.type == 'c':   # a choice question
                        # first get selected choice:
                        val = query.get('B'+self.name+'Q'+str(counter),
                                        [''])[0].strip()
                        if val == '+':    # nothing submitted
                            innerchoice = ['']
                        else:
                            innerchoice = []
                        for a in q.answers:
                            val=query.get('B'+self.name+'Q'+str(counter)+'.'+a,
                                            [''])[0].strip()
                            if val == '+':
                                innerchoice.append(a)
                        innerchoice.sort()
                        sub.append(AsciiData.LineTuple(innerchoice,
                                                       delimiter=','))
                        if '' in innerchoice:
                            marks.append('0')
                        elif innerchoice == q.solutions[k]:
                            marks.append('+')
                            exscore += q.scorecorrect
                        else:
                            marks.append('-')
                            exscore += q.scorewrong
                    elif q.type == 's':   # a free form question
                        val = query.get('B'+self.name+'Q'+str(counter),
                                        [''])[0].strip()
                        if val == '---': val = ''  # we say nothing!
                        # limit size!
                        val = val[:Config.conf['MaxStringInputLength']]
                        sub.append(val)
                        if val == '': 
                            marks.append('0')
                        else:
                            if type(q.solutions[k]) == types.ListType:
                                if val in q.solutions[k]:
                                    marks.append('+')
                                    exscore += q.scorecorrect
                                else:
                                    marks.append('-')
                                    exscore += q.scorewrong
                            else:
                                if q.solutions[k][1].search(val):
                                    marks.append('+')
                                    exscore += q.scorecorrect
                                else:
                                    marks.append('-')
                                    exscore += q.scorewrong
                    counter += 1
                if exscore < o.scorelowlim: exscore = o.scorelowlim
                score += exscore
             
        subst = AsciiData.LineTuple(sub,delimiter='|')
        marks = string.join(marks,'')
        # Now we append the submission to the data file:
        m = Data.MCResult()
        m.marks = marks
        m.score = score
        m.submission = subst
        m.date = int(time.time())
        line = AsciiData.LineTuple( (p.id,self.name,marks,str(score),subst,
                                     str(m.date)) )
        Data.Lock.acquire()
        try:
            Data.mcresultsdesc.AppendLine(line)
        except:
            Data.Lock.release()
            Utils.Error('Failed to register submission:\n'+line)
            return 0

        # Put new data into database in memory:
        p.mcresults[self.name] = m
        Data.Lock.release()

        if dubioussubmission:
            return 2
        else:
            return 1

    def Resubmit(self,p,seed):
        '''Accepts a resubmission from within the server. This is for the
case that the "correct answer" was not entered properly in the first place.
This function mimics the behaviour of "AcceptSubmission", but takes its 
data from the stored submission in memory instead from a query.
p is an object of type Person. The seed is the seed for the current
person and the sub is an object from which one can extract form data
with the 'get' method. This method returns 1 on success and 0 on
failure. A failure should only occur if something horrible happens like
disk full or manipulation by the user.'''
        # Find out the special situation for this person:
        choice = self.ChooserFunction(seed)

        if not(p.mcresults.has_key(self.name)):   # we know nothing for him
            return 1
        previousm = p.mcresults[self.name]  # an MCResult object
        previoussub = AsciiData.TupleLine(previousm.submission,delimiter='|')
        
        sub = []     # here we collect submissions
        marks = []   # here we collect the mark as strings of length 1
        counter = 0  # we count questions to index sub and marks
        score = 0    # points

        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,Exercise):
                # here we have to do something
                exscore = 0
                l = choice[i]
                for j,k in l:
                    q = o.list[j]    # the question object
                    if q.type == 'r':     # a radio button
                        val = previoussub[counter]
                        sub.append(val)
                        if val == '': 
                            marks.append('0')
                        elif val in q.solutions[k]:   # this list has always
                                                      # length 1
                            marks.append('+')
                            exscore += q.scorecorrect
                        else:
                            marks.append('-')
                            exscore += q.scorewrong
                    elif q.type == 'c':   # a choice question
                        # first get selected choice:
                        innerchoice = AsciiData.TupleLine(previoussub[counter],
                                                          delimiter=',')
                        sub.append(AsciiData.LineTuple(innerchoice,
                                                       delimiter=','))
                        if '' in innerchoice:
                            marks.append('0')
                        elif innerchoice == q.solutions[k]:
                            marks.append('+')
                            exscore += q.scorecorrect
                        else:
                            marks.append('-')
                            exscore += q.scorewrong
                    elif q.type == 's':   # a free form question
                        val = previoussub[counter]
                        sub.append(val)
                        if val == '': 
                            marks.append('0')
                        else:
                            if type(q.solutions[k]) == types.ListType:
                                if val in q.solutions[k]:
                                    marks.append('+')
                                    exscore += q.scorecorrect
                                else:
                                    marks.append('-')
                                    exscore += q.scorewrong
                            else:
                                if q.solutions[k][1].search(val):
                                    marks.append('+')
                                    exscore += q.scorecorrect
                                else:
                                    marks.append('-')
                                    exscore += q.scorewrong
                    counter += 1
                if exscore < o.scorelowlim: exscore = o.scorelowlim
                score += exscore
             
        subst = AsciiData.LineTuple(sub,delimiter='|')
        marks = string.join(marks,'')
        # Now we append the submission to the data file:
        m = Data.MCResult()
        m.marks = marks
        m.score = score
        m.submission = subst
        m.date = previousm.date   # we fake the last submission date
        line = AsciiData.LineTuple( (p.id,self.name,marks,str(score),subst,
                                     str(m.date)) )
        Data.Lock.acquire()
        try:
            Data.mcresultsdesc.AppendLine(line)
        except:
            Data.Lock.release()
            Utils.Error('Resubmit: failed to register submission:\n'+line)
            return 0

        # Put new data into database in memory:
        p.mcresults[self.name] = m
        Data.Lock.release()

        return 1

    def LatexSheetTable(self,seed):
        '''Creates a latex longtable environment for the PDF version  
of the sheet with seed "seed" and returns the result as a string.
'''
        choice = self.ChooserFunction(seed)

        counter = 0   # we count questions to index sub and marks
        
        # get widths of fields from config
        wos = str(Config.conf['WidthOfSheetsPDF'])+'in'
        woe = str(Config.conf['WidthOfExerciseTextsPDF'])+'in'
        woq = str(Config.conf['WidthOfQuestionsPDF'])+'in'
        woansw = str(Config.conf['WidthOfExerciseTextsPDF'] -
                     Config.conf['WidthOfQuestionsPDF'] - 0.3)+'in'
        f = cStringIO.StringIO()
        f.write('\\begin{longtable}{|c|p{'+woq+'}|p{'+woansw+'}|}\n' + \
                '\\hline\\endfoot\n\\hline\\endhead\\hline\n')
        
        # walk through the list:
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,TeXText):
                f.write(('\\multicolumn{3}{|p{'+wos+\
                  '}|}{\\begin{minipage}[t]{'+wos+\
                  '}%s\\vspace{1mm}\\end{minipage}} \\\\\n\\hline') \
                  % string.strip(CleanStringTeXComments(o.text)))
            elif type(o) == types.TupleType and isinstance(o[0],TeXText):
                # a conventional exercise:
                if self.IsClosed():
                    o = o[1]
                else:
                    o = o[0]
                f.write(('%d & \\multicolumn{2}{p{'+woe+\
                  '}|}{\\begin{minipage}[t]{'+woe+\
                  '}%s\\vspace{1mm}\\end{minipage}}\\\\\n\\hline\n') \
                  % (self.exnr[i], \
                     string.strip(CleanStringTeXComments(o.text))))
            elif isinstance(o,Exercise):
                f.write('%d & ' % self.exnr[i])
                
                # Now we have to write an exercise, first the prefix:
                if isinstance(o.list[0], TeXText):
                    f.write(('\\multicolumn{2}{p{'+woe+\
                      '}|}{\\begin{minipage}[t]{'+woe+
                      '}%s\\vspace{1mm}\\end{minipage}}\\\\\n\\cline{2-3}\n&') \
                      % string.strip(CleanStringTeXComments(o.list[0].text)))
                    
                # Now we collect all questions:
                l = choice[i]
                
                # Now we write out the questions:
                qnr = 1
                for j,k in l:
                    if (j,k) == (None,None):
                        if seed == '':  # called for checking all variants
                            f.write('\n\\\\[-5.5mm]\n\\cline{2-3}\n {\\tiny '+\
                                    str(qnr) +'} & ')
                            qnr = qnr + 1
                        else:
                            f.write('\n\\\\[-5.5mm]\n\\cline{2-3}\n & ')
                        continue;
                    q = o.list[j]
                    f.write(('\\begin{minipage}[t]{'+woq+\
                     '}%s\\vspace{1mm}\\end{minipage} & ') \
                     % string.strip(CleanStringTeXComments(q.variants[k].text)))
                    if q.type == 'r':
                        for a in q.answers:
                            f.write('\\ $\\bigcirc$ %s ' % a)
                            if a != q.answers[-1]:
                                f.write(' / ')
                    elif q.type == 'c':
                        for a in q.answers:
                            f.write('\\ $\\Box$ %s ' % a)
                            if a != q.answers[-1]:
                                f.write(' / ')
                    else:  # type is string:
                        f.write('\\rule[-5pt]{'+woansw+\
                                '}{0.5pt}\\rule{5mm}{0mm} ')
                    if j != l[-1][0] or k != l[-1][1]:
                        f.write('\\\\\n\\cline{2-3}\n   & ')
                    else:
                        f.write('\\\\\n\\hline\n')

                # Now the postfix:
                if isinstance(o.list[-1],TeXText):
                    f.write(('\\multicolumn{2}{p{'+woe+\
                      '}|}{\\begin{minipage}[t]{'+woe+\
                      '}%s\\vspace{1mm}\\end{minipage}} \\\\\n\\hline\n') \
                      % string.strip(CleanStringTeXComments(o.list[-1].text)))

        # Write Table end:
        f.write('\\end{longtable}\n')

        # Return the code as string
        res = f.getvalue()
        f.close()
        return res
    
    def LatexSheetNoTable(self):
        '''Creates a latex input of exercises and extra texts. Only
        works for sheets without interactive exercises (which are shown
        as "???". This is to avoid the - in this case - unnecessary table 
        around the exercise texts.
'''
        f = cStringIO.StringIO()
        
        # walk through the list:
        for i in range(len(self.list)):
            o = self.list[i]
            if isinstance(o,TeXText):
                f.write(string.strip(CleanStringTeXComments(o.text)))
            if type(o) == types.TupleType and isinstance(o[0],TeXText):
                # a conventional exercise
                if self.IsClosed():
                    o = o[1]
                else:
                    o = o[0]
                f.write(('\n\n\\begin{exercise}{%d}\n%s\n\\end{exercise}'
                '\n\n') % (self.exnr[i], \
                           CleanStringTeXComments(string.strip(o.text))))
            elif isinstance(o,Exercise):
                f.write('\n\n???\n\n')
        res = f.getvalue()
        f.close()
        return res
    
    def AllSolutions(self):
        res = ['']
        for i in range(len(self.list)):
            ex = self.list[i]
            if isinstance(ex, Exercise):
                qunr = 0
                for j in range(len(ex.list)):
                    qu = ex.list[j]
                    if isinstance(qu, Question):
                        qunr = qunr+1
                        #ll = l[qunr]
                        for k in range(qu.nrvariants):
                          if type(qu.solutions[k]) == types.ListType:
                            res.append('Ex '+str(self.exnr[i])+', Qu '+
                              str(qunr)+ ', Var '+str(k+1)+': '+
                              str(qu.solutions[k]))
                          else:  # a regular expression:
                            res.append('Ex '+str(self.exnr[i])+', Qu '+
                              str(qunr)+ ', Var '+str(k+1)+': '+
                              qu.solutions[k][0])
                res.append('')
        return string.join(res, '\n')

    def StatisticsForVariant(self, exNr, quNr, varNr):
        ''' Gives detailed  statistics for the specified variant 
        '''
        exercise = None
        i = 0
        numberOfQuestionsBefore = 0
        while ((exercise  == None) and (i < len(self.exnr)) ) :
            if self.exnr[i] == exNr :
                exercise = self.list[i]
                break
            if self.nrquestions[i] != None:
                numberOfQuestionsBefore += self.nrquestions[i]
            i += 1
        if exercise == None: return None
        exIndex = i
        quCount = 0
        found = 0        
        i = 0
        while ((i < len(exercise.list)) and (found  == 0)):
            if isinstance(exercise.list[i], Question) : quCount += 1
            if quNr == quCount: 
                found = 1
                break
            i += 1
        if found ==0: return None
        quIndex = i 
        peopleCount = 0
        submissionCount = 0
        correctAnswerCount = 0
        dictCorrectAnswers = {}
        dictFalseAnswers = {}
        for k in Data.people.keys():
            p = Data.people[k]
            if not(Config.conf['GuestIdRegExp'].match(k)):
                personalQuestions = \
                       self.ChooserFunction(Utils.SeedFromId(p.id)) 
                personalQuestions = personalQuestions[exIndex]
                countOfQuestions = -1
                # personalQuestions is now a list of tuples 
                #   (index in ex.list, variant number)
                for (i,n) in personalQuestions: 
                    countOfQuestions += 1    #0 for first question
                    if i == quIndex and ((n+1) == varNr):
                        if p.mcresults.has_key(self.name):
                            peopleCount += 1
                            if p.mcresults[self.name].marks[ \
                               numberOfQuestionsBefore+countOfQuestions] !='0':
                                submissionCount += 1
                                sm = p.mcresults[self.name].submission.split(
                                 '|')[numberOfQuestionsBefore+countOfQuestions]
                                if p.mcresults[self.name].marks[ \
                                   numberOfQuestionsBefore+countOfQuestions] \
                                    =='+':
                                    correctAnswerCount += 1
                                    if dictCorrectAnswers.has_key(sm):
                                        dictCorrectAnswers[sm].append(p.id)
                                    else:
                                        dictCorrectAnswers[sm]=[p.id]
                                else:
                                    if dictFalseAnswers.has_key(sm):
                                        dictFalseAnswers[sm].append(p.id)
                                    else:
                                        dictFalseAnswers[sm]=[p.id]
        if isinstance(self.list[exIndex].list[0],TeXText):
            questionText = self.list[exIndex].list[0]
        else:
            questionText = None
        return ( peopleCount, submissionCount, correctAnswerCount,
                 dictCorrectAnswers, dictFalseAnswers, 
                 questionText,
                 self.list[exIndex].list[quIndex].variants[varNr-1])
    
    def Statistics(self):
        presented = {}   # How many students have seen this question/variant?
        tried = {}       # How many students have submitted an solution?
        solved = {}      # How many students did it right?

        peopleKeys = Data.people.keys()

        for i in range(len(self.list)):
            if isinstance(self.list[i], Exercise):
                ex = self.list[i]
                presented[ex.key] = {}
                tried[ex.key] = {}
                solved[ex.key] = {}
                for j in range(len(ex.list)):
                    qu = ex.list[j]
                    if isinstance(qu, Question):
                        presented[ex.key][j]=[]
                        tried[ex.key][j]=[]
                        solved[ex.key][j]=[]
                        for k in range(qu.nrvariants):
                            presented[ex.key][j].append(0)
                            tried[ex.key][j].append(0)
                            solved[ex.key][j].append(0)
        submissionCount = 0
        peopleCount = 0
        for k in peopleKeys:
          p = Data.people[k]
          if not(Config.conf['GuestIdRegExp'].match(k)):
            personalExercises = self.ChooserFunction(Utils.SeedFromId(k))
            countOfQuestions = 0
            peopleCount += 1
            if p.mcresults.has_key(self.name): submissionCount+=1
            for i in range(len(personalExercises)):
              if isinstance(self.list[i], Exercise):
                exKey = self.list[i].key
                exerciseList = personalExercises[i]
                for exerciseIndex,variantNumber in exerciseList:
                  if p.mcresults.has_key(self.name):
                      presented[exKey][exerciseIndex][variantNumber] += 1
                      if p.mcresults[self.name].marks[countOfQuestions]!='0':
                        tried[exKey][exerciseIndex][variantNumber] += 1
                      if p.mcresults[self.name].marks[countOfQuestions]=='+':
                        solved[exKey][exerciseIndex][variantNumber] += 1
                      countOfQuestions += 1

        res = []
        for i in range(len(self.list)):
            if isinstance(self.list[i], Exercise):
                ex = self.list[i]
                qunr = 0
                for j in range(len(ex.list)):
                    qu = ex.list[j]
                    if isinstance(qu, Question):
                        qunr = qunr+1
                        for k in range(qu.nrvariants):
                            res.append( (self.exnr[i], qunr, k+1, \
                                 presented[ex.key][j][k] , 
                                 tried[ex.key][j][k], solved[ex.key][j][k] ) )

        return (peopleCount, submissionCount, res)

class Exercise(Utils.WithNiceRepr):
    key = "auf123"           # a unique key for the Exercise
    list = []                # a list of objects: TeXText or Question
    nrquestions = 0          # number of question objects in "list"
    filename = ""            # name of file containing the exercise
    position = (0,0,0,0)     # position EXERCISE element in that file
    keywords = ""            # a string with keywords for searching
    scorelowlim = 0          # lower limit for complete score for exercise
    def __init__(self):
        self.list = []
    

class Question(Utils.WithNiceRepr):
    type = None              # "r" for radio buttons, "s" for string 
                             # "c" for choice of buttons
    nrvariants = 0           # number of variants of this Question
    nranswers = 1            # number of possible answers
    answers = ["Ja","Nein"]  # possible answers, None for type "s"
    variants = []            # for each variant a TeXText
    solutions = []           # for each variant the correct solution(s)
                             # each entry in here is a list of possible
                             # correct solutions or otherwise a pair of a
                             # regular expression string and its compiled
                             # regexp to which the answer is matched.
                             # The latter is only possible for type "s".
    position = (0,0,0,0)     # position of QUESTION element in file
    scorecorrect = 1         # score for a correct answer
    scorewrong = -1          # score for a wrong answer

    def __init__(self):
        self.variants = []
        self.solutions = []
    

# To simplify handling of exercises and sheets in different directories 
# we collect first all exercises in a dictionary and then the sheets in 
# a list. All exercises must be identified by unique keys which are used in
# the sheets.

AllExercises = {}
AllSheets = []
# For simpler looping we collect the text pieces as well.
AllTexts = []


def SheetList():
    '''This function delivers a list of tripels, for each sheet one,
where the first component of each pair is the sheet number as an integer,
the second component is the name of the sheet as a string and the third
is the sheet object itself. The pairs are sorted by sheet number.'''
    l = []
    for s in AllSheets:
        l.append( (s.nr,s.name,s) )
    l.sort()
    return l
    
# The following function is called when pyRXP wants to open the dtd file:
# We direct pyRXP to the a directory containing the DTDs:
def OurDtdOpener(d):
    return os.path.join(Config.conf['PathToDTDs'],d)


# Create an XML parser, we switch on location information.
Parser = XMLRewrite.NewParser({'fourth': pyRXPU.recordLocation,
                       'ReturnDefaultedAttributes': 0,
                       'MergePCData': 1,
                       'Validate': 1,
                       'eoCB': OurDtdOpener })


# A little comment on error processing:
#   The following functions all report their errors at the place where
#   they occur. Most of the "inner" functions afterwards just raise
#   some exception. The "outer" functions "ReadExercisesFile" and
#   "ReadExercisesDirectory" just try to use the inner functions to
#   accumulate exercises and go on undisturbed, if this does not
#   work for some exercise.

# For reading exercises we use functions which create and fill the class
# instances described above. Their argument is a corresponding subtree from
# the XML parser.
def MakeTeXText(t,width):
    global AllTexts
    res = TeXText(string.join(t[2],'').encode('ISO8859-1','replace'),
                  t[3][0][0].encode('ISO-8859-1','replace'),
                  (t[3][0][1], t[3][0][2], t[3][1][1], t[3][1][2]),
                  width)
    AllTexts.append(res)
    return res


# the reading of exercises:

# transform ANSWERS element to tuple (type, list of answers)
def AnswersTuple(a):
  t = a[1]['type'].encode('ISO-8859-1','replace')
  if not t in ['r','c','s']:
      Utils.Error('Attribute "type" must be "r", "c" or "s" at ' +
                  Utils.StrPos(a[3]), prefix="Warning:")
      t = 's'
  if t == 's':
      return (t, None)
  elif a[2] == None or len(a[2]) == 0:
      Utils.Error('Missing content in ANSWERS element at '+Utils.StrPos(a[3]))
      raise Utils.UtilsError
  else:
      onlystrings = 1   # first look whether there are only strings
      answers = []      # here we collect the strings
      for u in a[2]:
          if type(u) != types.UnicodeType:
              onlystrings = 0
          else:
              answers.append(u.encode('ISO-8859-1','replace'))
      if not(onlystrings):
          Utils.Error('ANSWERS element must only contain character data at '+
                      Utils.StrPos(a[3]))
          raise Utils.UtilsError
      answers = string.join(answers,'').split('|')
      answers = map(string.strip,answers)
      if len(answers) < 2:
          Utils.Error('ANSWERS element contains only one possibility at '+
                      Utils.StrPos(a[3]), prefix="Warning:")
      return (t, answers)

# this function gets the default set of answers as second argument
# (None, if not set and otherwise a tuple (type, list of answer strings))
# It either returns a ready made question object or raises an exception.
def MakeQuestion(t, defansw):
    res = Question()
    answ = None
    res.scorecorrect = Config.conf['MCScoreCorrectDefault']
    if type(t[1]) == types.DictType and t[1].has_key('scorecorrect'):
        try:
            res.scorecorrect = int(t[1]['scorecorrect'])
        except:
            Utils.Error('QUESTION element with unreadable scorecorrect ' +
                        'attribute at ' + Utils.StrPos(t[3]),
                        prefix = 'Warning: ')
    res.scorewrong = Config.conf['MCScoreWrongDefault']
    if type(t[1]) == types.DictType and t[1].has_key('scorewrong'):
        try:
            res.scorewrong = int(t[1]['scorewrong'])
        except:
            Utils.Error('QUESTION element with unreadable scorewrong ' +
                        'attribute at ' + Utils.StrPos(t[3]),
                        prefix = 'Warning: ')
    for a in t[2]:
      if type(a) == types.UnicodeType:
          pass   # this should not happen as we have "element content" here
      elif a[0] == 'ANSWERS':
          if answ:
              Utils.Error('Only one specification of answers allowed: ' +
                        a[3][0][0].encode('ISO-8859-1','replace') + 
                        ', line ' + str(a[3][0][1]))
              raise Utils.UtilsError
          answ = AnswersTuple(a)
      elif a[0] == 'VARIANT':
          if res.type == None:
              if answ == None:
                  answ = defansw
              if answ == None:
                  Utils.Error('Question variant without specified set of ' +
                        'answers at ' + Utils.StrPos(a[3]))
                  raise Utils.UtilsError
              res.type = answ[0]
              res.answers = answ[1]
              res.nranswers = len(answ)
          v = MakeTeXText(a,Config.conf['WidthOfQuestionsHTML'])
          res.variants.append(v)
          if a[1].has_key('solution'):
              if a[1].has_key('solutionregexp'):
                  Utils.Error('Question variant with "solution" attribute and '
                     '"solutionregexp" attribute forbidden\nat '+
                     Utils.StrPos(a[3]))
                  raise Utils.UtilsError
              sol = a[1]['solution'].encode('ISO-8859-1','replace').strip()
              if sol == '':
                  sol = []
              else:
                  sol = sol.split('|')
                  sol = map(string.strip,sol)
              if res.type == 'r' and len(sol) > 1:
                  Utils.Error('Question variant of type "r" has more than one '
                     'correct solution\nat '+Utils.StrPos(a[3]))
                  raise Utils.UtilsError
              sol.sort()
              res.solutions.append(sol)
          elif a[1].has_key('solutionregexp'):
              if res.type != 's':
                  Utils.Error('Question variant with "solutionregexp" '
                     'attribute has different type than "s"\nat '+
                     Utils.StrPos(a[3]))
                  raise Utils.UtilsError
              sol = a[1]['solutionregexp'].encode('ISO-8859-1','replace')
              try:
                  solre = re.compile(sol)
              except:
                  Utils.Error('Cannot compile regular expression: '+sol+'\nat '+
                       Utils.StrPos(a[3]))
                  raise Utils.UtilsError
              res.solutions.append((sol,solre))
          else:
              Utils.Error('Question variant has no attribute "solution" or '
                          '"solutionregexp"\nat '+Utils.StrPos(a[3]))
              raise Utils.UtilsError
          res.nrvariants = res.nrvariants + 1
              
    return res


# A function for creating an Exercise object from an EXERCISE element.
def MakeExercise(t, prefix=''):
    # this k becomes key in AllExercises
    k = prefix + t[1]['key']
    ex = Exercise()
    ex.key = k
    ex.filename = t[3][0][0].encode('ISO-8859-1','replace')
    ex.position = (t[3][0][1], t[3][0][2], t[3][1][1], t[3][1][2])
    if t[1].has_key('keywords'):
        ex.keywords = t[1]['keywords']
    ex.scorelowlim = Config.conf['MCScoreExerciseLowerLimitDefault']
    if t[1].has_key('mcscorelowerlimit'):
        try:
            ex.scorelowlim = int(t[1]['mcscorelowerlimit'])
        except:
            Utils.Error('EXERCISE element with unreadable mcscorelowerlimit ' +
                        'attribute at ' + Utils.StrPos(t[3]),
                        prefix = 'Warning: ')
    defansw = None
    for a in t[2]:
        if type(a) == types.UnicodeType:   # this will probably not happen!
            pass        # because we have "element content" here.
        elif a[0] == 'TEXT':
            ex.list.append(MakeTeXText(a,
                                       Config.conf['WidthOfExerciseTextsHTML']))
        elif a[0] == 'ANSWERS':
            defansw = AnswersTuple(a)
        elif a[0] == 'QUESTION':
            ex.list.append(MakeQuestion(a, defansw))
            ex.nrquestions = ex.nrquestions + 1
    # now put into AllExercises
    if AllExercises.has_key(k):
        Utils.Error('Overwriting exercise with name '+k,prefix="Warning:")
    AllExercises[k] = ex

# We distinguish the two cases where several (enclosed by an <EXERCISES>
# tag) or just one <EXERCISE> is contained in the file fname.
# The prefix is prepended to the exercise key.
def ReadExercisesFile(fname, prefix=''):
  # Parsing and validating the content of an .auf file
  tree = XMLRewrite.Parse(Parser, file = fname)
  if not tree:
    Utils.Error('Cannot read or parse exercises file '+fname+'.')
    return

  # Now we can be sure that the "tree" contains data of a valid exercises
  # document.
  if tree[0] == 'EXERCISES':
      for a in tree[2]:
          if type(a) == types.TupleType and a[0] == 'EXERCISE':
               try:
                   MakeExercise(a, prefix)
               except:   # may fail, error is already reported
                   traceback.print_exc()
                   Utils.Error("Exception raised.")
  elif tree[0] == 'EXERCISE':
      try:
          MakeExercise(tree, prefix)
      except:   # may fail, error is already reported
          traceback.print_exc()
          Utils.Error("Exception raised.")

# Read one file as a TeX exercises:
def ReadTeXFile(fname,prefix):
    try:
        s = Utils.StringFile(fname)
    except:
        Utils.Error('Did not read '+fname+'.')
        return
    b = prefix + os.path.basename(fname)
    # Here we create two TeXTexts, one for before the closure time of the
    # sheet and one for after that time:
    p = s.find("\n% SOLUTION\n")
    if p == -1:
        ssol = s
        sbef = s
    else:
        ssol = s
        sbef = s[:p+1]
    tsol = TeXText(ssol,fname,(1,1,ssol.count('\n'),1),
                   Config.conf['WidthOfExerciseTextsHTML'])
    AllTexts.append(tsol)
    tbef = TeXText(sbef,fname,(1,1,sbef.count('\n'),1),
                   Config.conf['WidthOfExerciseTextsHTML'])
    AllTexts.append(tbef)
    if AllExercises.has_key(b):
        Utils.Error('Overwriting exercise with key '+b+' .',
                    prefix='Warning:')
    AllExercises[b] = (tbef,tsol)

# Read all *.auf files in a directory. Using the prefix, one can use 
# several such directories and avoid key-name conflict without editing the
# .auf files. Note that we ignore all errors. They are reported to the
# user but offending exercises will just not exist later on, probably
# rendering some sheets useless.
# In addition we read all *.tex files and store them as TeXTexts with
# their basename as key into AllExercises
def ReadExercisesDirectory(dirname, prefix=''):
    pos = dirname.find('|')
    if pos >= 0:   # there is a prefix
        prefix = dirname[pos+1:]
        dirname = dirname[:pos]
    for fname in glob.glob(os.path.join(dirname, '*.auf')):
        ReadExercisesFile(fname, prefix)
    for fname in glob.glob(os.path.join(dirname, '*.tex')):
        ReadTeXFile(fname, prefix)


# The reading of sheets:


# A function for creating an Exercise object from an EXERCISE element.
def MakeSheet(t):
    # this k becomes key in AllExercises
    sh = Sheet()
    sh.filename = t[3][0][0].encode('ISO-8859-1','replace')
    sh.position = (t[3][0][1], t[3][0][2], t[3][1][1], t[3][1][2])
    if t[1].has_key('counts'):
        try:
            sh.counts = int(t[1]['counts'])
        except:
            Utils.Error('Value of "counts" attribute is no integer: '+
                        t[1]['counts'].encode('ISO-8859-1','replace')+ ' at '+
                        Utils.StrPos(t[3])+'\nAssuming "1"',prefix='Warning:')
            sh.counts = 1
    else:
        sh.counts = 1
    try:
        sh.nr = int(t[1]['nr'])
    except:
        Utils.Error('Value of "nr" attribute is no integer: '+
                    t[1]['nr'].encode('ISO-8859-1','replace')+ ' at '+
                    Utils.StrPos(t[3]))
        raise Utils.UtilsError
    if t[1].has_key('name'):
        sh.name = t[1]['name'].encode('ISO-8859-1','replace')
    else:
        sh.name = str(sh.nr)
    if t[1].has_key('first'):
        try:
            sh.first = int(t[1]['first'])
        except:
            Utils.Error('Value of "first" attribute is no integer: '+
                        t[1]['first'].encode('ISO-8859-1','replace')+ ' at '+
                        Utils.StrPos(t[3])+'\nAssuming "1"',prefix='Warning:')
            sh.first = 1
    else:
        sh.first = 1
    if t[1].has_key('magic'):
        try:
            sh.magic = int(t[1]['magic'])
        except:
            Utils.Error('Value of "magic" attribute is no integer: '+
                        t[1]['magic'].encode('ISO-8859-1','replace')+ ' at '+
                        Utils.StrPos(t[3])+'\nAssuming "123456"',
                        prefix='Warning:')
            sh.magic = 123456
    else:
        sh.magic = 123456
    opento = t[1]['opento'].encode('ISO-8859-1','replace')
    try:
        x = list(time.strptime(opento,"%H:%M_%d.%m.%Y"))
        x[8] = -1  # dst flag
        sh.opento = time.mktime(x)
    except ValueError:
        Utils.Error('Value of "opento" attribute is unparsable: '+
                    opento+' at '+Utils.StrPos(t[3])+
                    '\nWill stay open forever.',prefix='Warning:')
        sh.opento = 0

    if t[1].has_key('openfrom'):
        openfrom = t[1]['openfrom'].encode('ISO-8859-1','replace')
        try:
            x = list(time.strptime(openfrom,"%H:%M_%d.%m.%Y"))
            x[8] = -1  # dst flag
            sh.openfrom = time.mktime(x)
        except ValueError:
            Utils.Error('Value of "openfrom" attribute is unparsable: '+
                        openfrom+' at '+Utils.StrPos(t[3])+
                        '\nAssuming -infinity.',prefix='Warning:')
            sh.openfrom = None
    else:
        sh.openfrom = None
    if t[1].has_key('maxhomescore'):
        try:
            sh.maxhomescore = int(t[1]['maxhomescore'])
        except:
            Utils.Error('Value of "maxhomescore" attribute is no integer: '+
                        t[1]['maxhomescore'].encode('ISO-8859-1','replace')+ 
                        ' at '+Utils.StrPos(t[3])+'\nAssuming "-1"',
                        prefix='Warning:')
            sh.maxhomescore = -1
    else:
        sh.maxhomescore = -1
    if t[1].has_key('starhomescore'):
        try:
            sh.starhomescore = int(t[1]['starhomescore'])
        except:
            Utils.Error('Value of "starhomescore" attribute is no integer: '+
                        t[1]['starhomescore'].encode('ISO-8859-1','replace')+ 
                        ' at '+Utils.StrPos(t[3])+'\nAssuming "0"',
                        prefix='Warning:')
            sh.starhomescore = 0
    else:
        sh.starhomescore = 0
    if t[1].has_key('starmcscore'):
        try:
            sh.starmcscore = int(t[1]['starmcscore'])
        except:
            Utils.Error('Value of "starmcscore" attribute is no integer: '+
                        t[1]['starmcscore'].encode('ISO-8859-1','replace')+ 
                        ' at '+Utils.StrPos(t[3])+'\nAssuming "0"',
                        prefix='Warning:')
            sh.starmcscore = 0
    else:
        sh.starmcscore = 0

    counter = sh.first
    for a in t[2]:
        if type(a) == types.UnicodeType:   # this will probably not happen!
            pass        # because we have "element content" here.
        elif a[0] == 'TEXT':
            sh.list.append(MakeTeXText(a,Config.conf['WidthOfSheetsHTML']))
            sh.exnr.append(None)
            sh.order.append(None)
            sh.nrquestions.append(None)
        elif a[0] == 'EXERCISE':
            ke = a[1]['key'].encode('ISO-8859-1','replace')
            if a[1].has_key('prefix'):
                ke = a[1]['prefix'].encode('ISO-8859-1','replace') + ke
            if not(AllExercises.has_key(ke)):
                Utils.Error('Unknown exercise "'+ke+'" needed by sheet at '+
                            Utils.StrPos(a[3])+'\nIgnoring sheet.')
                raise Utils.UtilsError
            sh.list.append(AllExercises[ke])
            if a[1].has_key('order'):
                if a[1]['order'][0] == 'f' or a[1]['order'][0] == 'F':
                    sh.order.append('f')
                else:
                    sh.order.append('p')
            else:
                sh.order.append('p')
            nrques = AllExercises[ke].nrquestions
            if a[1].has_key('nrquestions'):
                try:
                    nrques = int(a[1]['nrquestions'])
                except:
                    Utils.Error('Value of "nrquestions" attribute is no '
                                'integer: '+
                                a[1]['nrquestions'].encode('ISO-8859-1',
                                                           'replace')+
                                'assuming default '+str(nrques)+' at '+
                                Utils.StrPos(a[3]),prefix='Warning:')
            sh.nrquestions.append(nrques)
            sh.exnr.append(counter)
            counter += 1
        elif a[0] == 'INCLUDE':
            fi = a[1]['file'].encode('ISO-8859-1','replace')
            if a[1].has_key('prefix'):
                fi = a[1]['prefix'].encode('ISO-8859-1','replace') + fi
            if not(AllExercises.has_key(fi)):
                Utils.Error('Unknown exercise "'+fi+'" needed by sheet at '+
                            Utils.StrPos(a[3])+'\nIgnoring sheet.')
                raise Utils.UtilsError
            sh.list.append(AllExercises[fi])
            sh.exnr.append(counter)
            sh.order.append(None)
            sh.nrquestions.append(None)
            counter += 1
    # now put into AllExercises
    AllSheets.append(sh)

# We distinguish the two cases where several (enclosed by a <SHEETS>
# tag) or just one <SHEET> is contained in the file fname.
def ReadSheetsFile(fname):
  # Parsing and validating the content of an .bla file
  tree = XMLRewrite.Parse(Parser, file = fname)
  if not tree:
      Utils.Error('Cannot read or parse sheet(s) file '+fname+'.')
      return

  # Now we can be sure that the "tree" contains data of a valid sheets
  # document.
  if tree[0] == 'SHEETS':
      for a in tree[2]:
          if type(a) == types.TupleType and a[0] == 'SHEET':
               try:
                   MakeSheet(a)
               except:   # may fail, error is already reported
                   traceback.print_exc()
                   Utils.Error("Exception raised.")
  elif tree[0] == 'SHEET':
      try:
          MakeSheet(tree)
      except:   # may fail, error is already reported
          traceback.print_exc()
          Utils.Error("Exception raised.")

# Read all *.bla files in a directory. 
# Note that we ignore all errors here, including those that occur because
# some exercise required by a sheet was not there. They are reported to the
# user but offending sheets will just not exist later on.
def ReadSheetsDirectory(dirname):
    for fname in glob.glob(os.path.join(dirname, '*.bla')):
        ReadSheetsFile(fname)

# A utility that creates for all entries in AllTexts images in .png
# format. The image directory, the textwidth for LaTeX in inches and the 
# resolution in dots per inch must be given. Without showdots == 0 the
# progress is shown by one dot
def CreateAllImages(showdots = 1):
  for a in AllTexts:
      a.MakeImages(os.path.join(Config.conf['DocumentRoot'],"images"),
                   Config.conf['Resolutions'])

