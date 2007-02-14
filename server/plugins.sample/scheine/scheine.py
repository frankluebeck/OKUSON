# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for creating �ungsscheine
#
#   Copyright (C) 2005  Ingo Kl�ker <ingo.kloecker@mathA.rwth-aachen.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import locale

import Config, Data, Exercises, Plugins

from fmTools import Utils, LatexImage

class Scheine( Plugins.OkusonExtension ):
    state = 0  # this plugin is implemented as finite state machine
    options = {}
    mandatoryScore = -1 # the minimal total score necessary for getting a
                        # Schein; if -1 then the score is calculated as
                        # percentage of the maximal total score
    mandatoryScorePercentage = 0.333333
    def __init__( self, options = {} ):
        try:
            self.state = int( options['state'][0] )
        except:
            self.state = 0
        self.options = options
    def name( self ):
        return self.__class__.__name__
    def necessaryCredentials( self ):
        return Plugins.Admin
    def returnType( self ):
        if self.state == 0:
            return Plugins.HTML
        else:
            return Plugins.File
    def title( self ):
        return 'Generierung von &Uuml;bungsscheinen'
    def formCode( self ):
        return ( 'Generierung von &Uuml;bungsscheinen ('
                 '<input type="checkbox" name="nurScheinbedErf" value="true" '
                 'checked="checked" />'
                 'nur anzeigen, falls Scheinbedingung erf&uuml;llt)' )
    def cssCode( self ):
        return '''  table {
                        border          : none;
                        border-collapse : collapse;
                        border-spacing  : 0pt;
                        padding         : 0pt;
                    }
                    th {
                        border        : none;
                        border-left   : 1px solid black;
                        text-align    : left;
                        padding-left  : 15pt;
                        padding-right : 15pt;
                        font-weight   : bold;
                    }
                    th:first-child {
                        border-left   : none;
                    }
                    td {
                        border        : none;
                        border-top    : 1px solid black;
                        border-left   : 1px solid black;
                        text-align    : left;
                        padding-left  : 15pt;
                        padding-right : 15pt;
                        font-weight: normal;
                    }
                    td:first-child {
                        border-left   : none;
                    }'''
    def htmlCode( self ):
        lecturer = Config.conf['Lecturer']
        semester = Config.conf['Semester']
        s = ( '<hr />\n'
              '<form action="/AdminExtension" method="post">\n'
              '<div><input type="hidden" name="extension" value="' +
              self.name() + '" />\n'
               '<input type="hidden" name="state" value="1" /></div>\n'
              '<p>'
              'Dozent: <input size="30" maxlength="40" name="lecturer" '
              'value="' + lecturer + '" /><br />\n'
              'Semester: <input size="30" maxlength="40" name="semester" '
              'value="' + semester + '" /><br />\n'
              'Scheine: <input type="radio" name="benotet" '
              'value="ja" />benotet / '
              '<input type="radio" name="benotet" '
              'value="nein" />unbenotet<br />\n'
              'Datum: <input size="20" maxlength="20" name="date" '
              'value="" /> (falls leer wird heutiges Datum genommen)'
              '</p>\n'
              '<p>Waehlen Sie diejenigen Kursteilnehmer aus, fuer die ein '
              'Schein generiert werden soll.</p>\n' )
        table = []
        titleRow = [ '', 'Schein', 'Matr.-Nr.', 'Name', 'Uebungspunkte' ]
        for i in range( Data.Exam.maxexamnumber ):
            titleRow.append( 'Klausur ' + str( i ) )
        titleRow.append( 'Bemerkung' )
        table.append( titleRow )
        nurScheinbedErf = ( self.getString( 'nurScheinbedErf' ) == 'true' )
        l = Utils.SortNumerAlpha( Data.people.keys() )
        counter = 0
        for k in l:
            p = Data.people[k]
            if nurScheinbedErf and not self.ScheinbedingungErfuellt( p ):
                continue
            counter += 1
            row = [ str( counter ) ]
            if self.ScheinbedingungErfuellt( p ):
                row.append( '<input type="checkbox" name="Schein' + k + '" '
                            'value="true" />' )
            else:
                row.append( '-' )
            row += [ k, Utils.CleanWeb( p.lname + ', ' + p.fname ),
                     locale.str( p.TotalScore() ) ]
            for i in range( Data.Exam.maxexamnumber ):
                if ( len( p.exams ) <= i or p.exams[i] == None or
                     p.exams[i].totalscore < 0 ):
                    row.append( '-' )
                else:
                    row.append( locale.str( p.exams[i].totalscore ) )
            if self.ScheinbedingungErfuellt( p ):
                row.append( 'Scheinbedingung ist erfuellt' )
            else:
                row.append( 'Scheinbedingung ist nicht erfuellt' )
            table.append( row )
        s += createHTMLTable( table )
        s += ( '<p><input type="submit" name="Action" value="Send" />\n'
# Not sure how I can make use of the AdminPasswdField() method. OTOH, this
# method only uses a global variable, so there's no reason for it to be a
# method of a class.
#               '' + handler.AdminPasswdField() + '\n'
               '<input type="password" size="16" maxlength="16" '
               'name="passwd" value="" /></p>\n'
               '</form>\n' )
        return s
    def ScheinbedingungErfuellt( self, p ):
        # calculate the mandatory minimal total score if necessary
        if self.mandatoryScore < 0:
            maxtotalscore = self.MaxTotalMCScore()
            score = self.MaxTotalMandatoryHomeScore()
            if score > -1:
                maxtotalscore += score
            self.mandatoryScore = self.mandatoryScorePercentage * maxtotalscore
        # check whether the participant has gained enough points in the sheets
        if self.mandatoryScore > p.TotalScore():
            return False
        # check whether the participant has gained enough points in the exams (geandert)****
        if ( ( len( p.exams ) > 0 and p.exams[0] != None and
               p.exams[0].totalscore >= 28 ) or
             ( len( p.exams ) > 2 and p.exams[2] != None and
               p.exams[2].totalscore >= 22 ) ):
            return True
        return False
    # copied from WebWorkers.py
    def MaxTotalMCScore(self):
        l = Exercises.SheetList()
        maxtotalmcscore = 0
        for nr,name,s in l:
            if s.counts and s.IsClosed():   # sheet already closed 
                maxtotalmcscore += s.MaxMCScore()
        return maxtotalmcscore
    def MaxTotalHomeScore(self):
        l = Exercises.SheetList()
        maxtotalhomescore = 0
        for nr,name,s in l:
            if s.counts and s.IsClosed():   # sheet already closed 
                if s.maxhomescore == -1:
                    return -1    # invalid homescore -> abort calculation
                maxtotalhomescore += s.maxhomescore
        return maxtotalhomescore
    def MaxTotalOptionalHomeScore(self):
        l = Exercises.SheetList()
        maxtotalstarhomescore = 0
        for nr,name,s in l:
            if s.counts and s.IsClosed():   # sheet already closed 
                maxtotalstarhomescore += s.starhomescore
        return maxtotalstarhomescore
    def MaxTotalMandatoryHomeScore(self):
        maxtotalhomescore = self.MaxTotalHomeScore()
        if maxtotalhomescore == -1:
            return -1
        else:
            return maxtotalhomescore - self.MaxTotalOptionalHomeScore()
    # end of copied from WebWorkers.py
    def headAndBody( self ):
        courseName = Config.conf['CourseName']
        lecturer = self.getString( 'lecturer' ).strip().replace( ' ', '~' )
        semester = self.getString( 'semester' ).strip()
        benotet = ( self.getString( 'benotet' ) == 'ja' )
        date = self.getString( 'date' ).strip()
        if date == '':
            date = '\\today'
        # get people for which a Schein should be created
        s = ''
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            if self.getString( 'Schein' + k ) == 'true':
                p = Data.people[k]
                if benotet:
                    grade = self.calculateGrade( p )
                    s += ( r'\scheinMitNote{%s}{%s}{%s}{%s}{%s}{%s}{%s}' %
                           ( lecturer, semester, courseName, date,
                             p.fname + ' ' + p.lname, k, grade ) )
                else:
                    s += ( r'\schein{%s}{%s}{%s}{%s}{%s}{%s}' %
                           ( lecturer, semester, courseName, date,
                             p.fname + ' ' + p.lname, k ) )
                s += '\n'
        latexInput = LatexHead + s + LatexFoot
