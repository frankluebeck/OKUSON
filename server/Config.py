# -*- coding: ISO-8859-1 -*-
#  OKUSON Package
#  Frank Lübeck and Max Neunhöffer

'''This module is the central place for configuration data from the
administrator. The configuration data comes from a single file
"Config.xml" in OKUSON's home directory. The code to parse that file is
also in this module.
Information from this module is exported via the variables "home" and
"conf" below.'''

home = ''       # absolute path to OKUSON's home directory

conf = {}       # dictionary of configuration data
                # all entries will be strings, integers or lists of strings

# The following dictionary encodes which configuration parameters exist,
# their type ("STRING", "INT", "FLOAT", "LIST", "PATHLIST", or "PATH") and, 
# whether they are essential (error message if value is missing) or not.
# "PATH" means the same as "STRING", but home is prepended via
# os.path.join. The same is true for the entries in a "PATHLIST".
Parameters = {
  "AdministratorPassword":    ["STRING",1],
  "CourseName":               ["STRING",1],
  "Semester":                 ["STRING",1],
  "Lecturer":                 ["STRING",1],
  "Feedback":                 ["STRING",1],
  "PossibleStudies":          ["LIST",1],
  "Port":                     ["INT",1],
  "ExtraLaTeXHeader":         ["STRING",0],
  "User1":                    ["STRING",0],
  "User2":                    ["STRING",0],
  "User3":                    ["STRING",0],
  "User4":                    ["STRING",0],
  "User5":                    ["STRING",0],
  "User6":                    ["STRING",0],
  "User7":                    ["STRING",0],
  "User8":                    ["STRING",0],
  "User9":                    ["STRING",0],
  "IdCheckRegExp":            ["STRING",1],
  "GuestIdRegExp":            ["STRING",0],
  "GradingFunction":          ["STRING",0],
  "GradingActive":            ["INT",0],

  "AccessList":               ["LIST",1],
  "AdministrationAccessList": ["LIST",1],
  "DocumentRoot":             ["PATH",0],
  "ExerciseDirectories":      ["PATHLIST",1],
  "SheetDirectories":         ["PATHLIST",1],
  "GeneralMessageFile":       ["PATH",1],
  "RegistrationFile":         ["PATH",1],
  "SubmissionFile":           ["PATH",1],
  "HomeworkFile":             ["PATH",1],
  "ExamRegistrationFile":     ["PATH",1],
  "ExamFile":                 ["PATH",1],
  "GroupFile":                ["PATH",1],
  "MessageFile":              ["PATH",1],
  "GroupInfoFile":            ["PATH",0],
  "PathToDTDs":               ["PATH",1],
  "PDFTemplate":              ["STRING",1],
  "PDFTemplateNoTable":       ["STRING",0],

  "WidthOfSheetsHTML":        ["FLOAT",1],
  "WidthOfExerciseTextsHTML": ["FLOAT",1],
  "WidthOfQuestionsHTML":     ["FLOAT",1],
  "WidthOfSheetsPDF":         ["FLOAT",1],
  "WidthOfExerciseTextsPDF":  ["FLOAT",1],
  "WidthOfQuestionsPDF":      ["FLOAT",1],
  "Resolutions":              ["STRING",1],   # a comma separated list of ints
  "LaTeXTemplate":            ["STRING",1],
}

# Some stuff is needed:

import sys,os,traceback,string,types,re,socket


# We start by determining OKUSON's home directory:

if os.environ.has_key("OKUSONHOME"):
    home = os.environ["OKUSONHOME"]
else:
    home = os.path.abspath(os.path.join(sys.path[0],".."))

# The following is needed for error reporting purposes:

from fmTools import Utils, SimpleTemplate
import pyRXPU


# The following function is called just before the startup fails:

def FailMiserably():
    Utils.Error("Aborting.",prefix="")
    sys.exit(1)
     
# The following function is called when pyRXP wants to open the dtd file:
# We direct pyRXP to the 'dtd' subdirectory of our home directory:

def OurDtdOpener(d):
    return os.path.join(home,'dtd',d)

