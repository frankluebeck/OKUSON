#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the place where all special web services are implemented.'''

CVS = '$Id: WebWorkers.py,v 1.9 2003/10/04 23:36:57 luebeck Exp $'

import os,sys,time,locale,traceback,random,crypt,string,Cookie,signal,cStringIO

import Config,Data,Exercises

from Tools import BuiltinWebServer, XMLRewrite, Utils, AsciiData, SimpleTemplate, LatexImage

def LocalTimeString(t = time.time()):
  return time.strftime("%c", time.localtime(t))

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# First we set our document root:
DocRoot = BuiltinWebServer.DocRoot = os.path.join(Config.home,'html')
ElHandlers = XMLRewrite.ElementHandlers_tpl
# We store an xml header with DOCTYPE for XTML 1.0 Strict into the
# class variable "begin" such that this is the global default header:
XMLRewrite.PreparsedXMLWebResponse.begin = \
'''<?xml version="1.0" encoding="ISO-8859-1"?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

'''

ValidatorIconText = '''<a href="http://validator.w3.org/check/referer">
<img src="/images/valid-xhtml10.png" alt="Valid XHTML 1.0!" 
     height="31" width="88" /></a>
'''
# Make the main site dictionary available here:

Site = BuiltinWebServer.Site


#############################################################################
#
# Generic element handlers:
#
# We inherit from XMLRewrite.XMLElementHandlers and add a few element
# handlers that are used throughout all our dynamic pages:
#
class EH_Generic_class(XMLRewrite.XMLElementHandlers):
    iamadmin = 0
    def handle_CourseName(self,node,out):
        out.write(Config.conf['CourseName']+'\n')
    def handle_Semester(self,node,out):
        out.write(Config.conf['Semester']+'\n')
    def handle_Lecturer(self,node,out):
        out.write(Config.conf['Lecturer']+'\n')
    def handle_User1(self,node,out):
        if Config.conf.has_key('User1'):
            out.write(Config.conf['User1']+'\n')
    def handle_User2(self,node,out):
        if Config.conf.has_key('User2'):
            out.write(Config.conf['User2']+'\n')
    def handle_User3(self,node,out):
        if Config.conf.has_key('User3'):
            out.write(Config.conf['User3']+'\n')
    def handle_User4(self,node,out):
        if Config.conf.has_key('User4'):
            out.write(Config.conf['User4']+'\n')
    def handle_User5(self,node,out):
        if Config.conf.has_key('User5'):
            out.write(Config.conf['User5']+'\n')
    def handle_User6(self,node,out):
        if Config.conf.has_key('User6'):
            out.write(Config.conf['User6']+'\n')
    def handle_User7(self,node,out):
        if Config.conf.has_key('User7'):
            out.write(Config.conf['User7']+'\n')
    def handle_User8(self,node,out):
        if Config.conf.has_key('User8'):
            out.write(Config.conf['User8']+'\n')
    def handle_User9(self,node,out):
        if Config.conf.has_key('User9'):
            out.write(Config.conf['User9']+'\n')
    def handle_Feedback(self,node,out):
        out.write(Config.conf['Feedback']+'\n')
    def handle_PossibleStudies(self,node,out):
        for opt in Config.conf['PossibleStudies']:
            out.write('  <option>'+opt+'</option>\n')
    def handle_ValidatorIcon(self,node,out):
        out.write(ValidatorIconText)
    def handle_GroupSize(self,node,out):
        if node[1] == None or not(node[1].has_key('number')):
            Utils.Error('Found <GroupSize /> tag without "number" attribute. '
                        'Ignoring.',prefix='Warning:') 
            return
        try:
            nr = int(node[1]['number'])
        except:
            Utils.Error('Found "number" attribute in <GroupSize /> tag with '
                        'value not being a non-negative integer. Ignoring.',
                        prefix='Warning:')
            return
        if Data.groups.has_key(nr):
            out.write(str(len(Data.groups[nr])))
        else:
            out.write('0')
    def handle_ExerciseclassDistribution(self,node,out):
        l = Data.people.keys()
        l.sort()
        for k in l:
            out.write('<tr><td>'+k+'</td><td>'+str(Data.people[k].group)+
                      '</td></th>\n')
    def handle_MembersOfGroup(self,node,out):
        if node[1] == None or not(node[1].has_key('number')):
            Utils.Error('Found <MemberOfGroups /> tag without "number" '
                        'attribute. Ignoring.',prefix='Warning:') 
            return
        try:
            nr = int(node[1]['number'])
        except:
            Utils.Error('Found "number" attribute in <MembersOfGroup /> tag '
                        'with value not being a non-negative integer. '
                        'Ignoring.', prefix='Warning:')
            return
        if Data.groups.has_key(nr):
            l = list(Data.groups[nr])
            l.sort()
            for k in l[:-1]:
                out.write(k+', ')
            out.write(l[-1]+'.')
        else:
            Utils.Error('<MembersOfGroup /> tag requested empty group "'+
                        str(nr)+'".',prefix='Warning:')
    def handle_OKUSONLoginStatus(self,node,out):
        if currentcookie != None:
            out.write('There is somebody logged in. '
                      '<a href="/AdminLogout">Logout</a>\n')
        else:
            out.write('Nobody logged in. Administratorpassword:\n'
                      '<input type="password" size="16" maxlength="16" '
                      'name="passwd" value="" /> or \n'
                      '<a href="/adminlogin.html">login here.</a>\n')
    def handle_OKUSONServerStatus(self,node,out):
        if currentcookie != None:
            out.write('There is somebody logged in. ')
        else:
            out.write('Nobody logged in. ')
    def handle_AvailableSheetsAsButtons(self,node,out):
       l = Exercises.SheetList()
       for nr,name,s in l:
           if len(name) == 1:
             name = ' '+name
           if s.openfrom and time.time() < s.openfrom:
               if self.iamadmin:
                   out.write('(<input type="submit" name="sheet" value="'
                             +name+'" /> not yet open)\n')
           else:
               out.write('<input type="submit" name="sheet" value="'
                         +name+'" />\n')
    def handle_AvailableResolutions(self,node,out):
        out.write('<option selected="selected">Standard</option>\n')
        for r in Config.conf['Resolutions']:
            out.write('<option>'+str(r)+'</option>\n')    

