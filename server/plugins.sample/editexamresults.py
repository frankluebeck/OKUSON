# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for entering and editting the results of an exam
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
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import locale
import Data, Plugins

from fmTools import Utils, AsciiData

class EditExamResults( Plugins.OkusonExtension ):
    state = 0  # this plugin is implemented as finite state machine
    examnr = -1
    options = {}
    def __init__( self, options = {} ):
        try:
            self.state = int(options['state'][0])
        except:
            self.state = 0
        try:
            self.examnr = int(options['examnr'][0])
        except:
            self.examnr = -1
        self.options = options
    def name( self ):
        return self.__class__.__name__
    def isAdminExtension( self ):
        return True
    def returnType( self ):
        return Plugins.HTML
    def title( self ):
        return 'Eingabe von Klausurergebnissen'
    def formCode( self ):
        s = '<input type="hidden" name="state" value="0" />\n'
        s += 'Eingabe der Ergebnisse von Klausur <select name="examnr">\n'
        for i in range( Data.Exam.maxexamnumber ):
            s += ( '<option value="' + str(i) + '">' + str(i) + '</option>\n' )
        s += '</select>\n'
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
        if self.examnr < 0:
            return '<em>Error: Invalid exam number</em>'
        if self.state == 0:
            return self.createExamResultInputMask()
        else:
            return self.createSummary()
    def createExamResultInputMask( self ):
        examnr = self.examnr
        s = '<h3>Eingabe der Ergebnisse von Klausur ' + str(examnr) + '</h3>\n'
        s += ( '<p><em>Hinweis:</em> Es werden nur diejenigen '
               'Kursteilnehmer angezeigt, die zu dieser Klausur angemeldet '
               'sind.</p>' )
        s += ( '<form action="/AdminExtension" method="post">\n'
               '<div><input type="hidden" name="extension" value="' + 
               self.name() + '" />\n'
               '<input type="hidden" name="state" value="1" />\n'
               '<input type="hidden" name="examnr" value="' +
               str(examnr) + '" /></div>\n' )
        table = []
        table.append( ['', 'Matr.-Nr.', 'Name', 'Punkte', 
                       'Punkte in den einzelnen Aufgaben'] )
        l = Utils.SortNumerAlpha( Data.people.keys() )
        counter = 0
        oldmaxscore = ''
        for k in l:
            p = Data.people[k]
            checked = ''
            if ( examnr < len( p.exams ) and
                 p.exams[examnr] != None ):
                exam = p.exams[examnr]
                if ( exam.maxscore != 0 ):
                    oldmaxscore = locale.str( exam.maxscore )
                if ( exam.registration == 1 ):
                    counter += 1
                    oldtotalscore = ''
                    if ( exam.totalscore != -1 ):
                        oldtotalscore = locale.str( exam.totalscore )
                    table.append( [ str(counter), k,
                                Utils.CleanWeb( p.lname ) + ', ' +
                                Utils.CleanWeb( p.fname ),
                                '<input size="6" maxlength="6" '
                                'name="P' + str(examnr) + '_' + k + '" '
                                'value="' + oldtotalscore + '" />',
                                '<input size="40" maxlength="100" '
                                'name="S' + str(examnr) + '_' + k + '" '
                                'value="' + Utils.CleanWeb( exam.scores ) +
                                '" />' ] )
        s += ( '<p>Maximal erreichbare Punktzahl: '
               '<input name="maxscore" value="' + oldmaxscore + '" '
               'size="4" maxlength="4" /></p>\n' )
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
    def createSummary( self ):
        examnr = self.examnr
        # get the maxscore
        maxscore = self.getNumber( 'maxscore' )
        if maxscore == None:
            return '<em>Error: Invalid maximal score.</em>'
        elif maxscore == '':
            return '<em>Error: Missing maximal score.</em>'
        # get the individual scores
        scores = {}
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            score = self.getNumber( 'P' + str(examnr) + '_' + k, default = -1 )
            if score == None:
                return '<em>Error: Invalid score for ' + k + '.</em>'
            else:
                if score > maxscore:
                    return ( '<em>Error: Score for ' + k + ' exceeds the '
                             'maximal score.</em>' )
                scores[k] = [ score,
                              self.getString( 'S' + str(examnr) + '_' + k ) ]

        # put the changes into the database
        table = []
        table.append( ['', 'Matr.-Nr.', 'Name', 'Punkte', 
                       'Punkte in den einzelnen Aufgaben'] )
        counter = 0
        Data.Lock.acquire()
        for k in Utils.SortNumerAlpha( scores.keys() ):
            p = Data.people[k]
            while len( p.exams ) < examnr + 1:
                p.exams.append( None )
            newOrChanged = False
            # we only have to save non-default values for not yet existing
            # entries or changed values for existing entries
            if ( p.exams[examnr] == None or p.exams[examnr].maxscore == 0 ):
                # do we have non-default values?
                if ( scores[k][0] != -1 or scores[k][1] != '' ):
                    p.exams[examnr] = Data.Exam()
                    newOrChanged = True
            elif ( p.exams[examnr].totalscore != scores[k][0] or
                   p.exams[examnr].scores != scores[k][1] or
                   p.exams[examnr].maxscore != maxscore ):
                newOrChanged = True
            if newOrChanged:
                p.exams[examnr].totalscore = scores[k][0]
                p.exams[examnr].scores = scores[k][1]
                p.exams[examnr].maxscore = maxscore
                line = AsciiData.LineTuple( ( k, str(examnr), str(scores[k][0]),
                                              str(maxscore), scores[k][1] ) )
                try:
                    Data.examdesc.AppendLine( line )
                except:
                    Data.Lock.release()
                    Utils.Error( '[' + Utils.LocalTimeString() +
                                 '] Failed to store exam result:\n' + line )
                    return '<em>Error: The results could not be saved.</em>'
            if scores[k][0] != -1:
                counter += 1
                table.append( [ str(counter), k,
                                Utils.CleanWeb( p.lname ) + ', ' +
                                Utils.CleanWeb( p.fname ),
                                locale.str(scores[k][0]),
                                scores[k][1] ] )
        Data.Lock.release()

        Utils.Error( '[' + Utils.LocalTimeString() + '] Changed results '
                     'for exam ' + str(examnr),
                     prefix = self.name() + ': ' )
        s = '<h3>Ergebnisse von Klausur ' + str(examnr) + '</h3>\n'
        s += createHTMLTable( table )
        return s
    def getNumber( self, optionName, default = '' ):
        ''' Returns the number corresponding to the query option @p optionName
            or returns an empty string if the query option does not exist or is
            empty (except for possible whitespace) or returns None if the value
            of the query option is no valid number.'''
        if optionName not in self.options:
            return default
        # allow the usage of ',' instead of '.' for decimal numbers
        s = self.options[optionName][0].strip().replace( ',', '.' )
        if s == '':
            return default
        t = 0
        try:
            if '.' in s:
                t = float( s )
            else:
                t = int( s )
        except:
            return None
        return t
    def getString( self, optionName ):
        if optionName not in self.options:
            return ''
        return self.options[optionName][0]

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

Plugins.register( EditExamResults.__name__,
                  'Klausuren',
                  'Eingabe von Klausurergebnissen',
                  'Dieses Plugin erlaubt die Eingabe von Klausurergebnissen.',
                  'Ingo Klöcker',
                  'Ingo Klöcker',
                  '2005',
                  EditExamResults )
