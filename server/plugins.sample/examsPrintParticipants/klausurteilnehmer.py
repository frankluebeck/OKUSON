# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for listing the participants of an exam
#
#   Copyright (C) 2005  Ingo Klöcker <ingo.kloecker@mathA.rwth-aachen.de>
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
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import Data, Plugins

from fmTools import Utils, LatexImage

class KlausurTeilnehmer( Plugins.OkusonExtension ):
    examnr = 0
    exportType = 'html'
    def __init__( self, options = {} ):
        try:
            self.exportType = options['type'][0]
        except:
            pass
        try:
            self.examnr = int(options['examnr'][0])
        except:
            pass
    def name( self ):
        return self.__class__.__name__
    def necessaryCredentials( self ):
        return Plugins.Admin
    def returnType( self ):
        if self.exportType == 'html':
            return Plugins.HTML
        else:
            return Plugins.File
    def title( self ):
        return 'Klausurteilnehmerliste'
    def formCode( self ):
        if Data.Exam.maxexamnumber >= 1:
          s = 'Liste der Teilnehmer für Klausur <select name="examnr">\n'
          for i in range( Data.Exam.maxexamnumber ):
            s += ( '<option value="' + str(i) + '">' + str(i) + '</option>\n' )
          s += '</select>\n'
          s += ' als '
          s += ( '<select name="type">\n'
                 '<option value="html">Webseite</option>\n'
                 '<option value="txt">Textdatei</option>\n'
                 '<option value="pdf">PDF-Datei</option>\n'
                 '</select>\n' )
        else:
          s = 'Klausurteilnehmerliste '
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
    def htmlCode( self ):
        s = '<h3>Liste der Teilnehmer an Klausur ' + str(self.examnr) + '</h3>\n'
        table = []
        table.append( ['', 'Matr.-Nr.', 'Name'] )
        l = Utils.SortNumerAlpha( Data.people.keys() )
        i = 0
        for k in l:
            p = Data.people[k]
            if self.examnr < len( p.exams ) and \
                p.exams[self.examnr] != None and \
                p.exams[self.examnr].registration:
                    i += 1
                    table.append( [ str(i), k, 
                                    Utils.CleanWeb( p.lname ) + ', ' + 
                                    Utils.CleanWeb( p.fname ) ] )
        s += createHTMLTable( table )
        return s
    def headAndBody( self ):
        s = ''
        head = {}
        if self.exportType == 'txt':
            s = self.createTextFile()
            head = { 'Content-type' : 'text/plain',
                     'Content-Disposition' : 'attachment; filename="klausurteilnehmer.txt"'}
        else:
            s = self.createPDFFile()
            head = { 'Content-type' : 'application/pdf',
                     'Content-Disposition' : 'attachment; filename="klausurteilnehmer.pdf"'}
        return ( head, s )
    def createTextFile( self ):
        s = '# All participants of exam number ' + str(self.examnr) + ':\n'
        s += '# ID:angemeldet?:name:fname\n'
        s += '# Time and date of export: ' + Utils.LocalTimeString() + '\n'
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            p = Data.people[k]
            if self.examnr < len( p.exams ) and \
                p.exams[self.examnr] != None and \
                p.exams[self.examnr].registration:
                    s += ( k + ':1:' + Utils.Protect( p.lname ) + ':' +
                           Utils.Protect( p.fname ) + '\n' )
            else:
                    s += ( k + ':0:' + Utils.Protect( p.lname ) + ':' +
                           Utils.Protect( p.fname ) + '\n' )
        return s
    def createPDFFile( self ):
        table = []
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            p = Data.people[k]
            if self.examnr < len( p.exams ) and \
               p.exams[self.examnr] != None and \
               p.exams[self.examnr].registration:
                    table.append( [ k, p.lname + ', ' + p.fname ] )
        s = ( '\\section*{Liste der Teilnehmer an Klausur ' + str(self.examnr) +
              '}\n' )
        lines = '\\cline{1-3}\\cline{5-7}\n'
        linesshort = '\\hline\n'
        eol = '\\\\\n'
        tablehead = ( '\\begin{tabular}{|r|c|l|l|r|c|l|}\n' + lines +
                      ' & Matr.-Nr. & Name & & & Matr.-Nr. & Name ' + eol + lines )
        tableheadshort = ( '\\begin{tabular}{|r|c|l|}\n' + linesshort +
                      ' & Matr.-Nr. & Name ' + eol + linesshort )
        tablefoot = lines + '\\end{tabular}\n'
        tablefootshort = linesshort + '\\end{tabular}\n'
        maxRows = 44
        offset = 0
        while offset < len( table ):
            if offset > 0:
                s += '\\newpage\n'
            twoColumns = ( offset + maxRows < len( table ) )
            if twoColumns:
                s += tablehead
            else:
                s += tableheadshort
            for i in range( offset, min( offset + maxRows, len( table ) ) ):
                s += str( i + 1 ) + ' & ' + table[i][0] + ' & ' + table[i][1]
                if twoColumns:
                    s += ' & & '
                    if i + maxRows < len( table ):
                        s += ( str( i + maxRows + 1 ) + ' & ' + 
                               table[i + maxRows][0] + ' & ' + 
                               table[i + maxRows][1] )
                    else:
                        s += '& &'
                s += eol
            if twoColumns:
                s += tablefoot
            else:
                s += tablefootshort
            offset += 2 * maxRows
        latexInput = LatexTemplate % ( s )
        pdf = LatexImage.LatexToPDF( latexInput )
        if not pdf:
            return ''
        return pdf

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

LatexTemplate = '''
\\documentclass[ngerman,DIV12]{scrartcl}
\\usepackage[T1]{fontenc}
\\usepackage[latin1]{inputenc}
\\usepackage{babel}
\\pagestyle{empty}

\\begin{document}
%s
\\end{document}
'''

Plugins.register( KlausurTeilnehmer.__name__,
                  'Klausuren',
                  'Ausgabe der Liste der Klausurteilnehmer',
                  'Dieses Plugin dient zur Erzeugung einer Liste der Teilnehmer an einer Klausur.',
                  'Ingo Klöcker',
                  'Ingo Klöcker',
                  '2005',
                  KlausurTeilnehmer )