EH_Generic = EH_Generic_class()

#
# Some helper functions:
#
def CleanQuotes(st):
    return st.replace('"','')

def Delegate(path,req,onlyhead,handler = None,addheader = []):
    '''This delegates to another path.'''
    if handler == None:
        (header,response) = Site[path].getresult(req,onlyhead)
    else:
        (header,response) = Site[path].getresult(req,onlyhead,handler)
    header['Content-Location'] = path
    for k,v in addheader: header[k] = v
    return (header,response)

def Authenticate(p,req,onlyhead):
    '''Checks password in the request. Administrator password is also 
       accepted. Return value is 1 if authentication was with admin
       password and 0 otherwise. In case of a failure we return -1.'''
    # Check whether password is correct:
    pw = req.query.get('passwd',['1'])[0].strip()[:16]
    salt = p.passwd[:2]
    passwd = crypt.crypt(pw,salt)
    # Check admin password:
    passwdadmin = crypt.crypt(pw,Config.conf['AdministratorPassword'][:2])
    iamadmin = (passwdadmin == Config.conf['AdministratorPassword'])
    if passwd != p.passwd and not(iamadmin):
        return -1
    else:
        return iamadmin

def SubmitRegistration(req,onlyhead):
    '''This function is called when a user submits a registration. It will
work on the submitted form data, register the new participant if possible
and either send an error message or a report.'''
    # First check whether the id is valid:
    id = req.query.get('id',['100000'])[0].strip()   # our default id
    if not(Config.conf['IdCheckRegExp'].match(id)):
        return Delegate('/errors/invalidid.html',req,onlyhead)

    # Now check whether the two passwords are identical:
    pw1 = req.query.get('passwd',['1'])[0].strip()[:16]
    pw2 = req.query.get('passwd2',['2'])[0].strip()[:16]
    if pw1 != pw2:
        return Delegate('/errors/diffpasswd.html',req,onlyhead)

    # Now check for empty fields:
    lname = req.query.get('lname',[''])[0].strip()[:30]
    fname = req.query.get('fname',[''])[0].strip()[:30]
    stud = req.query.get('stud',[''])[0].strip()[:30]
    topic = req.query.get('topic',[''])[0].strip()[:30]
    if topic != '': stud = topic
    sem = req.query.get('sem',[''])[0].strip()[:2]
    try:
        sem = int(sem)
    except:
        sem = 0
    if sem <= 0:
        return Delegate('/errors/semnonumber.html',req,onlyhead)

    if lname == '' or fname == '' or stud == '':
        return Delegate('/errors/emptyfields.html',req,onlyhead)

    email = req.query.get('email',[''])[0].strip()[:80]
    wishes = req.query.get('wishes',[''])[0].strip()[:80]

    # additional, not further specified, personal data for customization
    # (each can store up to 256 characters)
    persondata1 = req.query.get('persondata1',[''])[0].strip()[:256]
    persondata2 = req.query.get('persondata2',[''])[0].strip()[:256]
    persondata3 = req.query.get('persondata3',[''])[0].strip()[:256]
    persondata4 = req.query.get('persondata4',[''])[0].strip()[:256]
    persondata5 = req.query.get('persondata5',[''])[0].strip()[:256]
    persondata6 = req.query.get('persondata6',[''])[0].strip()[:256]
    persondata7 = req.query.get('persondata7',[''])[0].strip()[:256]
    persondata8 = req.query.get('persondata8',[''])[0].strip()[:256]
    persondata9 = req.query.get('persondata9',[''])[0].strip()[:256]

    # Construct data line with encrypted password:
    salt = random.choice(LETTERS) + random.choice(LETTERS)
    passwd = crypt.crypt(pw1,salt)
    line = AsciiData.LineTuple( (id,lname,fname,str(sem),stud,passwd,email,
                                 wishes,
                                 persondata1, persondata2, persondata3,
                                 persondata4, persondata5, persondata6,
                                 persondata7, persondata8, persondata9 ) )

    # Create a new Person object:
    p = Data.Person()
    p.id = id
    p.lname = lname
    p.fname = fname
    p.sem = sem
    p.stud = stud
    p.passwd = passwd
    p.email = email
    p.wishes = wishes
    p.persondata1 = persondata1
    p.persondata2 = persondata2
    p.persondata3 = persondata3
    p.persondata4 = persondata4
    p.persondata5 = persondata5
    p.persondata6 = persondata6
    p.persondata7 = persondata7
    p.persondata8 = persondata8
    p.persondata9 = persondata9

    # Then check at last whether we already have someone with that id:
    Data.Lock.acquire()
    if Data.people.has_key(id):
        Data.Lock.release()
        return Delegate('/errors/idinuse.html',req,onlyhead)
        
    # Put new person into file on disk:
    try:
        Data.peopledesc.AppendLine(line)
    except:
        Data.Lock.release()
        Utils.Error('Failed to register person:\n'+line)
        return Delegate('/errors/fatal.html',req,onlyhead)
    
    # Put new person into database in memory:
    Data.people[id] = p
    Data.Lock.release()

    # At last write out a sensible response:
    return Delegate('/messages/regsuccess.html',req,onlyhead)

