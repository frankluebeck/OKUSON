# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This is the place where all data about participants of the course are
administrated. This includes data about their results and submissions.'''

CVS = '$Id: Data.py,v 1.22 2004/03/09 15:16:39 neunhoef Exp $'

import sys,os,string,threading

import Config, Exercises

from fmTools import Utils, AsciiData

# The following decides, whether the server is in Administrator mode
# or not.
AdminMode = 0

# Here we begin the definition of the user database:

# We agree on the following locking policy:
# Once threaded service has begun, we allow every thread unlocked read
# access to the data base (which is made up of a tree of memory objects
# stored under the root "people"). However, any write access to any data
# in this tree must be protected by acquiring the following lock:
Lock = threading.Lock()

# This means: Whenever a routine writes anything into the database,
# one has to acquire the Lock even before certain read accesses, on
# which the following write operation might depend! So if one for 
# example checks whether there is already some data for a person
# just before creating it (as for example during registration), one
# has to acquire the Lock before the check, to avoid any write accesses
# from other sources between the lookup and the addition of the data!
# Please keep locks short! And ALWAYS, ALWAYS, ALWAYS make sure to 
# release the lock eventually, under all circumstances!

class Person(Utils.WithNiceRepr):
    '''Objects of in this class store a person.'''
    id = "100000"     # an id which determines the person uniquely
    lname = "?"       # last name
    fname = "?"       # first name
    sem = 1           # semester number
    stud = "?"        # "Studiengang"
    passwd = "x"      # password, encrypted via "crypt"
    email = ""        # email address, optional
    wishes = ""       # a string with wishes for tutoring groups
    persondata = {}   # a dictionary for additional personal data, 
                      # these are not used in the default setup provided 
                      # by OKUSON
    mcresults = {}    # for each sheet name an object of type "MCResult"
                      # note that keys in this dictionary are strings!
    homework = {}     # for each sheet name an object of type "Homework"
    exams = []        # for each exam (zero based numbers) either unbound
                      # or None or an object of type "Exam"
    group = 0         # number of tutoring group the person is in
    messages = []     # here we collect private messages for participants
                      # these are just strings which are put into a web
                      # page one after another.

    def __init__(self):
        self.mcresults = {}
        self.homework = {}
        self.exams = []
        self.messages = []
        
    def TotalMCScore(self):
        l = Exercises.SheetList()
        totalscore = 0
        for nr,name,s in l:
            if s.counts and s.IsClosed():   # sheet already closed 
                if self.mcresults.has_key(name):
                    totalscore += self.mcresults[name].score
        return totalscore
    def TotalHomeScore(self):
        l = Exercises.SheetList()
        totalscore = 0
        for nr,name,s in l:
            if s.counts and s.IsClosed():   # sheet already closed 
                if self.homework.has_key(name) and \
                   self.homework[name].totalscore != -1:
                    totalscore += self.homework[name].totalscore
        return totalscore
    def TotalScore(self):
        l = Exercises.SheetList()
        totalscore = 0
        for nr,name,s in l:
            if s.counts and s.IsClosed():   # sheet already closed 
                if self.mcresults.has_key(name):
                    totalscore += self.mcresults[name].score
                if self.homework.has_key(name) and \
                   self.homework[name].totalscore != -1:
                    totalscore += self.homework[name].totalscore
        return totalscore

people = {}     # all people are stored in here under their id

peopledesc = AsciiData.FileDescription(Config.conf['RegistrationFile'],people,
  ( "ENTER", 0, "KEY",         Person,
    "STORE", 0, "id",          "STRING",
    "STORE", 1, "lname",       "STRING",
    "STORE", 2, "fname",       "STRING",
    "STORE", 3, "sem",         "INT",
    "STORE", 4, "stud",        "STRING",
    "STORE", 5, "passwd",      "STRING",
    "STORE", 6, "email",       "STRING",
    "STORE", 7, "wishes",      "STRING",
    "STORE", 8, "persondata",  "LINEDICT" ) )


class MCResult(Utils.WithNiceRepr):
    '''Objects in this class store multiple choice submissions and results.'''
    marks = ""      # string of "+", "-", and "0"s each letter for one question
    score = 0       # sum of points
    submission = "" # the submission as one string for later reference
    date = 0        # submission date in seconds since the epoche
                                       
mcresultsdesc = AsciiData.FileDescription(Config.conf['SubmissionFile'],people,
  ( "ENTER", 0, "KEY",        Person,
    "STORE", 0, "id",         "STRING",
    "ENTER", 0, "mcresults",  "DICT",
    "ENTER", 1, "KEY",        MCResult,
    "STORE", 2, "marks",      "STRING",
    "STORE", 3, "score",      "INT",
    "STORE", 4, "submission", "STRING",
    "STORE", 5, "date",       "INT" ) )


class Homework(Utils.WithNiceRepr):
    '''Objects in this class store homework results.'''
    totalscore = -1 # score for all written exercises
    scores = ""     # scores of the separate written exercises

    def __init__(self):
        self.scores = ""

homeworkdesc = AsciiData.FileDescription(Config.conf['HomeworkFile'],people,
  ( "ENTER", 0, "KEY",        Person,
    "STORE", 0, "id",         "STRING",
    "ENTER", 0, "homework",   "DICT",
    "ENTER", 1, "KEY",        Homework,
    "STORE", 2, "totalscore", "NUMBER",
    "STORE", 3, "scores",     "STRING" ) )


class Exam(Utils.WithNiceRepr):
    '''Objects in this class store exam information.'''
    maxexamnumber = 0   # this is a class variable, which keeps the
                        # largest number of exam occuring plus 1 (zero-based)
    registration = 1    # if true, person has registered for exam
    totalscore = -1     # totalscore
    maxscore = 0        # maximal score
    scores = ""         # scores for separate parts of exam
    timestamp = 0       # timestamp of registration, in seconds since 1970

examregdesc = AsciiData.FileDescription(Config.conf['ExamRegistrationFile'],
                                        people,
  ( "ENTER", 0, "KEY",          Person,
    "STORE", 0, "id",           "STRING",
    "ENTER", 0, "exams",        "VECT",
    "ENTER", 1, "KEY",          Exam,
    "STORE", 2, "registration", "INT",
    "STORE", 3, "timestamp",    "INT" ) )

examdesc = AsciiData.FileDescription(Config.conf['ExamFile'],people,
  ( "ENTER", 0, "KEY",          Person,
    "STORE", 0, "id",           "STRING",
    "ENTER", 0, "exams",        "VECT",
    "ENTER", 1, "KEY",          Exam,
    "STORE", 2, "totalscore",   "NUMBER",
    "STORE", 3, "maxscore",     "NUMBER",
    "STORE", 4, "scores",       "STRING" ) )

def countexams():
    '''This function looks through all people and counts, how many exams
       there are. It sets the class variable Exam.maxexamnumber.'''
    for k,p in people.iteritems():
        if len(p.exams) > Exam.maxexamnumber:
            Exam.maxexamnumber = len(p.exams)
    # Note: There is one place, where Exam.maxexamnumber may change during
    #       the runtime of the server. That is when the first person registers
    #       for a new exam. Therefore there is code in that place to handle
    #       this case!
        

groupdesc = AsciiData.FileDescription(Config.conf['GroupFile'],people,
  ( "ENTER", 0, "KEY",          Person,
    "STORE", 0, "id",           "STRING",
    "STORE", 1, "group",        "INT" ) )

messagedesc = AsciiData.FileDescription(Config.conf['MessageFile'],people,
  ( "ENTER", 0, "KEY",          Person,
    "STORE", 0, "id",           "STRING",
    "ENTER", 0, "messages",     "VECT",
    "STORE", 1, "NEXT",         "STRING" ) )

def cleanRevokedMessages():
    '''This little function cleans revoked messages. If the administrator
       deletes a private message, it is not really deleted but only revoked.
       This means, that a new message is appended, that starts with a dollar
       sign and repeats the text of the message before. Such messages cancel
       the previous ones by way of this function.'''
    for k,p in people.iteritems():
        i = 0
        while i < len(p.messages):
            if len(p.messages[i]) > 0 and p.messages[i][0] == '$':
                j = 0
                while j < i and p.messages[j] != p.messages[i][1:]: 
                    j += 1
                if j < i:   # found a revoked message
                    del p.messages[i]
                    del p.messages[j]
                    i -= 2   # will be inkremented in a second.
            i += 1

# Here comes a little statistic about the exercises classes or "groups":
# Under each key we store

groups = {}

class GroupInfo(Utils.WithNiceRepr):
    '''Object containing general information about a tutoring group.'''
    people = []        # list of participants by their ID
    number = -1        # number of group ( = its key in 'groups')
    passwd = ''        # encrypted password for tutor access
    tutor = ''         # name of tutor
    place = ''         # description where the group meets
    time = ''          # description when the group meets
    emailtutor = ''    # email of tutor
    maxsize = 1000     # maximal number of participants
    groupdata = {}     # a dictionary for custom data for groups

    def __init__(self, number = -1):
        self.people = []
        self.number = number

def AddToGroupStatistic(p):
    '''Adds a person to the groups statistic.'''
    global groups
    g = str(p.group)
    if not(groups.has_key(g)): 
        groups[g] = GroupInfo(g)
    if not(Config.conf['GuestIdRegExp'].match(p.id)):
        # we only add "real" IDs to the group cache
        groups[g].people.append(p.id)

def DelFromGroupStatistic(p):
    '''Deletes a person from the groups statistic.'''
    global groups
    g = str(p.group)
    if not(groups.has_key(g)):
        groups[g] = GroupInfo(g)
    try:
        i = groups[g].people.index(p.id)
        del groups[g].people[i]
    except:
        pass
        
def MakeGroupStatistic():
    global groups
    for k in people.keys():
        p = people[k]
        AddToGroupStatistic(p)

def GlobalStatistics (sheetKey, group=None):
    '''Returns a tuple of statistical Data for the Exercise Sheets.