# The following function reads our configuration file "Config.xml" and 
# parses it, failing miserably if that does not work:

def ReadConfig():
    global conf
    configfile = os.path.join(home,"Config.xml")
    try:
        cf = Utils.StringFile(configfile)
    except:
        FailMiserably()
    p = pyRXPU.Parser(fourth = pyRXPU.recordLocation,
                      ReturnDefaultedAttributes = 0,
                      MergePCData = 1,
                      Validate = 1,
                      eoCB = OurDtdOpener)
    try:
        tree = p.parse(cf, srcName = configfile)
    except pyRXPU.error, e:
        Utils.Error("XML parser error:\n\n"+str(e))
        FailMiserably()

    # Now run through the tree:
    # We know by the DTD that there is exactly one "Config" element.
    if tree[2] != None:   # there might be no subelements
        for node in tree[2]:
          if type(node) == types.TupleType:
            # We know by the DTD that there is only element content, but
            # strings in between are still reported by pyRXP.
            key = node[0].encode('ISO-8859-1','replace')
            if Parameters.has_key(key):
                info = Parameters[key]
                if info[0] == 'STRING' or info[0] == 'INT' or \
                   info[0] == 'FLOAT' or info[0] == 'PATH':
                    # We know by the DTD that there is only #PCDATA content
                    # Usually this will come as one chunk because of
                    # "MergePCData=1" above. We strip whitespace at 
                    # beginning and end:
                    conf[key] = string.strip(string.join(node[2]))
                    if info[0] == 'STRING' or info[0] == 'PATH':
                        try:
                            conf[key] = conf[key].encode('ISO8859-1')
                        except:
                            Utils.Error('Value "'+conf[key]+'" of '+
                                'configuration field "'+key+'" at '+
                                Utils.StrPos(node[3])+' has no ISO8859-1'+
                                ' encoding. We assume the empty string.',
                                prefix = 'Warning: ')
                            conf[key] = ""
                        if info[0] == 'PATH':
                            conf[key] = os.path.join(home,conf[key])
                    elif info[0] == 'INT':
                        try:
                            conf[key] = int(conf[key])
                        except:
                            Utils.Error('Value "'+conf[key]+'" of '+
                                'configuration field "'+key+'" at '+
                                Utils.StrPos(node[3])+' is not an integer. We'+
                                ' assume 0.',prefix = 'Warning: ')
                            conf[key] = 0
                    elif info[0] == 'FLOAT':
                        try:
                            conf[key] = float(conf[key])
                        except:
                            Utils.Error('Value "'+conf[key]+'" of '+
                                'configuration field "'+key+'" at '+
                                Utils.StrPos(node[3])+' is not a float. We'+
                                ' assume 0.0 .',prefix = 'Warning: ')
                            conf[key] = 0.0
                elif info[0] == 'LIST' or info[0] == 'PATHLIST':
                    # We know by the DTD, that the children are just a list
                    # of elements with #PCDATA content:
                    conf[key] = []
                    for subnode in node[2]:
                        if type(subnode) == types.TupleType:
                            s = string.strip(string.join(subnode[2]))
                            try:
                                s = s.encode('ISO8859-1')
                            except:
                                Utils.Error('Value "'+s+'" of '+
                                    'configuration field "'+key+'" at '+
                                    Utils.StrPos(node[3])+' has no ISO8859-1'+
                                    ' encoding. We ignore it.',
                                    prefix = 'Warning: ')
                            if info[0] == 'PATHLIST':
                                s = os.path.join(home,s)
                            conf[key].append(s)

            else:  # A configuration field that we do not know!
                Utils.Error('Unknown configuration field "'+key+'" at '+
                            Utils.StrPos(node[3])+', ignoring.',
                            prefix='Warning: ')
    abort = 0
    for k in Parameters.keys():
        if Parameters[k][1] and not(conf.has_key(k)):
            Utils.Error('Essential configuration option not found: "'+k+'".')
            abort = 1
    if abort:
        FailMiserably()