class EH_withPersData_class(EH_Generic_class):
    '''This class exists to produce handlers that can fill in personal data
into a web sheet. It has some additional non-generic methods and holds
one Person object as data.'''
    p = None    # here we store the concrete personal data
    def __init__(self,p):
        self.p = p
    def handle_IdOfPerson(self,node,out):
        out.write(str(self.p.id))
    def handle_HiddenIdField(self,node,out):
        out.write('<input type="hidden" name="id" value="'+
                  CleanQuotes(self.p.id)+'" />'+self.p.id)
    def handle_LastName(self,node,out):
        out.write(str(self.p.lname))
    def handle_LastNameField(self,node,out):
        out.write('<input size="30" maxlength="30" name="lname" value="'+
                  CleanQuotes(self.p.lname)+'" />')
    def handle_FirstName(self,node,out):
        out.write(str(self.p.fname))
    def handle_FirstNameField(self,node,out):
        out.write('<input size="30" maxlength="30" name="fname" value="'+
                  CleanQuotes(self.p.fname)+'" />')
    def handle_PersonData1Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata1" ' + \
                  'value="'+ CleanQuotes(self.p.persondata1)+'" />')
    def handle_PersonData2Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata2" ' + \
                  'value="'+ CleanQuotes(self.p.persondata2)+'" />')
    def handle_PersonData3Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata3" ' + \
                  'value="'+ CleanQuotes(self.p.persondata3)+'" />')
    def handle_PersonData4Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata4" ' + \
                  'value="'+ CleanQuotes(self.p.persondata4)+'" />')
    def handle_PersonData5Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata5" ' + \
                  'value="'+ CleanQuotes(self.p.persondata5)+'" />')
    def handle_PersonData6Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata6" ' + \
                  'value="'+ CleanQuotes(self.p.persondata6)+'" />')
    def handle_PersonData7Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata7" ' + \
                  'value="'+ CleanQuotes(self.p.persondata7)+'" />')
    def handle_PersonData8Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata8" ' + \
                  'value="'+ CleanQuotes(self.p.persondata8)+'" />')
    def handle_PersonData9Field(self,node,out):
        out.write('<input size="30" maxlength="256" name="persondata9" ' + \
                  'value="'+ CleanQuotes(self.p.persondata9)+'" />')
    def handle_PersonData1(self, node, out):
        out.write(self.p.persondata1)
    def handle_PersonData2(self, node, out):
        out.write(self.p.persondata2)
    def handle_PersonData3(self, node, out):
        out.write(self.p.persondata3)
    def handle_PersonData4(self, node, out):
        out.write(self.p.persondata4)
    def handle_PersonData5(self, node, out):
        out.write(self.p.persondata5)
    def handle_PersonData6(self, node, out):
        out.write(self.p.persondata6)
    def handle_PersonData7(self, node, out):
        out.write(self.p.persondata7)
    def handle_PersonData8(self, node, out):
        out.write(self.p.persondata8)
    def handle_PersonData9(self, node, out):
        out.write(self.p.persondata9)

    def handle_PossibleStudies(self,node,out):
        found = 0
        for i in range(len(Config.conf['PossibleStudies'])):
            opt = Config.conf['PossibleStudies'][i]
            if (self.p.stud == opt) or \
               (found == 0 and i == len(Config.conf['PossibleStudies'])-1):
                out.write('  <option selected="selected">'+opt+'</option>\n')
                found = 1
            else:
                out.write('  <option>'+opt+'</option>\n')
    def handle_Topic(self,node,out):
        out.write(str(self.p.stud))
    def handle_TopicField(self,node,out):
        out.write('<input size="18" maxlength="30" name="topic" value="')
        if not(self.p.stud in Config.conf['PossibleStudies']):
            out.write(self.p.stud)
        out.write('" />')
    def handle_Sem(self,node,out):
        out.write(str(self.p.sem))
    def handle_SemesterField(self,node,out):
        out.write('<input size="2" maxlength="2" name="sem" value="'+
                  str(self.p.sem)+'" />')
    def handle_Email(self,node,out):
        out.write(str(self.p.email))
    def handle_EmailField(self,node,out):
        out.write('<input size="30" maxlength="80" name="email" value="'+
                  CleanQuotes(self.p.email)+'" />')
    def handle_Wishes(self,node,out):
        out.write(str(self.p.wishes))
    def handle_WishesField(self,node,out):
        out.write('<input size="30" maxlength="80" name="wishes" value="'+
                  CleanQuotes(self.p.wishes)+'" />')
    def handle_Results(self,node,out):
        # Check attributes if interactive and/or homework exercises are
        # considered (not given attributes mean 'true').
        if node[1] and node[1].has_key('interactive'):
            if node[1]['interactive'] != 'false':
                ia = 1
            else:
                ia = 0
        else:
            ia = 1
        if node[1] and node[1].has_key('homework'):
            if node[1]['homework'] != 'false':
                hw = 1
            else:
                hw = 0
        else:
            hw = 1
        l = Exercises.SheetList()
        for nr,name,s in l:
            if time.time() > s.opento:   # sheet already closed 
                if self.p.mcresults.has_key(name):
                    mcscore = str(self.p.mcresults[name].score)
                else:
                    mcscore = '---'
                if self.p.homework.has_key(name):
                    homescore = str(self.p.homework[name].totalscore)
                else:
                    homescore = '?'
                out.write('<tr><td align="center">'+name+'</td>')
                if ia:
                    out.write('<td align="center">'+mcscore+'</td>')
                if hw:
                    out.write('<td align="center">'+homescore+'</td>')
                out.write('</tr>\n')  
    def handle_Totalscore(self,node,out):
        l = Exercises.SheetList()
        totalscore = 0
        for nr,name,s in l:
            if time.time() > s.opento:   # sheet already closed 
                if self.p.mcresults.has_key(name):
                    totalscore += self.p.mcresults[name].score
                if self.p.homework.has_key(name):
                    totalscore += self.p.homework[name].totalscore
        out.write(str(totalscore))
    def handle_GeneralMessages(self,node,out):
        out.write(Config.conf['GeneralMessages'])
    def handle_PrivateMessages(self,node,out):
        for m in self.p.messages:
            out.write(m+'\n')