#        return ( { 'Content-type' : 'text/x-latex',                   'Content-Disposition' : 'attachment; filename="scheine.tex"'}, latexInput )
        pdf = LatexImage.LatexToPDF( latexInput )
        if not pdf:
            pdf = ''
        head = { 'Content-type' : 'application/pdf',
                 'Content-Disposition' : 'attachment; filename="scheine.pdf"'}
        return ( head, pdf )
    def calculateGrade( self, p ):
        grades    = [ '1,0', '1,3', '1,7', '2,0', '2,3', '2,7', '3,0', '3,3', '3,7', '4,0', '5,0' ]
        minPoints = [  56.5,  53,  50,  47,  44,  41.5,  37,  34,  31,  28,  0 ]
        if ( len( p.exams ) > 0 and p.exams[0] != None and
             p.exams[0].totalscore >= 28 ):
            for i in range( len( minPoints ) ):
                if ( p.exams[0].totalscore >= minPoints[i] ):
                    return grades[i]
        if ( len( p.exams ) > 2 and p.exams[2] != None and
             p.exams[2].totalscore >= 22 ):
            for i in range( len( minPoints ) ):
                if ( p.exams[2].totalscore >= minPoints[i] ):
                    return grades[i]
        return '5,0'
    def getString( self, optionName ):
        if optionName not in self.options:
            return ''
        return self.options[optionName][0]

def createHTMLTable( table, className = None ):
    if className == None:
        s = '<table>\n<thead>\n'
    else:
        s = '<table class="' + className + '">\n<thead>\n'
    # first row is table head
    s += '<tr>'
    for cell in table[0]:
        s += '<th>' + cell + '</th>'
    s += '</tr>\n'
    s += '</thead>\n<tbody>\n'
    for row in table[1:]:
        s += '<tr>'
        for cell in row:
            s += '<td>' + cell + '</td>'
        s += '</tr>\n'
    s += '</tbody>\n</table>\n'
    return s

