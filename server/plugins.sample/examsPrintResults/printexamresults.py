# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for viewing the results of an exam
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

import locale
import Data, Plugins

from fmTools import Utils, AsciiData

class PrintExamResults( Plugins.OkusonExtension ):
    examnr = -1
    def __init__( self, options = {} ):
        try:
            self.examnr = int(options['examnr'][0])
        except:
            self.examnr = -1
    def name( self ):
        return self.__class__.__name__
    def necessaryCredentials( self ):
        return Plugins.Admin
    def returnType( self ):
        return Plugins.HTML
    def title( self ):
        return 'Ergebnisse von Klausur ' + str(self.examnr)
    def formCode( self ):
        if Data.Exam.maxexamnumber >= 1:
          s = '<input type="hidden" name="state" value="0" />\n'
          s += 'Ausgabe der Ergebnisse von Klausur <select name="examnr">\n'
          for i in range( Data.Exam.maxexamnumber ):
            s += ( '<option value="' + str(i) + '">' + str(i) + '</option>\n' )
          s += '</select>\n'
        else:
          s = 'Klausurergebnisse '
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
        examnr = self.examnr
        if examnr < 0:
            return '<em>Error: Invalid exam number</em>'
        table = []
        table.append( ['', 'Matr.-Nr.', 'Name', 'Punkte', 
                       'Punkte in den einzelnen Aufgaben'] )
        l = Utils.SortNumerAlpha( Data.people.keys() )
        maxscore = 0
        counter = 0
        for k in l:
            p = Data.people[k]
            if ( examnr < len( p.exams ) and p.exams[examnr] != None ):
                exam = p.exams[examnr]
                if ( exam.maxscore != 0 ):
                    maxscore = exam.maxscore
                if ( exam.registration == 1 and exam.totalscore != -1 ):
                    counter += 1
                    table.append( [ str(counter), k,
                                    Utils.CleanWeb( p.lname ) + ', ' +
                                    Utils.CleanWeb( p.fname ),
                                    locale.str( exam.totalscore ),
                                    Utils.CleanWeb( exam.scores ) ] )
        s = ( '<p>Maximal erreichbare Punktzahl: ' + locale.str(maxscore) +
              '</p>\n' )
        s += createHTMLTable( table )
        return s
    def headAndBody( self ):
        pass

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

Plugins.register( PrintExamResults.__name__,
                  'Klausuren',
                  'Ausgabe von Klausurergebnissen',
                  'Dieses Plugin erlaubt die Ausgabe von Klausurergebnissen.',
                  'Ingo Klöcker',
                  'Ingo Klöcker',
                  '2005',
                  PrintExamResults )