def QueryRegChange(req,onlyhead):
    '''This function is called when a user asks to change his registration. 
It will work on the submitted form data, check whether a registration is
there and send a form to display and change the saved data.'''
    # First check whether the id is valid:
    id = req.query.get('id',['100000'])[0].strip()   # our default id
    if not(Config.conf['IdCheckRegExp'].match(id)):
        return Delegate('/errors/invalidid.html',req,onlyhead)

    # Then check whether we already have someone with that id:
    if not(Data.people.has_key(id)):
        return Delegate('/errors/idunknown.html',req,onlyhead)
        
    p = Data.people[id]
    iamadmin = Authenticate(p,req,onlyhead)
    if iamadmin < 0:
        return Delegate('/errors/wrongpasswd.html',req,onlyhead)

    currentHandler = EH_withPersData_class(p)
    return Delegate('/regchange2.html',req,onlyhead,currentHandler)


def SubmitRegChange(req,onlyhead):
    '''This function is called when a user submits a registration. It will
work on the submitted form data, register the new participant if possible
and either send an error message or a report.'''
    # First check whether the id is valid:
    id = req.query.get('id',['100000'])[0].strip()   # our default id
    if not(Config.conf['IdCheckRegExp'].match(id)):
        return Delegate('/errors/invalidid.html',req,onlyhead)

    # Then check whether we already have someone with that id:
    if not(Data.people.has_key(id)):
        return Delegate('/errors/idunknown.html',req,onlyhead)
        
    p = Data.people[id]
    iamadmin = Authenticate(p,req,onlyhead)
    if iamadmin < 0:
        return Delegate('/errors/wrongpasswd.html',req,onlyhead)

    # Now check whether the two new passwords are identical:
    pw1 = req.query.get('pw1',[''])[0].strip()[:16]
    pw2 = req.query.get('pw2',[''])[0].strip()[:16]
    if pw1 != '' or pw2 != '':
        if pw1 != pw2:
            return Delegate('/errors/diffpasswd.html',req,onlyhead)
        salt = random.choice(string.letters) + random.choice(string.letters)
        passwd = crypt.crypt(pw1,salt)
    else:   # here we have to 
        passwd = p.passwd

    # Now check for empty fields:
    lname = req.query.get('lname',[''])[0].strip()[:30]
    fname = req.query.get('fname',[''])[0].strip()[:30]
    stud = req.query.get('stud',[''])[0].strip()[:30]
    topic = req.query.get('topic',[''])[0].strip()[:30]
    if topic != '': stud = topic
    sem = req.query.get('sem',[''])[0].strip()[:2]
    try:
        sem = int(sem)
    except:
        sem = 0
    if sem <= 0:
        return Delegate('/errors/semnonumber.html',req,onlyhead)

    if lname == '' or fname == '' or stud == '':
        return Delegate('/errors/emptyfields.html',req,onlyhead)

    email = req.query.get('email',[''])[0].strip()[:80]
    wishes = req.query.get('wishes',[''])[0].strip()[:80]

    # additional, not further specified, personal data for customization
    # (each can store up to 256 characters)
    persondata1 = req.query.get('persondata1',[''])[0].strip()[:256]
    persondata2 = req.query.get('persondata2',[''])[0].strip()[:256]
    persondata3 = req.query.get('persondata3',[''])[0].strip()[:256]
    persondata4 = req.query.get('persondata4',[''])[0].strip()[:256]
    persondata5 = req.query.get('persondata5',[''])[0].strip()[:256]
    persondata6 = req.query.get('persondata6',[''])[0].strip()[:256]
    persondata7 = req.query.get('persondata7',[''])[0].strip()[:256]
    persondata8 = req.query.get('persondata8',[''])[0].strip()[:256]
    persondata9 = req.query.get('persondata9',[''])[0].strip()[:256]

    # Put person into file on disk:
    line = AsciiData.LineTuple( (id,lname,fname,str(sem),stud,passwd,email,
                                 wishes,
                                 persondata1, persondata2, persondata3,
                                 persondata4, persondata5, persondata6,
                                 persondata7, persondata8, persondata9 ) )

    # Note: Between the moment we looked up our person and stored it in
    # 'p' there might have been some change in the database, because we
    # acquire the lock only now. We carry on regardless, assuming that
    # we, being "later", have the latest data. Also, we only overwrite
    # fields in the very same "Person" object and so do not change other
    # data.
    Data.Lock.acquire()
    try:
        Data.peopledesc.AppendLine(line)
    except:
        Data.Lock.release()
        Utils.Error('Failed to register person:\n'+line)
        return Delegate('/errors/fatal.html',req,onlyhead)
    
    # Put new person into database in memory:
    p.lname = lname
    p.fname = fname
    p.sem = sem
    p.stud = stud
    p.passwd = passwd
    p.email = email
    p.wishes = wishes
    p.persondata1 = persondata1
    p.persondata2 = persondata2
    p.persondata3 = persondata3
    p.persondata4 = persondata4
    p.persondata5 = persondata5
    p.persondata6 = persondata6
    p.persondata7 = persondata7
    p.persondata8 = persondata8
    p.persondata9 = persondata9

    # The same person object stays in the "people" dictionary.
    Data.Lock.release()

    # At last write out a sensible response:
    return Delegate('/messages/regchsuccess.html',req,onlyhead)


