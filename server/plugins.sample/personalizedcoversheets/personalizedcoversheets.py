# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for creating personalized cover sheets for exams
#
#   Copyright (C) 2006  Ingo Klöcker <ingo.kloecker@mathA.rwth-aachen.de>
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

import locale, random

import Config, Data, Exercises, Plugins

from fmTools import Utils, LatexImage

class PersonalizedCoverSheets( Plugins.OkusonExtension ):
    examnr = 0
    copies = 1 # number of copies of the cover sheet per person
    exportType = 'pdf'
    options = {}
    def __init__( self, options = {} ):
        try:
            self.examnr = int(options['examnr'][0])
        except:
            pass
        try:
            self.copies = int(options['copies'][0])
        except:
            pass
        try:
            self.exportType = options['type'][0]
        except:
            pass
        self.options = options
    def name( self ):
        return self.__class__.__name__
    def necessaryCredentials( self ):
        return Plugins.Admin
    def returnType( self ):
        return Plugins.File
    def title( self ):
        return 'Generierung von personalisierten Deckbl&auml;ttern f&uuml;r Klausuren'
    def formCode( self ):
        if Data.Exam.maxexamnumber >= 1:
          s = 'Generierung von personalisierten Deckbl&auml;ttern f&uuml;r Klausur <select name="examnr">\n'
          for i in range( Data.Exam.maxexamnumber ):
            s += ( '<option value="' + str(i) + '">' + str(i) + '</option>\n' )
          s += '</select>\n'
          s += ' als '
          s += ( '<select name="type">\n'
               '<option value="tex">TeX-Datei</option>\n'
               '<option value="pdf" selected="selected">PDF-Datei</option>\n'
               '</select>\n' )
          s += '<br />\n'
          s += 'Anzahl der Kopien: '
          s += '<input type="text" name="copies" value="1" size="2" maxlength="1" />\n'
        else:
          s = 'Generierung von personalisierten Deckbl&auml;ttern f&uuml;r Klausuren '
          s += '(bislang keine Klausuren eingetragen)\n'
        return s
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
    def headAndBody( self ):
        latex = self.createLaTeXFile()
        if self.exportType == 'tex':
            head = { 'Content-type' : 'text/x-latex',
                     'Content-Disposition' : 'attachment; filename="deckblaetter.tex"'}
            return ( head, latex )
        else:
            head = { 'Content-type' : 'application/pdf',
                     'Content-Disposition' : 'attachment; filename="deckblaetter.pdf"'}
            pdf = LatexImage.LatexToPDF( latex )
            if not pdf:
                pdf = ''
            return ( head, pdf )
    def createLaTeXFile( self ):
        courseName = Config.conf['CourseName']
        lecturer = self.getString( 'lecturer' ).strip().replace( ' ', '~' )
        semester = self.getString( 'semester' ).strip()
        date = self.getString( 'date' ).strip()
        if date == '':
            date = '\\today'
        # count number of registrations
        count = 0
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            p = Data.people[k]
            if self.examnr < len( p.exams ) and \
               p.exams[self.examnr] != None and \
               p.exams[self.examnr].registration:
                count += 1
        # get people for which a Deckblatt should be created
        s = ''
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            p = Data.people[k]
            if self.examnr < len( p.exams ) and \
               p.exams[self.examnr] != None and \
               p.exams[self.examnr].registration:
                for i in range( self.copies ):
                    s += ( r'\deckblatt{%s}{%s}{%s}{%s}{%s}{%s}' %
                        ( lecturer, semester, courseName, date,
                            p.lname + ', ' + p.fname, k ) )
                    s += '\n'
        latexInput = LatexHead + s + LatexFoot
        return latexInput
    def getString( self, optionName ):
        if optionName not in self.options:
            return ''
        return self.options[optionName][0]

