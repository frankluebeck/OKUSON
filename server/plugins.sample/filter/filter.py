# -*- coding: utf-8 -*-

import Config, Data, Exercises, Plugins
from fmTools import Utils, LatexImage
import locale, smtplib, string, time

def stringtosortkey (s):
  sortkeylist = []
  currenttype = None
  for bst in s.lower():
    if bst == "ä".decode("utf_8").encode("latin_1"): bst = "ae"
    if bst == "ö".decode("utf_8").encode("latin_1"): bst = "oe"
    if bst == "ü".decode("utf_8").encode("latin_1"): bst = "ue"
    if bst == "ß".decode("utf_8").encode("latin_1"): bst = "ss"
    if "a" <= bst <= "z":
      if currenttype <> "character": sortkeylist.append ("")
      sortkeylist[-1] += bst
      currenttype = "character"
    elif "0" <= bst <= "9":
      if currenttype not in ["digit", "digitasstring"]: sortkeylist.append (0)
      if currenttype == "digitasstring":
        sortkeylist[-1] += bst
      else:
        sortkeylist[-1] = sortkeylist[-1] * 10 + int(bst)
        currenttype = "digit"
    elif bst in [".", ","] and currenttype == "digit":
      sortkeylist.append ("")
      currenttype = "digitasstring"
    elif bst == " ":
      sortkeylist.append ("")
      currenttype = None
  return tuple(sortkeylist)


def outputstring (s, masklist = [], deletecolon = True):
  ml = masklist[:] + [('\n', '')]
  if deletecolon: ml += [(':', '')]
  for char, mask in ml:
    s = s.replace(char, mask)
  return s