class EH_withPersSheet_class(EH_withPersData_class):
    '''This class exists to produce handlers that can fill in personal data
into an exercises sheet. It has some additional non-generic methods and holds
a Person object and a Sheet object as data.'''
    p = None    # here we store the concrete personal data
    s = None    # here we store the concrete sheet data
    r = 100     # resolution
    iamadmin = 0  # Flag, whether admin password was given
    def __init__(self,p,s,r):
        self.p = p
        self.s = s
        self.r = r
    def handle_SheetName(self,node,out):
        out.write(self.s.name)
    def handle_SheetNr(self,node,out):
        out.write(str(self.s.nr))
    def handle_IfOpen(self,node,out):
        if (time.time() <= self.s.opento and (self.s.openfrom == None or 
            time.time() >= self.s.openfrom)) or self.iamadmin:  # Sheet is open
            # Write out tree recursively:
            if node[2] != None:
                for n in node[2]:
                    XMLRewrite.XMLTreeRecursion(n,self,out)
    def handle_IfClosed(self,node,out):
        if time.time() > self.s.opento and not(self.iamadmin):    
            # Sheet already closed
            # Write out tree recursively:
            if node[2] != None:
                for n in node[2]:
                    XMLRewrite.XMLTreeRecursion(n,self,out)
    def handle_HiddenIdOfPerson(self,node,out):
        out.write('<input type="hidden" name="id" value="'+self.p.id+'" />\n')
    def handle_HiddenNameOfSheet(self,node,out):
        out.write('<input type="hidden" name="sheet" value="'+self.s.name+
                  '" />\n')
    def handle_WebSheetTable(self,node,out):
        if self.p.mcresults.has_key(self.s.name):
            self.s.WebSheetTable(self.r,SeedFromId(self.p.id),out,
                                 self.p.mcresults[self.s.name])
        else:
            self.s.WebSheetTable(self.r,SeedFromId(self.p.id),out,None)
    def handle_Timestamp(self,node,out):
        out.write(time.ctime())
    def handle_OpenTo(self,node,out):
        out.write(LocalTimeString(self.s.opento))
    def handle_OpenFrom(self,node,out):
        if self.s.openfrom:
            out.write(LocalTimeString(self.s.openfrom))
    def handle_CurrentTime(self,node,out):
        out.write(LocalTimeString())