LatexHead = r'''\documentclass[12pt,a4paper]{article}
\usepackage[ngerman,activeacute]{babel}
\usepackage{geometry}
\usepackage[latin1]{inputenc}
\geometry{a4paper,body={442.65375pt,636.60028pt}}
\addtolength{\topmargin}{-15mm}
\addtolength{\textheight}{20mm}
\usepackage{times}
\newlength{\solang}
\pagestyle{empty}
\parindent 0em


\def\smallskip{\vspace{4mm}}
\def\midskip{\vspace{8mm}}
\def\bigskip{\vspace{12mm}}

\newcommand{\schein}[6]{%
\settowidth{\solang}{Rhein.-Westf.\ Technische Hochschule Aachen}
\parbox[t]{\solang}{%
\textsc{\large Lehrstuhl~A~f\"{u}r Mathematik}\\
Rhein.-Westf.\ Technische Hochschule Aachen\\
#1}
\hfill
\settowidth{\solang}{Tel.: 0241/80--94531}
\parbox[t]{\solang}{%
52062 Aachen\\
Templergraben 55\\
Tel.: 0241/80--94531}

\vspace{10mm}

\centerline{\large\bf \"{U}bungsschein}

\vspace{7mm}

#5, Matrikelnummer~#6, hat im #2
an den \"{U}bungen und der Klausur zur Vorlesung
\begin{center}
  \textbf{#3}
\end{center}
mit Erfolg teilgenommen.

\vspace{7mm}

Aachen, den #4

\vfill

\begin{center}
  {\bf\large Kopie}
\end{center}
\settowidth{\solang}{Rhein.-Westf.\ Technische Hochschule Aachen}
\parbox[t]{\solang}{%
\textsc{\large Lehrstuhl~A~f\"{u}r Mathematik}\\
Rhein.-Westf.\ Technische Hochschule Aachen\\
#1}
\hfill
\settowidth{\solang}{Tel.: 0241/80--94531}
\parbox[t]{\solang}{%
52062 Aachen\\
Templergraben 55\\
Tel.: 0241/80--94531}

\vspace{10mm}

\centerline{\large\bf \"{U}bungsschein}

\vspace{7mm}

#5, Matrikelnummer~#6, hat im #2
an den \"{U}bungen und der Klausur zur Vorlesung
\begin{center}
  \textbf{#3}
\end{center}
mit Erfolg teilgenommen.

\vspace{7mm}

Aachen, den #4

\vspace*{10mm}

\clearpage
}

\newcommand{\scheinMitNote}[7]{%
\settowidth{\solang}{Rhein.-Westf.\ Technische Hochschule Aachen}
\parbox[t]{\solang}{%
\textsc{\large Lehrstuhl~A~f\"{u}r Mathematik}\\
Rhein.-Westf.\ Technische Hochschule Aachen\\
#1}
\hfill
\settowidth{\solang}{Tel.: 0241/80--94531}
\parbox[t]{\solang}{%
52062 Aachen\\
Templergraben 55\\
Tel.: 0241/80--94531}

\vspace{10mm}

\centerline{\large\bf \"{U}bungsschein}

\vspace{7mm}

#5, Matrikelnummer~#6, hat im #2
an den \"{U}bungen und der Klausur zur Vorlesung
\begin{center}
  \textbf{#3}
\end{center}
teilgenommen und mit der Note #7 bestanden.

\vspace{7mm}

Aachen, den #4

\vfill

\begin{center}
  {\bf\large Kopie}
\end{center}
\settowidth{\solang}{Rhein.-Westf.\ Technische Hochschule Aachen}
\parbox[t]{\solang}{%
\textsc{\large Lehrstuhl~A~f\"{u}r Mathematik}\\
Rhein.-Westf.\ Technische Hochschule Aachen\\
#1}
\hfill
\settowidth{\solang}{Tel.: 0241/80--94531}
\parbox[t]{\solang}{%
52062 Aachen\\
Templergraben 55\\
Tel.: 0241/80--94531}

\vspace{10mm}

\centerline{\large\bf \"{U}bungsschein}

\vspace{7mm}

#5, Matrikelnummer~#6, hat im #2
an den \"{U}bungen und der Klausur zur Vorlesung
\begin{center}
  \textbf{#3}
\end{center}
teilgenommen und mit der Note #7 bestanden.

\vspace{7mm}

Aachen, den #4

\vspace*{10mm}

\clearpage
}

\begin{document}
'''

LatexFoot = r'''\end{document}
'''

Plugins.register( Scheine.__name__,
                  'Scheine',
                  'Erzeugung von \"{U}bungsscheinen',
                  'Dieses Plugin dient zur Erzeugung von \"{U}bungsscheinen.',
                  'Ingo Kl\"{o}cker',
                  'Ingo Kl\"{o}cker',
                  '2005',
                  Scheine )
