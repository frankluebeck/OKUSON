import Config, Data, Exercises, Plugins
from fmTools import Utils
import smtplib, string, time

defaultserver = "relay.rwth-aachen.de"

class Mailer (Plugins.OkusonExtension):
  def __init__ (self, options = {}):
    self.__options = options
    try:
      self.__state = int(options["state"][0])
    except:
      self.__state = 0
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
    try:
      self.__server = options["server"][0]
    except:
      self.__server = defaultserver
    try:
      self.__username = options["username"][0]
    except:
      self.__username = ""
    try:
      self.__mailpw = options["mailpw"][0]
    except:
      self.__mailpw = ""
    try:
      self.__pause = int(options["pause"][0])
    except:
      self.__pause = 0
    try:
      self.__from = options["from"][0]
    except:
      self.__from = ""
    try:
      self.__fromname = options["fromname"][0]
    except:
      self.__fromname = ""
    try:
      self.__subject = options["subject"][0]
    except:
      self.__subject = ""
    try:
      self.__text = options["text"][0]
    except:
      self.__text = "Text"

  def name (self):
    return self.__class__.__name__

  def necessaryCredentials (self):
    return Plugins.Admin

  def returnType (self):
    return Plugins.HTML

  def title (self):
    return "Sending (personalised) mail to participants"

  def formCode (self):
    return "Sending (personalised) mail to participants"

  def cssCode (self):
    return ""

  def htmlCode (self):
    html = ''
    try:
      smtpserver = smtplib.SMTP(self.__server)
      if self.__username <> "" and self.__mailpw <> "":
        smtpserver.login (self.__username, self.__mailpw)
    except:
      smtpserver = None
      html += '<p>Error: Could not contact the server %s</p>\n' % self.__server
    html += '<p>'
    html += '(<a href="/adminmenu.html">back to administrator menu</a>)'
    html += '&nbsp;&nbsp;'
    html += '(<a href="/adminextensions.html">back to administrator ' + \
     'extensions</a>)'
    html += '</p>\n'
    varlist = ["i", "n", "f", "s", "g", "a", "m"]
    vartofieldtitle = {}
    vartofieldtitle["i"] = "ID"
    vartofieldtitle["n"] = "last name"
    vartofieldtitle["f"] = "first name"
    vartofieldtitle["s"] = "semester"
    vartofieldtitle["g"] = "group"
    vartofieldtitle["a"] = "field of studies"
    vartofieldtitle["m"] = "mail address"
    for sheetnr, sheetname, sheet in Exercises.SheetList():
      if not sheet.IsClosed(): continue
      if not sheet.counts: continue
      varlist.append (str(sheetnr) + "c")
      vartofieldtitle[str(sheetnr) + "c"] = "points from interactive " \
       "part of exercise sheet " + str(sheetnr)
    varlist.append ("C")
    vartofieldtitle["C"] = "total points from interactive exercises"
    for sheetnr, sheetname, sheet in Exercises.SheetList():
      if not sheet.IsClosed(): continue
      if not sheet.counts: continue
      varlist.append (str(sheetnr) + "h")
      vartofieldtitle[str(sheetnr) + "h"] = "points from written homework " \
       "part of exercise sheet " + str(sheetnr)
    varlist.append ("H")
    vartofieldtitle["H"] = "total points from written homework exercises"
    varlist.append ("T")
    vartofieldtitle["T"] = "total points from written and interactive exercises"
    for i in range(Data.Exam.maxexamnumber):
      varlist.append (str(i) + "e")
      vartofieldtitle[str(i) + "e"] = "points from exam " + str(i)
    varlist.append ("E")
    vartofieldtitle["E"] = "total points from exams"
    for i in range(Data.Exam.maxexamnumber):
      varlist.append (str(i) + "r")
      vartofieldtitle[str(i) + "r"] = "registered for exam " + str(i) + \
       " (no/yes)"
    persondatakeys = []
    for k in Data.people.keys():
      for key in Data.people[k].persondata.keys():
        if key not in persondatakeys: persondatakeys.append (key)
    persondatakeys.sort ()
    for i in range(len(persondatakeys)):
      varlist.append ("%dd" % i)
      vartofieldtitle[varlist[-1]] = persondatakeys[i]
    if self.__state > 0 and smtpserver <> None:
      fullfrom = self.__from
      maillist = []
      if self.__fromname <> "":
        fullfrom = "%s <%s>" % (self.__fromname, self.__from)
      if self.__state % 2 == 1:
        html += '<p>Please confirm that the following participants should ' \
         'receive a mail.</p>\n'
      else:
        html += '<p>Tried to send last mail to the following ' \
         'participants:</p>\n'
      html += '<table>\n'
      html += '<tr>\n'
      html += \
       '<th>ID</th><th>last name</th><th>first name</th><th>status</th>\n'
      html += '</tr>\n'
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
        for i in range(len(persondatakeys)):
          try:
            vardict["%dd" % i] = p.persondata[persondatakeys[i]]
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
        if filter and p.email <> "":
          msg = "From: %s\r\n" % fullfrom
          msg += "Subject: %s\r\n" % self.__subject
          msg += "To: %s\r\n" % p.email
          msg += "Content-type: text/plain; charset=iso-8859-15\r\n"
          msg += "\r\n"
          msg += self.__text
          msg = msg.replace("%%", "_!_/_")
          usedvar = False
          for var in vardict.keys():
            if ("%%%s" % var) in msg: usedvar = True
            msg = msg.replace("%%%s" % var, str(vardict[var]))
          msg = msg.replace("_!_/_", "%")
          msg = msg.strip() + "\r\n"
          html += '<tr>\n'
          if self.__state % 2 == 1:
            status = "not yet sent"
          else:
            status = "successful"
            if usedvar:
              try:
                smtpserver.sendmail (fullfrom, p.email, msg)
                time.sleep (self.__pause)
              except:
                status = "<strong>not successful</strong>"
            else:
              maillist.append (p.email)
              status = "BCC"
          html += '<td>%s</td><td>%s</td><td>%s</td><td>%s</td>\n' % (k, \
           p.lname, p.fname, status)
          html += '</tr>\n'
      html += '</table>\n'
      if maillist <> [] and self.__state % 2 == 0:
        msg = "From: %s\r\n" % fullfrom
        msg += "Subject: %s\r\n" % self.__subject
        msg += "To: %s\r\n" % fullfrom
        msg += "BCC: %s\r\n" % string.join(maillist, ", ")
        msg += "Content-type: text/plain; charset=iso-8859-15\r\n"
        msg += "\r\n"
        msg += self.__text
        msg = msg.replace("%%", "%")
        msg = msg.strip() + "\r\n"
        try:
          smtpserver.sendmail (fullfrom, [fullfrom] + maillist, msg)
          pass
        except:
          html = html.replace("BCC", "<strong>not successful</strong>")
      smtpserver.quit ()
    html += '<form action="/AdminExtension" method="post" ' + \
     'accept-charset="ISO-8859-15">\n'
    html += '<div>\n'
    html += '<input type="hidden" name="extension" value="%s" />\n' % \
     self.name()
    html += '<input type="hidden" name="state" value="%d" />\n' % \
     (self.__state + 1)
    html += '</div>\n'
    if self.__state % 2 == 0:
      html += '<p>\n'
      html += 'Select participants who should receive a mail.\n'
      html += 'The following conditions have all to be met simultaneously.\n'
      html += '(Please note that comparisons are interpreted as numerical '
      html += 'comparisons whenever it is possible. To force comparison of '
      html += 'texts, include the value in quotes ("..."))\n'
      html += 'If no condition is given, every participant will receive '
      html += 'a mail.\n'
      html += '</p>\n'
      html += '<table>\n'
      for i in range(5):
        html += '<tr>\n'
        html += '<td>\n'
        html += '<select name="field%d">\n' % i
        html += '<option value="none">field</option>\n'
        for var in varlist:
          if self.__fieldlist[i] == var:
            html += '<option value="%s" selected="selected">%s</option>\n' % \
             (var, vartofieldtitle[var])
          else:
            html += '<option value="%s">%s</option>\n' % \
             (var, vartofieldtitle[var])
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
         (i, self.__vallist[i])
        html += '</td>\n'
        html += '</tr>\n'
      html += '</table>\n'
      html += ('<p>server:&nbsp;<input type="text" name="server" ' + 
       'size="40" value="%s" /></p>\n') % self.__server
      html += ('<p>user name for mail server (if needed):&nbsp;<input type=' +
       '"text" name="username" size="40" value="%s" /></p>\n') % self.__username
      html += ('<p>pause between two mails:&nbsp;<input type="text" ' + \
       'name="pause" size="5" value="%s" /> seconds</p>\n') % self.__pause
      html += ('<p>from address:&nbsp;<input type="text" name="from" ' +
       'size="40" value="%s" /></p>\n') % self.__from
      html += ('<p>from name (optional):&nbsp;<input type="text" ' +
       'name="fromname" size="40" value="%s" /></p>\n') % self.__fromname
      html += '<p>\n'
      html += 'In the following text fields you may use variables, '
      html += 'which are set according to the participant the mail '
      html += 'is sent to.<br />\n'
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
      for i in range(len(persondatakeys)):
        html += '; <strong>%%%dd</strong>: %s' % (i, persondatakeys[i])
      html += '.\n'
      html += '(In order to produce a %-sign, type ' \
       '<strong>%%</strong>.)<br />\n'
      html += 'If no variables are used, only one mail will be sent &ndash; '
      html += 'addressed to the from address with all recipients in a BCC ' \
       'list.\n'
      html += '</p>\n'
      html += ('<p>subject:&nbsp;<input type="text" ' + 'name="subject" ' +
       'size="40" value="%s" /></p>\n') % self.__subject
      html += '<p><textarea name="text" cols="50" rows="10">' + \
       self.__text + '</textarea></p>\n'
    else:
      html += '<table>\n'
      for i in range(5):
        html += '<tr>\n'
        if self.__fieldlist[i] in varlist:
          html += '<td>\n'
          html += '<input type="hidden" name="field%d" value="%s" />' % \
           (i, self.__fieldlist[i])
          html += vartofieldtitle[self.__fieldlist[i]] + "\n"
          html += '</td>\n'
        else:
          html += '<td>\n'
          html += ('<input type="hidden" name="field%d" value="none" ' + \
           '/>&nbsp;\n') % i
          html += '</td>\n'
        html += '<td>\n'
        html += '<input type="hidden" name ="relation%d" value="%s" />' % \
         (i, self.__rellist[i])
        if self.__rellist[i] == "equal": html += "="
        if self.__rellist[i] == "greater": html += "&gt;"
        if self.__rellist[i] == "greaterequal": html += "&gt;="
        if self.__rellist[i] == "less": html += "&lt;"
        if self.__rellist[i] == "lessequal": html += "&lt;="
        if self.__rellist[i] == "notequal": html += "not equal to"
        if self.__rellist[i] == "begins": html += "begins with"
        if self.__rellist[i] == "contains": html += "contains"
        if self.__rellist[i] == "ends": html += "ends with"
        html += '\n</td>\n'
        html += '<td>\n'
        html += '<input type="hidden" name="value%d" value="%s" />%s\n' % \
         (i, self.__vallist[i], self.__vallist[i])
        html += '</td>\n'
        html += '</tr>\n'
      html += '</table>\n'
      html += ('<p>server:&nbsp;<input type="hidden" name="server" ' + 
       'value="%s" />%s</p>\n') % (self.__server, self.__server)
      html += ('<p>user name for mail server (if needed):&nbsp;<input type=' +
       '"hidden" name="username" value="%s" />%s</p>\n') % (self.__username,
       self.__username)
      html += ('<p>password for mail server (if needed):&nbsp;<input type=' +
       '"password" name="mailpw" size="10" value="%s" /></p>\n') % self.__mailpw
      html += ('<p>pause between two mails:&nbsp;<input type="hidden" ' + \
       'name="pause" value="%s" />%s seconds</p>\n') % (self.__pause,
       self.__pause)
      html += ('<p>from address:&nbsp;<input type="hidden" name="from" ' +
       'value="%s" />%s</p>\n') % (self.__from, self.__from)
      html += ('<p>from name (optional):&nbsp;<input type="hidden" ' +
       'name="fromname" value="%s" />%s</p>\n') % (self.__fromname, 
       self.__fromname)
      html += ('<p>subject:&nbsp;<input type="hidden" ' + 'name="subject" ' +
       'value="%s" />%s</p>\n') % (self.__subject, self.__subject)
      html += '<p><textarea name="text" cols="50" rows="10" ' + \
       'readonly="readonly">' + self.__text + '</textarea></p>\n'
    html += '<p>administrator password: <input type="password" ' + \
     'size="16" maxlength="16" name="passwd" value="" />' + \
     '&nbsp;<input type="submit" /></p>\n'
    html += '</form>\n'
    return html


Plugins.register (Mailer.__name__, "Mail", "Mails to participants",
 "This plugin serves for sending (personalised) mails to participants.",
 "Marc Ensenbach", "Marc Ensenbach", "2007", Mailer)