def SeedFromId(id):
    return hash(id)   # is this guaranteed to return the same number for
                      # the same string?

def QuerySheet(req,onlyhead):
    # First check whether the id is valid:
    id = req.query.get('id',['100000'])[0].strip()   # our default id
    if not(Config.conf['IdCheckRegExp'].match(id)):
        return Delegate('/errors/invalidid.html',req,onlyhead)

    # Then check whether we already have someone with that id:
    if not(Data.people.has_key(id)):
        return Delegate('/errors/idunknown.html',req,onlyhead)
        
    p = Data.people[id]
    iamadmin = Authenticate(p,req,onlyhead)
    if iamadmin < 0:
        return Delegate('/errors/wrongpasswd.html',req,onlyhead)

    format = req.query.get('format',['HTML'])[0]  # Can be "HTML" or "PDF"

    sheetname = req.query.get('sheet',[''])[0].strip()  # the name of a sheet
    # Search for this name among sheet names:
    l = Exercises.SheetList()
    i = 0
    while i < len(l) and l[i][1] != sheetname: 
        i += 1
    if i >= len(l) or (not(iamadmin) and l[i][2].openfrom and 
                       time.time() < l[i][2].openfrom):
        return Delegate('/errors/unknownsheet.html',req,onlyhead)
    sheet = l[i]
    if format == 'HTML':
        resolution = req.query.get('resolution',['Standard'])[0]
        addheader = []   # If resolution chosen explicitly, store it in cookie
        if resolution == 'Standard':
            resolution = Config.conf['Resolutions'][0]   # the default
            try:
                # Check for cookie:
                cookie = Cookie.SimpleCookie()
                cookie.load('Cookie: '+req.headers.get('Cookie',''))
                cookieres = cookie['OKUSONResolution'].value
                resolution = int(cookieres)
                if not(resolution in Config.conf['Resolutions']):
                    resolution = Config.conf['Resolutions'][0]
            except:
                pass
        else:
            try: 
                resolution = int(resolution)
                if not(resolution in Config.conf['Resolutions']):
                    resolution = Config.conf['Resolutions'][0]
                else:
                    addheader = [('Set-Cookie','OKUSONResolution='+str(resolution))]
            except: 
                resolution = Config.conf['Resolutions'][0]
               
        # Now we really deliver the sheet. We must create a handler object
        # for person p's sheet l[i]:
        handler = EH_withPersSheet_class(p,sheet[2],resolution)
        handler.iamadmin = iamadmin
        return Delegate('/sheet.html',req,onlyhead,handler,addheader)
    elif format == 'PDF':
        # Collect placeholder values in dictionary
        values = {}
        values['SheetName'] = sheetname
        values['IdOfPerson'] = id
        for a in ['CourseName', 'Semester', 'Lecturer']:
          values[a] = Config.conf[a]
        # find values of custom variables from config and for persons
        for i in range(9):
          ii = str(i+1)
          if Config.conf.has_key('User'+ii):
            values['User'+ii] = Config.conf['User'+ii]
          else:
            values['User'+ii] = ''
          try:
            values['PersonData'+ii] = getattr(Data[id], 'persondata'+ii)
          except:
            values['PersonData'+ii] = ''
        values['OpenTo'] = LocalTimeString(sheet[2].opento)
        if sheet[2].openfrom:
            values['OpenFrom'] = LocalTimeString(sheet[2].openfrom)
        else:
            values['OpenFrom'] = ''
        values['CurrentTime'] = LocalTimeString()

        # finally the actual exercises as longtable environment
        values['ExercisesTable'] = sheet[2].LatexSheetTable(SeedFromId(id))
        latexinput = SimpleTemplate.FillTemplate(Config.conf['PDFTemplate'], 
                                                 values)
        pdf = LatexImage.LatexToPDF(latexinput)

        if not pdf:
            Utils.Error('Cannot pdflatex sheet input (id='+id+\
                        ', sheet='+sheetname+').')
            return Delegate('/errors/pdfproblem.html', req, onlyhead)
        return ({'Content-type': 'application/pdf', 'Expires': 'now'}, pdf)
    else:
        return Delegate('/errors/invalidformat.html', req, onlyhead)