LatexHead = r'''
\documentclass[12pt,ngerman,a4paper,DIV20]{scrartcl}
\usepackage{times}
\usepackage[T1]{fontenc}
\usepackage[latin9]{inputenc}

\setlength{\parindent}{0pt}

\pagestyle{empty}
\usepackage{array}

\makeatletter

\providecommand{\tabularnewline}{\\}

\usepackage{babel}
\makeatother

\newcommand{\dozent}{Prof.~Dr.~R.~Stens}
\newcommand{\datum}{23.~August~2006}
\newcommand{\klausurtitel}{4. Klausur zur Analysis I}
\newcommand{\bearbeitungszeit}{150}
\newcommand{\hilfsmittel}{keine}

\RequirePackage{ifthen}%
\RequirePackage{graphics}%
\RequirePackage{color}%
%
\newlength{\sperren}%
%
\newcommand{\lamalogoblau}[5]{%
\setlength{\sperren}{0.06em}
\begin{minipage}[t]{1.5cm}%
\scalebox{0.1}{\includegraphics{/okuson/share/logo-blue-16cm-A25px}}%
\end{minipage} \\[-1.6cm]%
\hspace*{2.2cm}%
\begin{minipage}[t]{8cm}%
\textsc{\large L\hspace*{\sperren}%
e\hspace*{\sperren}%
h\hspace*{\sperren}%
r\hspace*{\sperren}%
s\hspace*{\sperren}%
t\hspace*{\sperren}%
u\hspace*{\sperren}%
h\hspace*{\sperren}%
l\hspace*{\sperren}%
\ \hspace*{\sperren}%
A\hspace*{\sperren}%
\ \hspace*{\sperren}%
f\hspace*{\sperren}%
\"u\hspace*{\sperren}%
r\hspace*{\sperren}%
\ \hspace*{\sperren}%
M\hspace*{\sperren}%
a\hspace*{\sperren}%
t\hspace*{\sperren}%
h\hspace*{\sperren}%
e\hspace*{\sperren}%
m\hspace*{\sperren}%
a\hspace*{\sperren}%
t\hspace*{\sperren}%
i\hspace*{\sperren}%
k\hspace*{\sperren}%
} \\
#1 \\
#2 \\
\end{minipage}%
\hfill Aachen, den \ifthenelse{\equal{#3}{}}{\today}{#3} \\[-1.5\baselineskip]
{\center\textbf{\hrulefill \\[.2\baselineskip] \Large{}#4} \ifthenelse{\equal{#5}{}}{}{\\[0.25\baselineskip] \small{}#5\normalsize}
\\[-.6\baselineskip] \hrulefill}\\[-\baselineskip]
}%

\newcommand{\deckblatt}[6]{%
\lamalogoblau{\dozent}{}{\datum}{\textbf{\Large \klausurtitel}}{{\small Bearbeitungszeit: \bearbeitungszeit{} Minuten; zugelassene Hilfsmittel: \hilfsmittel{}}}{\small \par}

\vfill{}
\begin{center}
\textbf{\LARGE
\begin{tabular}{l}
Name: #5\tabularnewline
~\tabularnewline
Matrikelnummer: #6\tabularnewline
\end{tabular}}
\end{center}

\vfill{}
\begin{center}\makebox[\linewidth]{\tabcolsep.30cm\doublerulesep.5cm\begin{tabular}{%
|l%
|>{\centering}p{0.6cm}% A 1
|>{\centering}p{0.6cm}% A 2
|>{\centering}p{0.6cm}% A 3
|>{\centering}p{0.6cm}% A 4
|>{\centering}p{0.6cm}% A 5
|>{\centering}p{0.6cm}% A 6
|>{\centering}p{0.6cm}% A 7
|>{\centering}p{0.6cm}% A 8
|>{\centering}p{0.6cm}% A 9
|>{\centering}p{0.6cm}|% A 10
}
\hline
\rule[-5mm]{0mm}{12mm}Aufgabe&
  1 &
  2 &
  3 &
  4 &
  5 &
  6 &
  7 &
  8 &
  9 &
 10
\tabularnewline
\hline
\rule[-5mm]{0mm}{12mm}max. Punktzahl&
  4 &
  6 &
 14 &
  6 &
 14 &
 12 &
  4 &
  8 &
  6 &
 10
\tabularnewline
\hline
\rule[-5mm]{0mm}{12mm}Ihre Punktzahl&
  % A 1
& % A 2
& % A 3
& % A 4
& % A 5
& % A 6
& % A 7
& % A 8
& % A 9
& % A 10
\tabularnewline
\hline
\rule[-5mm]{0mm}{12mm}korrigiert von&
  % A 1
& % A 2
& % A 3
& % A 4
& % A 5
& % A 6
& % A 7
& % A 8
& % A 9
& % A 10
\tabularnewline
\hline
\hline
\rule[-5mm]{0mm}{12mm}Aufgabe&
 11 &
 12 &
 13 &
 14 &
 15 &
 16 &
 17 &
 18 &
\multicolumn{2}{c|}{$\sum$}%
\tabularnewline
\hline
\rule[-5mm]{0mm}{12mm}max. Punktzahl&
  8 &
  6 &
  8 &
 10 &
  6 &
  9 &
  7 &
 12 &
\multicolumn{2}{c|}{150}%
\tabularnewline
\hline
\rule[-5mm]{0mm}{12mm}Ihre Punktzahl&
  % A 11
& % A 12
& % A 13
& % A 14
& % A 15
& % A 16
& % A 17
& % A 18
& \multicolumn{2}{c|}{} % Summe
\tabularnewline
\hline
\rule[-5mm]{0mm}{12mm}korrigiert von&
  % A 11
& % A 12
& % A 13
& % A 14
& % A 15
& % A 16
& % A 17
& % A 18
& \multicolumn{2}{c|}{} % Summe
\tabularnewline
\hline
\end{tabular}}\end{center}\vfill{}
 
\clearpage
}

\begin{document}
'''

LatexFoot = r'''\end{document}
'''

Plugins.register( PersonalizedCoverSheets.__name__,
                  'Klausuren',
                  'Erzeugung von personalisierten Deckblättern für Klausuren',
                  'Dieses Plugin dient zur Erzeugung von personalisierten Deckblätter für Klausuren, d. h. von Deckblätter, die mit Name und Matrikelnummer versehen sind.',
                  'Ingo Klöcker',
                  'Ingo Klöcker',
                  '2006',
                  PersonalizedCoverSheets )