class Filter (Plugins.OkusonExtension):
  def __init__ (self, options = {}):
    self.__options = options
    try:
      self.__msg = options["msg"][0]
    except:
      #self.__msg = ""
      self.__msg = "%i:%n:%f"
    try:
      if options["submit"][0] == "get HTML output":
        self.__exporttype = "html"
      if options["submit"][0] == "get text file":
        self.__exporttype = "text"
      if options["submit"][0] == "get CSV file":
        self.__exporttype = "csv"
      if options["submit"][0] == "get LaTeX file":
        self.__exporttype = "latex"
      if options["submit"][0] == "get PDF file":
        self.__exporttype = "pdf"
    except:
      self.__exporttype = "html"
    try:
      if options["shortcolhead"][0] == "yes":
        self.__shortcolhead = True
      else:
        self.__shortcolhead = False
    except:
      self.__shortcolhead = False
    try:
      self.__sortkey = "%" + options["sortkey1"][0]
      try:
        self.__sortkey += " %" + options["sortkey2"][0]
      except:
        pass
    except:
      self.__sortkey = "%i"
    self.__sortkey = self.__sortkey.strip()
    self.__fieldlist = 5 * [None]
    self.__rellist = 5 * [None]
    self.__vallist = 5 * [""]
    for i in range(5):
      try:
        self.__fieldlist[i] = options["field%d" % i][0]
        if self.__fieldlist[i] == "none": self.__fieldlist[i] = None
      except:
        pass
      try:
        self.__rellist[i] = options["relation%d" % i][0]
        if self.__rellist[i] == "none": self.__rellist[i] = None
      except:
        pass
      try:
        self.__vallist[i] = options["value%d" % i][0]
      except:
        pass

  def name (self):
    return self.__class__.__name__

  def necessaryCredentials (self):
    return Plugins.Admin

  def returnType (self):
    if self.__exporttype == "html":
      return Plugins.HTML
    if self.__exporttype in ["text", "csv", "latex", "pdf"]:
      return Plugins.File

  def title (self):
    return "List participants fulfilling certain conditions"

  def formCode (self):
    return "List participants fulfilling certain conditions"

  def cssCode (self):
    return ""

  def __varinit (self):
    self.__varlist = ["i", "n", "f", "s", "g", "a", "m"]
    self.__vartofieldtitle = {}
    self.__vartofieldtitle["i"] = "ID"
    self.__vartofieldtitle["n"] = "last name"
    self.__vartofieldtitle["f"] = "first name"
    self.__vartofieldtitle["s"] = "semester"
    self.__vartofieldtitle["g"] = "group"
    self.__vartofieldtitle["a"] = "field of studies"
    self.__vartofieldtitle["m"] = "email address"
    for sheetnr, sheetname, sheet in Exercises.SheetList():
      if not sheet.IsClosed(): continue
      if not sheet.counts: continue
      self.__varlist.append (str(sheetnr) + "c")
      self.__vartofieldtitle[str(sheetnr) + "c"] = "points from interactive " \
       "part of exercise sheet " + str(sheetnr)
    self.__varlist.append ("C")
    self.__vartofieldtitle["C"] = "total points from interactive exercises"
    for sheetnr, sheetname, sheet in Exercises.SheetList():
      if not sheet.IsClosed(): continue
      if not sheet.counts: continue
      self.__varlist.append (str(sheetnr) + "h")
      self.__vartofieldtitle[str(sheetnr) + "h"] = "points from written " \
       "homework part of exercise sheet " + str(sheetnr)
    self.__varlist.append ("H")
    self.__vartofieldtitle["H"] = "total points from written homework exercises"
    self.__varlist.append ("T")
    self.__vartofieldtitle["T"] = "total points from written and interactive " \
     "exercises"
    for i in range(Data.Exam.maxexamnumber):
      self.__varlist.append (str(i) + "e")
      self.__vartofieldtitle[str(i) + "e"] = "points from exam " + str(i)
    self.__varlist.append ("E")
    self.__vartofieldtitle["E"] = "total points from exams"
    for i in range(Data.Exam.maxexamnumber):
      self.__varlist.append (str(i) + "r")
      self.__vartofieldtitle[str(i) + "r"] = "registered for exam " + str(i) + \
       " (no/yes)"
    self.__persondatakeys = []
    for k in Data.people.keys():
      for key in Data.people[k].persondata.keys():
        if key not in self.__persondatakeys: self.__persondatakeys.append (key)
    self.__persondatakeys.sort ()
    for i in range(len(self.__persondatakeys)):
      self.__varlist.append ("%dd" % i)
      self.__vartofieldtitle[self.__varlist[-1]] = self.__persondatakeys[i]

  def __filteroutput (self, type = "html"):
    tablerowbeforefirst = '<tr>\n'
    tablerowinbetween = '\n</tr>\n<tr>\n'
    tablerowafterlast = '\n</tr>\n'
    tablecellbeforefirst = '<td>'
    tablecellinbetween = '</td><td>'
    tablecellafterlast = '</td>'
    tableheadinbetween = '</th><th>'
    reltext = {'equal': '=', 'greater': '&gt;', 'greaterequal': '&gt;=',
     'less': '&lt;', 'lessequal': '&lt;=', 'notequal': 'not equal to',
     'begins': 'begins with', 'contains': 'contains', 'ends': 'ends with'}
    masklist = [('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;')]
    if type == "text":
      tablerowbeforefirst = ''
      tablerowinbetween = '\n'
      tablerowafterlast = '\n'
      tablecellbeforefirst = ''
      tablecellinbetween = ':'
      tablecellafterlast = ''
      tableheadinbetween = ':'
      reltext = {'equal': '=', 'greater': '>', 'greaterequal': '>=',
       'less': '<', 'lessequal': '<=', 'notequal': 'not equal to',
       'begins': 'begins with', 'contains': 'contains', 'ends': 'ends with'}
      masklist = []
    if type == "csv":
      tablerowbeforefirst = ''
      tablerowinbetween = '\n'
      tablerowafterlast = '\n'
      tablecellbeforefirst = '"'
      tablecellinbetween = '";"'
      tablecellafterlast = '"'
      tableheadinbetween = '";"'
      reltext = {'equal': '=', 'greater': '>', 'greaterequal': '>=',
       'less': '<', 'lessequal': '<=', 'notequal': 'not equal to',
       'begins': 'begins with', 'contains': 'contains', 'ends': 'ends with'}
      masklist = []
    if type == "latex":
      tablerowbeforefirst = ''
      tablerowinbetween = ' \\\\\n'
      tablerowafterlast = '\n'
      tablecellbeforefirst = ''
      tablecellinbetween = ' & '
      tablecellafterlast = ''
      tableheadinbetween = '} & \\textbf{'
      reltext = {'equal': '$=$', 'greater': '$>$', 'greaterequal': '$\\geq$',
       'less': '$<$', 'lessequal': '$\\leq$', 'notequal': '$\\neq$',
       'begins': 'begins with', 'contains': 'contains', 'ends': 'ends with'}
      masklist = [('\\', '\\textbackslash '), ('{', '\\{'), ('}', '\\}'),
       ('\\textbackslash ', '\\textbackslash{}'), ('"', '\\textquotedbl{}'),
       ('#', '\\#'), ('$', '\\$'), ('%', '\\%'), ('&', '\\&'),
       ('<', '\\textless{}'), ('>', '\\textgreater{}'), ('[', '\\relax['),
       (']', '\\relax]'), ('^', '\\^{}'), ('_', '\\_'), ('|', '\\textbar{}'),
       ('~', '\\~{}')]
    totalcount = 0
    filtercount = 0
    resultlist = []
    for k in Utils.SortNumerAlpha(Data.people.keys()):
      p = Data.people[k]
      vardict = {}
      vardict["i"] = k
      vardict["n"] = p.lname
      vardict["f"] = p.fname
      vardict["s"] = p.sem
      vardict["g"] = p.group
      vardict["a"] = p.stud
      vardict["m"] = p.email
      totalintscore = 0.0
      for sheetnr, sheetname, sheet in Exercises.SheetList():
        if not sheet.IsClosed(): continue
        if not sheet.counts: continue
        vardict[str(sheetnr) + "c"] = -1
        if p.mcresults.has_key(sheetname):
          vardict[str(sheetnr) + "c"] = p.mcresults[sheetname].score
          totalintscore += p.mcresults[sheetname].score
      vardict["C"] = totalintscore
      totalhomescore = 0.0
      for sheetnr, sheetname, sheet in Exercises.SheetList():
        if not sheet.IsClosed(): continue
        if not sheet.counts: continue
        vardict[str(sheetnr) + "h"] = -1
        if p.homework.has_key(sheetname) and \
         p.homework[sheetname].totalscore <> -1:
          vardict[str(sheetnr) + "h"] = p.homework[sheetname].totalscore
          totalhomescore += p.homework[sheetname].totalscore
      vardict["H"] = totalhomescore
      vardict["T"] = totalintscore + totalhomescore
      totalexamscore = 0.0
      for i in range(Data.Exam.maxexamnumber):
        if i >= len(p.exams) or p.exams[i] == None or \
         p.exams[i].totalscore < 0:
          vardict[str(i) + "e"] = -1
        else:
          vardict[str(i) + "e"] = p.exams[i].totalscore
          totalexamscore += p.exams[i].totalscore
        vardict[str(i) + "r"] = "no"
        if i < len(p.exams) and p.exams[i] <> None:
          if p.exams[i].registration == 1:
            vardict[str(i) + "r"] = "yes"
      vardict["E"] = totalexamscore
      for i in range(len(self.__persondatakeys)):
        try:
          vardict["%dd" % i] = p.persondata[self.__persondatakeys[i]]
        except:
          vardict["%dd" % i] = ""
      filter = True
      for i in range(5):
        if self.__fieldlist[i] <> None:
          val1 = vardict[self.__fieldlist[i]]
          val2 = self.__vallist[i]
          if len(val2) >= 2 and val2[0] == '"' and val2[-1] == '"':
            val2 = val2[1:-1]
            val1 = str(val1)
          else:
            try:
              val1 = int(val1)
              val2 = int(val2)
            except:
              try:
                val1 = float(val1)
                val2 = float(val2)
              except:
                pass
          if self.__rellist[i] == "equal":
            if not val1 == val2: filter = False
          if self.__rellist[i] == "greater":
            if not val1 > val2: filter = False
          if self.__rellist[i] == "greaterequal":
            if not val1 >= val2: filter = False
          if self.__rellist[i] == "less":
            if not val1 < val2: filter = False
          if self.__rellist[i] == "lessequal":
            if not val1 <= val2: filter = False
          if self.__rellist[i] == "notequal":
            if not val1 <> val2: filter = False
          if self.__rellist[i] == "begins":
            if not str(val1)[:len(str(val2))] == str(val2): filter = False
          if self.__rellist[i] == "contains":
            if not str(val2) in str(val1): filter = False
          if self.__rellist[i] == "ends":
            if not str(val1)[-len(str(val2)):] == str(val2): filter = False
      totalcount += 1
      if filter:
        filtercount += 1
        sortkey = self.__sortkey.replace("%%", "_!_/_")
        for var in vardict.keys():
          sortkey = sortkey.replace("%%%s" % var, str(vardict[var]))
        sortkey = sortkey.replace("_!_/_", "%")
        sortkey = stringtosortkey(sortkey)
        msg = self.__msg.replace("%%", "_!_/_")
        for var in vardict.keys():
          if var[-1:] in ["i", "n", "f", "a", "m", "r", "d"]:
            msg = msg.replace('%%%s' % var, Utils.Protect(str(vardict[var])))
          elif var[-1:] in ["s", "g"]:
            msg = msg.replace("%%%s" % var, str(vardict[var]))
          else:
            msg = msg.replace("%%%s" % var, locale.str(vardict[var]))
        msg = outputstring(msg, masklist, deletecolon = False)
        msg = msg.replace(":", tablecellinbetween)
        msg = msg.replace("_!_/_", "%")
        resultlist.append ([sortkey, (k, p.lname, p.fname, msg)])
    resultlist.sort ()
    filteroutput = tablerowbeforefirst
    isfirst = True
    for sortkey, (k, ln, fn, msg) in resultlist:
      if not isfirst: filteroutput += tablerowinbetween
      isfirst = False
      filteroutput += tablecellbeforefirst
      #filteroutput += outputstring(k, masklist)
      #filteroutput += tablecellinbetween
      #filteroutput += outputstring(ln, masklist)
      #filteroutput += tablecellinbetween
      #filteroutput += outputstring(fn, masklist)
      if self.__msg <> "":
        #filteroutput += tablecellinbetween
        filteroutput += msg
      filteroutput += tablecellafterlast
    filteroutput += tablerowafterlast
    filterinfo = ["", "", "", "", filtercount, totalcount]
    #filterinfo[0] = '%i:%n:%f'
    #if self.__msg <> "": filterinfo[0] += ":" + self.__msg
    filterinfo[0] = self.__msg
    if not self.__shortcolhead:
      for var, fieldtitle in self.__vartofieldtitle.iteritems():
        filterinfo[0] = filterinfo[0].replace("%%%s" % var, 
         Utils.Protect(fieldtitle))
    filterinfo[0] = outputstring(filterinfo[0], masklist, deletecolon = False)
    filterinfo[0] = filterinfo[0].replace(":", tableheadinbetween)
    filtercriteria = []
    for i in range(5):
      if self.__fieldlist[i] <> None and self.__rellist[i] <> None:
        filtercriteria.append \
         (outputstring(self.__vartofieldtitle[self.__fieldlist[i]], masklist))
        filtercriteria[-1] += " " + reltext[self.__rellist[i]]
        filtercriteria[-1] += " " + outputstring(self.__vallist[i], masklist)
    if filtercriteria <> []:
      filterinfo[1] = " and ".join(filtercriteria)
    filterinfo[2] = self.__sortkey.replace(" ", ", ")
    for var, fieldtitle in self.__vartofieldtitle.iteritems():
      filterinfo[2] = filterinfo[2].replace("%%%s" % var, 
       outputstring(fieldtitle, masklist))
    filterinfo[3] = Utils.LocalTimeString()
    return filterinfo, filteroutput

  def htmlCode (self):
    html = ''
    html += '<p>'
    html += '(<a href="/adminmenu.html">back to administrator menu</a>)'
    html += '&nbsp;&nbsp;'
    html += '(<a href="/adminextensions.html">back to administrator ' + \
     'extensions</a>)'
    html += '</p>\n'
    self.__varinit ()
    filterinfo, filteroutput = self.__filteroutput(type = 'html')
    html += '<table>\n'
    html += '<tr>\n'
    html += '<th>%s</th>\n' % filterinfo[0]
    #html += '<th>ID</th><th>last name</th><th>first name</th><th>%s</th>\n' \
    # % self.__msg
    html += '</tr>\n'
    html += filteroutput
    html += '</table>\n'
    html += '<p>Filter matched %d of %s participants.</p>\n' % (filterinfo[4],
     filterinfo[5])
    html += '<form action="/AdminExtension" method="post" ' + \
     'accept-charset="ISO-8859-15">\n'
    html += '<div>\n'
    html += '<input type="hidden" name="extension" value="%s" />\n' % \
     self.name()
    html += '</div>\n'
    html += '<p>\n'
    html += 'Select participants who should be displayed.\n'
    html += 'The following conditions have all to be met simultaneously.\n'
    html += '(Please note that comparisons are interpreted as numerical '
    html += 'comparisons whenever it is possible. To force comparison of '
    html += 'texts, include the value in quotes ("..."))\n'
    html += 'If no condition is given, every participant will be listed.\n'
    html += '</p>\n'
    html += '<table>\n'
    for i in range(5):
      html += '<tr>\n'
      html += '<td>\n'
      html += '<select name="field%d">\n' % i
      html += '<option value="none">field</option>\n'
      for var in self.__varlist:
        if self.__fieldlist[i] == var:
          html += '<option value="%s" selected="selected">%s</option>\n' % \
           (var, self.__vartofieldtitle[var])
        else:
          html += '<option value="%s">%s</option>\n' % \
           (var, self.__vartofieldtitle[var])
      html += '</select>\n'
      html += '</td>\n'
      reqsel = ""
      rgtsel = ""
      rgesel = ""
      rltsel = ""
      rlesel = ""
      rnesel = ""
      rbgsel = ""
      rcosel = ""
      rensel = ""
      if self.__rellist[i] == "equal": reqsel = ' selected="selected"'
      if self.__rellist[i] == "greater": rgtsel = ' selected="selected"'
      if self.__rellist[i] == "greaterequal": rgesel = ' selected="selected"'
      if self.__rellist[i] == "less": rltsel = ' selected="selected"'
      if self.__rellist[i] == "lessequal": rlesel = ' selected="selected"'
      if self.__rellist[i] == "notequal": rnesel = ' selected="selected"'
      if self.__rellist[i] == "begins": rbgsel = ' selected="selected"'
      if self.__rellist[i] == "contains": rcosel = ' selected="selected"'
      if self.__rellist[i] == "ends": rensel = ' selected="selected"'
      html += '<td>\n'
      html += '<select name="relation%s">\n' % i
      html += '<option value="none">relation</option>\n'
      html += '<option value="equal"%s>=</option>\n' % reqsel
      html += '<option value="greater"%s>&gt;</option>\n' % rgtsel
      html += '<option value="greaterequal"%s>&gt;=</option>\n' % rgesel
      html += '<option value="less"%s>&lt;</option>\n' % rltsel
      html += '<option value="lessequal"%s>&lt;=</option>\n' % rlesel
      html += '<option value="notequal"%s>not equal to</option>\n' % rnesel
      html += '<option value="begins"%s>begins with</option>\n' % rbgsel
      html += '<option value="contains"%s>contains</option>\n' % rcosel
      html += '<option value="ends"%s>ends with</option>\n' % rensel
      html += '</select>\n'
      html += '</td>\n'
      html += '<td>\n'
      html += '<input type="text" name="value%d" size="30" value="%s" />' % \
       (i, self.__vallist[i].replace("&", "&amp;").replace("<", 
       "&lt;").replace(">", "&gt;").replace('"', "&quot;"))
      html += '</td>\n'
      html += '</tr>\n'
    html += '</table>\n'
    html += '<p>\n'
    html += 'In the following text field you may use variables.<br />\n'
    html += '<strong>%i</strong>: ID'
    html += '; <strong>%n</strong>: last name'
    html += '; <strong>%f</strong>: first name'
    html += '; <strong>%s</strong>: semester'
    html += '; <strong>%g</strong>: group'
    html += '; <strong>%a</strong>: field of studies'
    html += '; <strong>%m</strong>: email address'
    html += '; <strong>%1c</strong>, <strong>%2c</strong>, ...: points ' \
     'from interactive part of exercise sheet 1, 2, ...'
    html += '; <strong>%C</strong>: total points from interactive exercises'
    html += '; <strong>%1h</strong>, <strong>%2h</strong>, ...: points ' \
     'from written homework part of exercise sheet 1, 2, ...'
    html += '; <strong>%H</strong>: total points from written homework ' \
     'exercises'
    html += '; <strong>%T</strong>: total points from interactive and ' \
     'written homework exercises'
    html += '; <strong>%0e</strong>, <strong>%1e</strong>, ...: points ' \
     'from exam 0, 1, ...'
    html += '; <strong>%E</strong>: total points from exams'
    for i in range(len(self.__persondatakeys)):
      html += '; <strong>%%%dd</strong>: %s' % (i, self.__persondatakeys[i])
    html += '.\n'
    html += '(In order to produce a %-sign, type ' \
     '<strong>%%</strong>.)\n'
    html += 'Use <strong>:</strong> as column separator.\n'
    html += '</p>\n'
    #html += ('<p>additional information to be displayed:' +
    html += ('<p>information to be displayed:' +
     '&nbsp;<input type="text" ' + 'name="msg" ' + 
     'size="40" value="%s" /></p>\n') % self.__msg.replace("&",
     "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    html += '<p><input type="checkbox" name="shortcolhead" value="yes" '
    if self.__shortcolhead:
      html += 'checked="checked"'
    html += '/>&nbsp;short column headers</p>\n'
    html += '<p>\n'
    html += 'sort by&nbsp;\n'
    html += '<select name="sortkey1">\n'
    html += '<option value=""></option>\n'
    for var in self.__varlist:
      if self.__sortkey.split(" ")[0][1:] == var:
        html += '<option value="%s" selected="selected">%s</option>\n' % \
         (var, self.__vartofieldtitle[var])
      else:
        html += '<option value="%s">%s</option>\n' % \
         (var, self.__vartofieldtitle[var])
    html += '</select>,\n'
    html += 'then by&nbsp;\n'
    html += '<select name="sortkey2">\n'
    html += '<option value=""></option>\n'
    for var in self.__varlist:
      if len(self.__sortkey.split(" ")) > 1 and \
       self.__sortkey.split(" ")[-1][1:] == var:
        html += '<option value="%s" selected="selected">%s</option>\n' % \
         (var, self.__vartofieldtitle[var])
      else:
        html += '<option value="%s">%s</option>\n' % \
         (var, self.__vartofieldtitle[var])
    html += '</select>\n'
    html += '</p>\n'
    html += '<p>administrator password: <input type="password" ' + \
     'size="16" maxlength="16" name="passwd" value="" />' + \
     '&nbsp;<input type="submit" name="submit" value="get HTML output" />' + \
     '&nbsp;<input type="submit" name="submit" value="get text file" />' + \
     '&nbsp;<input type="submit" name="submit" value="get CSV file" />' + \
     '&nbsp;<input type="submit" name="submit" value="get LaTeX file" />' + \
     '&nbsp;<input type="submit" name="submit" value="get PDF file" />'
    html += '</p>\n'
    html += '</form>\n'
    return html

  def headAndBody (self):
    s = ''
    head = {}
    if self.__exporttype == "text":
      self.__varinit ()
      filterinfo, filteroutput = self.__filteroutput(type = "text")
      s = '# columns: ' + filterinfo[0] + '\n'
      if filterinfo[1] <> "":
        s += '# filter criterion: ' + filterinfo[1] + '\n'
      else:
        s += '# filter criterion: ALL\n'
      s += '# matches: %d of %d participants\n' % (filterinfo[4],
       filterinfo[5])
      if self.__sortkey.count("%") == 1:
        s += '# sort key: ' + filterinfo[2] + '\n'
      elif self.__sortkey.count("%") == 2:
        s += '# sort keys: ' + filterinfo[2] + '\n'
      s += '# time and date of export: ' + filterinfo[3] + '\n'
      s += filteroutput
      head['Content-type'] = 'text/plain'
      head['Content-Disposition'] = 'attachment; filename="export.txt"'
    if self.__exporttype == "csv":
      self.__varinit ()
      filterinfo, filteroutput = self.__filteroutput(type = "csv")
      s = '"' + filterinfo[0] + '"\n' + filteroutput
      head['Content-type'] = 'text/csv'
      head['Content-Disposition'] = 'attachment; filename="export.csv"'
    if self.__exporttype in ["latex", "pdf"]:
      self.__varinit ()
      filterinfo, filteroutput = self.__filteroutput(type = "latex")
      maxcolumns = 0
      for row in filteroutput.split("\\\\"):
        if row.count(" & ") >= maxcolumns: maxcolumns = row.count(" & ") + 1
      latex = '\\documentclass[10pt, DIV20, parskip-]{scrartcl}\n\n'
      latex += '\\usepackage[latin9]{inputenc}\n'
      latex += '\\usepackage[T1]{fontenc}\n'
      latex += '\\usepackage{mathptmx}\n'
      latex += '\\usepackage{textcomp}\n'
      latex += '\\usepackage[ngerman]{babel}\n'
      latex += '\\usepackage{array}\n\n'
      latex += '\\usepackage{longtable}\n'
      latex += '\\begin{document}\n'
      latex += '\\centering\n'
      latex += '\\hrule\n'
      latex += '\\vspace*{-0.7\\baselineskip}\n'
      latex += '{\\LARGE\\bfseries List of participants\\par}\n'
      latex += '\\vspace*{0.25\\baselineskip}\n'
      latex += '\\hrule\n'
      latex += '\\vspace*{1\\baselineskip}\n'
      latex += '\\begin{tabular}{ll}\n'
      if filterinfo[1] <> "":
        latex += '\\textbf{filter criterion:} & ' + filterinfo[1] + ' \\\\\n'
      else:
        latex += '\\textbf{filter criterion:} & ALL \\\\\n'
      latex += '\\textbf{matches:} & %d of %d participants \\\\\n' % \
       (filterinfo[4], filterinfo[5])
      if self.__sortkey.count("%") == 1:
        latex += '\\textbf{sort key:} & ' + filterinfo[2] + ' \\\\\n'
      elif self.__sortkey.count("%") == 2:
        latex += '\\textbf{sort keys:} & ' + filterinfo[2] + ' \\\\\n'
      latex += '\\textbf{time and date of export:} & ' + filterinfo[3] + \
       ' \\\\\n'
      latex += '\\end{tabular}\n\n'
      latex += '\\vspace*{1\\baselineskip}\n'
      latex += '\\begin{longtable}{' + maxcolumns * 'l' + '}\n'
      latex += '\\hline\n'
      latex += '\\textbf{' + filterinfo[0] + '}\\\\\n'
      latex += '\\hline\n'
      latex += '\\endhead\n'
      latex += filteroutput
      latex += '\\end{longtable}\n'
      latex += '\\end{document}\n'
      if self.__exporttype == "pdf":
        s = LatexImage.LatexToPDF(latex)
        head['Content-type'] = 'application/pdf'
        head['Content-Disposition'] = 'attachment; filename="export.pdf"'
      else:
        s = latex
        head['Content-type'] = 'application/x-latex'
        head['Content-Disposition'] = 'attachment; filename="export.tex"'
    return (head, s)


Plugins.register (Filter.__name__, "Output/Export",
 "List participants fulfilling certain conditions",
 "This plugin serves for listing participants that fulfil certain conditions.",
 "Marc Ensenbach", "Marc Ensenbach", "2008", Filter)