def SubmitSheet(req,onlyhead):
    '''This function accepts a submission for a sheet. It checks the
input, gives appropriate warning and error messages and stores the
submission as well as the results.'''

    # First check whether the id is valid:
    id = req.query.get('id',['100000'])[0].strip()   # our default id
    if not(Config.conf['IdCheckRegExp'].match(id)):
        return Delegate('/errors/invalidid.html',req,onlyhead)

    # Then check whether we already have someone with that id:
    if not(Data.people.has_key(id)):
        return Delegate('/errors/idunknown.html',req,onlyhead)
        
    p = Data.people[id]
    iamadmin = Authenticate(p,req,onlyhead)
    if iamadmin < 0:
        return Delegate('/errors/wrongpasswd.html',req,onlyhead)

    sheetname = req.query.get('sheet',[''])[0]    # the name of a sheet
    # Search for this name among sheet names:
    l = Exercises.SheetList()
    i = 0
    while i < len(l) and l[i][1] != sheetname: 
        i += 1
    s = l[i][2]   # the sheet in question
    if i >= len(l) or (not(iamadmin) and s.openfrom and 
                       time.time() < s.openfrom):
        return Delegate('/errors/unknownsheet.html',req,onlyhead)

    # Now check, whether it is still possible to submit this sheet:
    if time.time() > s.opento and not(iamadmin):
        return Delegate('/errors/sheetclosed.html',req,onlyhead)

    ok = s.AcceptSubmission(p,SeedFromId(p.id),req.query)
    if not(ok):
        return Delegate('/error/badsubmission.html',req,onlyhead)
    else:
        handler = EH_withPersSheet_class(p,s,Config.conf['Resolutions'][0])
        handler.iamadmin = iamadmin
        return Delegate('/messages/subsuccess.html',req,onlyhead,handler)

def QueryResults(req,onlyhead):
    '''This function is called when a user asks to see his results.
It will work on the submitted form data, check whether a registration is
there and send a form to display and change the saved data.'''
    # First check whether the id is valid:
    id = req.query.get('id',['100000'])[0].strip()   # our default id
    if not(Config.conf['IdCheckRegExp'].match(id)):
        return Delegate('/errors/invalidid.html',req,onlyhead)

    # Then check whether we already have someone with that id:
    if not(Data.people.has_key(id)):
        return Delegate('/errors/idunknown.html',req,onlyhead)
        
    p = Data.people[id]
    iamadmin = Authenticate(p,req,onlyhead)
    if iamadmin < 0:
        return Delegate('/errors/wrongpasswd.html',req,onlyhead)

    currentHandler = EH_withPersData_class(p)
    return Delegate('/results.html',req,onlyhead,currentHandler)


# The following is for the administrator's pages:

currentcookie = None

def AuthenticateAdmin(req,onlyhead):
    '''Check password for admin. Return -1 for failure and 0 otherwise.'''
    global currentcookie
    # Check for cookie:
    cookie = Cookie.SimpleCookie()
    cookie.load('Cookie: '+req.headers.get('Cookie',''))
    # Check for admin password:
    passwd = req.query.get('passwd',[''])[0]
    salt = Config.conf['AdministratorPassword'][:2]
    passwd = crypt.crypt(passwd,salt)
    try: 
        cookieval = cookie['OKUSON'].value
    except:
        cookieval = ''
    if cookieval != currentcookie and \
       passwd != Config.conf['AdministratorPassword']:
        return -1
    else:
        return 0

def AdminLogin(req,onlyhead):
    global currentcookie
    passwd = req.query.get('passwd',[''])[0]
    salt = Config.conf['AdministratorPassword'][:2]
    passwd = crypt.crypt(passwd,salt)
    if passwd != Config.conf['AdministratorPassword']:
        return Delegate('/errors/wrongpasswd.html',req,onlyhead)

    (header,content) = Site['/adminmenu.html'].getresult(req,onlyhead)
    random.seed(time.time())
    currentcookie = str(random.randrange(10000000))
    header['Set-Cookie'] = 'OKUSON='+currentcookie
    header['Location'] = '/adminmenu.html'
    return (header,content)

# The following was just for testing purposes:
#def AdminTest(req,onlyhead):
#    if AuthenticateAdmin(req,onlyhead) < 0:
#        return Delegate('/errors/notloggedin.html',req,onlyhead)
#    else:
#        return Delegate('/adminmenu.html',req,onlyhead)

def AdminLogout(req,onlyhead):
    global currentcookie
    currentcookie = None
    return Delegate('/adminlogin.html',req,onlyhead)

def NormalizeWishes(w):
    '''Normalizes a wishlist. First the string is split at space and commas,
       then only those chunks are taken, that are a valid ID of some
       participant.'''
    w = w.split()
    wishlist = []
    for ww in w:
      for www in ww.split(','):
        if Data.people.has_key(www): wishlist.append(www)
    return string.join(wishlist,',')