Sheet Number is indicated by sheetKey.
   The tuple consists of 
    Number of people who produced homework
    average score homework
    median score homework
    higest score homework
    list of numbers for each interval homework
    Number of people who submitted MC
    average score mc
    median score mc
    highest score mc
    list of numbers for each interval mc'''

    sum = 0
    sumMc = 0
    listOfPoints = []
    listOfPointsMc = []
    listOfIntervals = [ 0 ]
    listOfIntervalsMc = [ 0 ]
    numberOfSubmissions = 0
    numberOfSubmissionsMc = 0
    highestScore = 0
    highestScoreMc=0
    for k in people.keys():
        p = people[k]
        if group != None:
            if p.group != groups[group].number: continue
        if not(Config.conf['GuestIdRegExp'].match(k)):
            if p.homework.has_key(sheetKey) and \
               p.homework[sheetKey].totalscore != -1:
                numberOfSubmissions += 1
                score = p.homework[sheetKey].totalscore
                listOfPoints.append(score)
                sum += score
                roundedscore = int(score)
                while roundedscore >= len(listOfIntervals):
                    listOfIntervals.append(0)
                listOfIntervals[roundedscore] += 1
                if highestScore < score: highestScore = score;
            if p.mcresults.has_key(sheetKey):
                numberOfSubmissionsMc += 1
                score = p.mcresults[sheetKey].score
                listOfPointsMc.append(score)
                sumMc += score
                roundedscore = int(score)
                while roundedscore >= len(listOfIntervalsMc):
                    listOfIntervalsMc.append(0)
                listOfIntervalsMc[roundedscore] += 1
                if highestScoreMc < score: highestScoreMc = score;
    if numberOfSubmissions > 0:
        average = float(sum) / float(numberOfSubmissions)
        listOfPoints.sort()
        if len(listOfPoints) % 2 == 0:
            median = float(listOfPoints[len(listOfPoints)/2 - 1] + \
                listOfPoints[len(listOfPoints)/2 ]   ) / 2
        else:
            median = listOfPoints[ (len(listOfPoints)-1)/2 ]
    else:
        average = 0
        median = 0
    if numberOfSubmissionsMc > 0:
        averageMc = float(sumMc) / float(numberOfSubmissionsMc)
        listOfPointsMc.sort()
        if len(listOfPointsMc) % 2 == 0:
            medianMc = float(listOfPointsMc[len(listOfPointsMc)/2 - 1] + \
                           listOfPointsMc[len(listOfPointsMc)/2  ]   ) / 2.0
        else:
            medianMc = listOfPointsMc[ (len(listOfPointsMc)-1)/2 ]
    else:
        averageMc = 0
        medianMc = 0
    return ( numberOfSubmissions, average, median, highestScore, 
             listOfIntervals, numberOfSubmissionsMc, averageMc, medianMc, 
             highestScoreMc, listOfIntervalsMc)
                

# General information about tutoring groups 
groupinfodesc = AsciiData.FileDescription(Config.conf['GroupInfoFile'],groups,
  (  "ENTER", 0, "KEY",        GroupInfo,
     "STORE", 0, "number",     "INT",
     "STORE", 1, "passwd",     "STRING",
     "STORE", 2, "tutor",      "STRING",
     "STORE", 3, "place",      "STRING",
     "STORE", 4, "time",       "STRING",
     "STORE", 5, "emailtutor", "STRING",
     "STORE", 6, "maxsize",    "INT",
     "STORE", 7, "groupdata",  "LINEDICT" )  )