def PostProcessing():
    '''This routine is called by the server to bring configuration options
into a usable form. Some values are changed into other data types.'''
    try:
        l = map(string.strip,conf['Resolutions'].split(','))
        conf['Resolutions'] = map(int,l)
    except:
        Utils.Error('Value of "Resolutions" option must be a comma-separated'+
                    ' list of positive integers.')
        FailMiserably()
    try:
        conf['IdCheckRegExp'] = re.compile(conf['IdCheckRegExp'])
    except:
        Utils.Error('Regular expression in "IdCheckRegExp" cannot be '
                    'compiled.')
        etype, value, tb = sys.exc_info()
        lines = traceback.format_exception(etype,value,tb)
        Utils.Error(string.join(lines),prefix="")
        FailMiserably()
    if not(conf.has_key('GuestIdRegExp')):
        conf['GuestIdRegExp'] = '^$'   # matches only the empty string
    try:
        conf['GuestIdRegExp'] = re.compile(conf['GuestIdRegExp'])
    except:
        Utils.Error('Regular expression in "GuestIdRegExp" cannot be '
                    'compiled.')
        etype, value, tb = sys.exc_info()
        lines = traceback.format_exception(etype,value,tb)
        Utils.Error(string.join(lines),prefix="")
        FailMiserably()
    try:
        conf['GeneralMessages'] = Utils.StringFile(conf['GeneralMessageFile'])
    except:
        Utils.Error('Cannot read general messages for results pages, assuming'
                    ' no messages.', prefix="Warning:")
        conf['GeneralMessages'] = ''
        traceback.print_exc()
    for i in range(len(conf['AccessList'])):
        s = conf['AccessList'][i]
        try:
            pos = s.find('/')
            if pos < 0:
                Utils.Error('Range in AccessList must contain a slash:\n'+s)
                FailMiserably()
            conf['AccessList'][i] = (socket.inet_aton(s[:pos]),
                                     socket.inet_aton(s[pos+1:]))
        except:
            traceback.print_exc()
            Utils.Error('Cannot parse IP range for AccessList: '+s)
            FailMiserably()
    for i in range(len(conf['AdministrationAccessList'])):
        s = conf['AdministrationAccessList'][i]
        try:
            pos = s.find('/')
            if pos < 0:
                Utils.Error('Range in AdministrationAccessList must contain '
                            'a slash:\n'+s)
                FailMiserably()
            conf['AdministrationAccessList'][i] = (socket.inet_aton(s[:pos]),
                                                   socket.inet_aton(s[pos+1:]))
        except:
            traceback.print_exc()
            Utils.Error('Cannot parse IP range for AdministrationAccessList: '+
                        s)
            FailMiserably()
    # Give a default for the DocumentRoot:
    if not(conf.has_key('DocumentRoot')):
        conf['DocumentRoot'] = os.path.join(home,'html')
    # Give a default for GroupInfoFile:
    if not(conf.has_key('GroupInfoFile')):
        conf['GroupInfoFile'] = os.path.join(home,'data/groupinfo.txt')
    # Give a default for ExtraLaTeXHeader:
    if not(conf.has_key('ExtraLaTeXHeader')):
        conf['ExtraLaTeXHeader'] = ''
    # Preparse the PDFTemplate:
    conf['PDFTemplate'] = SimpleTemplate.ParseString(conf['PDFTemplate'])
    # Same for NoTable variant:
    if not conf.has_key('PDFTemplateNoTable'):
         conf['PDFTemplateNoTable'] = ''
    conf['PDFTemplateNoTable'] = SimpleTemplate.ParseString(conf['PDFTemplateNoTable'])
    # Now parse the GradingFunction if applicable:
    if conf.has_key('GradingFunction'):
        d = {}
        try:
            exec conf['GradingFunction']+'\n' in d
            conf['GradingFunction'] = d['Grade']
        except:
            etype, value, tb = sys.exc_info()
            lines = traceback.format_exception(etype,value,tb)
            Utils.Error('Cannot parse ScheinDecisionFunction.\n'+
                        string.join(lines))
            conf['GradingFunction'] = None
    else:
        conf['GradingFunction'] = None
    if not(conf.has_key('GradingActive')):
        conf['GradingActive'] = 0