def ExportByID(req,onlyhead):
    '''Export the list of all participants, sorted by ID, giving the
       following fields: 
         id:lname:fname:sem:stud:wishes 
       where wishes has been normalized into a comma separated list
       of existing id's. Colons have been deleted.'''
    l = Data.people.keys()
    l.sort()
    out = cStringIO.StringIO()
    out.write('# ID:last name:first name:semester:studiengang:wishes\n')
    for k in l:
        p = Data.people[k]
        w = NormalizeWishes(p.wishes)
        out.write(k+':'+
                  p.lname.replace(':','')+':'+
                  p.fname.replace(':','')+':'+
                  str(p.sem)+':'+
                  p.stud.replace(':','')+':'+
                  w+'\n')
    st = out.getvalue()
    out.close()
    head = {'Content-type':'text/okuson',
            'Content-Disposition':'attachment; filename="peoplelist.txt"',
            'Last-modified':req.date_time_string(time.time())}
    return (head,st)



def AdminWork(req,onlyhead):
    '''This function does the dispatcher work for the administrator
       actions.'''
    action = req.query.get('Action','')[0].strip()
    if action == 'PID':
        return ({'Content-type': 'text/plain'}, str(BuiltinWebServer.PID))
    if AuthenticateAdmin(req,onlyhead) < 0:
        return Delegate('/errors/notloggedin.html',req,onlyhead)
    if action == 'Restart':
        BuiltinWebServer.SERVER.raus = 1
        BuiltinWebServer.SERVER.restartcommand = \
              os.path.join(Config.home,'server/Server.py')
        os.kill(BuiltinWebServer.SERVER.ourpid,signal.SIGUSR1)
        return Delegate('/adminrestarted.html',req,onlyhead)
    if action == 'Shutdown':
        BuiltinWebServer.SERVER.raus = 1
        os.kill(BuiltinWebServer.SERVER.ourpid,signal.SIGUSR1)
        return Delegate('/admindown.html',req,onlyhead)
    if action == 'ExportByID':
        return ExportByID(req,onlyhead)
    if action == 'Display Sheets':
        return Adminexquery.getresult(req, onlyhead)

# Install the dynamic pages:
# There are two different sorts of pages:
# 1) Pages without input which are generated from templates by filling
#    in some values.
# 2) Pages with input that trigger a function that works on the input
#    and sends out a page of the first kind.
PPXML = XMLRewrite.PreparsedXMLWebResponse
FunWR = BuiltinWebServer.FunctionWebResponse

BuiltinWebServer.SiteLock.acquire()
Site['/SubmitRegistration'] = FunWR(SubmitRegistration)
Site['/QueryRegChange'] = FunWR(QueryRegChange)
Site['/SubmitRegChange'] = FunWR(SubmitRegChange)
Site['/QuerySheet'] = FunWR(QuerySheet)
Site['/SubmitSheet'] = FunWR(SubmitSheet)
Site['/QueryResults'] = FunWR(QueryResults)
Site['/AdminLogin'] = FunWR(AdminLogin)
Site['/AdminLogin'].access_list = Config.conf['AdministrationAccessList']
Site['/AdminLogout'] = FunWR(AdminLogout)
Site['/AdminLogout'].access_list = Config.conf['AdministrationAccessList']
Site['/AdminWork'] = FunWR(AdminWork)
Site['/AdminWork'].access_list = Config.conf['AdministrationAccessList']


# We register all the other .tpl files in our tree with EH_Generic handlers:

def visitor(arg,dirname,names):
    if dirname == os.path.join(DocRoot,"images"):
        names[:] = []
    for n in names:
        if n[-4:] == '.tpl':
            if dirname == DocRoot:
                ourpath = '/'+n[:-4]
            else:
                ourpath = os.path.join(dirname[len(DocRoot):]+'/',n[:-4])
            if not(Site.has_key(ourpath+'.html')):
                try:
                    Site[ourpath+'.html'] = PPXML(dirname,n,EH_Generic)
                    Utils.Error('Successfully loaded '+ourpath+'.tpl',
                                prefix="Info:")
                except:
                    Utils.Error('Loading of '+ourpath+'.tpl was not '
                                'successful!')

Adminexquery = None
def RegisterAllTpl():
    global Adminexquery
    os.path.walk(DocRoot,visitor,None)
    # Mark the administrator's pages:
    Site['/adminlogin.html'].access_list=Config.conf['AdministrationAccessList']
    Site['/adminmenu.html'].access_list=Config.conf['AdministrationAccessList']
    # Reinstall exquery.html for admin - includes not yet open sheets
    eh = EH_Generic_class()
    eh.iamadmin = 1
    Adminexquery = PPXML(DocRoot,'exquery.tpl',eh)
    # Copy the index file to hide things:
    Site['/messages'] = Site['/errors'] = Site['/'] = Site['/index.html']
    Site['/messages/'] = Site['/errors/'] = Site['/index.html']
    Site['/images'] = Site['/images/'] = Site['/index.html']
    for r in Config.conf['Resolutions']:
        Site['/images/dpi'+str(r)] = Site['/index.html']
        Site['/images/dpi'+str(r)+'/'] = Site['/index.html']


BuiltinWebServer.SiteLock.release()
BuiltinWebServer.WebResponse.access_list = Config.conf['AccessList']
BuiltinWebServer.access_list = Config.conf['AccessList']

