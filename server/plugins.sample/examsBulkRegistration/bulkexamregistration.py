# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for changing exam registrations
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

import time
import Data, Plugins

from fmTools import Utils, AsciiData

class BulkExamRegistration( Plugins.OkusonExtension ):
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
    def necessaryCredentials( self ):
        return Plugins.Admin
    def returnType( self ):
        return Plugins.HTML
    def title( self ):
        return '&Auml;nderung von Klausuranmeldungen'
    def formCode( self ):
        s = '<input type="hidden" name="state" value="0" />\n'
        if Data.Exam.maxexamnumber >= 1:
          s += '&Auml;nderung der Anmeldungen zu Klausur <select name="examnr">\n'
          for i in range( Data.Exam.maxexamnumber ):
            s += ( '<option value="' + str(i) + '">' + str(i) + '</option>\n' )
          s += '</select>\n'
        else:
          s += '&Auml;nderung von Klausuranmeldungen '
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
        if self.examnr < 0:
            return '<emph>Error: Invalid exam number</emph>'
        if self.state == 0:
            return self.createExamRegistrationMask()
        else:
            return self.createSuccessMessage()
    def createExamRegistrationMask( self ):
        examnr = self.examnr
        s = '<h3>An-/Abmeldung von Klausur ' + str(examnr) + '</h3>\n'
        s += ( '<form action="/AdminExtension" method="post">\n'
               '<div><input type="hidden" name="extension" value="' + 
               self.name() + '" />\n'
               '<input type="hidden" name="state" value="1" />\n'
               '<input type="hidden" name="examnr" value="' +
               str(examnr) + '" /></div>\n' )
        table = []
        table.append( ['', 'Matr.-Nr.', 'Name', 'Klausurteilnahme'] )
        l = Utils.SortNumerAlpha( Data.people.keys() )
        counter = 0
        for k in l:
            counter += 1
            p = Data.people[k]
            checked = ''
            if ( examnr < len( p.exams ) and
                 p.exams[examnr] != None and
                 p.exams[examnr].registration == 1 ):
                    checked = 'checked="checked" '
            table.append( [ str(counter), k,
                            Utils.CleanWeb( p.lname ) + ', ' +
                            Utils.CleanWeb( p.fname ),
                            '<input type="checkbox" name="T' + k + '" '
                            'value="true" ' + checked + ' />' ] )
        s += createHTMLTable( table )
        s += ( '<p><input type="submit" name="Action" value="Send" />\n'
# Not sure how I can make of the AdminPasswdField() method. OTOH, this method
# only uses a global variable, so there's no reason for it to be a method of
# a class.
#               '' + handler.AdminPasswdField() + '\n'
               '<input type="password" size="16" maxlength="16" '
               'name="passwd" value="" /></p>\n'
               '</form>\n' )
        return s
    def createSuccessMessage( self ):
        examnr = self.examnr
        # evaluate the changes
        registrations = {}
        l = Utils.SortNumerAlpha( Data.people.keys() )
        for k in l:
            p = Data.people[k]
            wasRegistered = ( examnr < len( p.exams ) and
                              p.exams[examnr] != None and
                              p.exams[examnr].registration == 1 )
            shouldBeRegistered = self.options.has_key( 'T' + k )
            if wasRegistered != shouldBeRegistered:
                registrations[k] = int( shouldBeRegistered )

        # put the changes into the database
        registered = []
        unregistered = []
        Data.Lock.acquire()
        timestamp = int( time.time() )
        for k in Utils.SortNumerAlpha( registrations.keys() ):
            v = registrations[k]
            line = AsciiData.LineTuple( ( k, str(examnr), str(v),
                                          str(timestamp) ) )
            try:
                Data.examregdesc.AppendLine( line )
            except:
                Data.Lock.release()
                Utils.Error( '[' + Utils.LocalTimeString() +
                             '] Failed to register person for exam:\n' + line )
                return '<emph>Error: The changes could not be saved.</emph>'
            p = Data.people[k]
            while len( p.exams ) < examnr + 1:
                p.exams.append( None )
            if p.exams[examnr] == None:
                p.exams[examnr] = Data.Exam()
            p.exams[examnr].timestamp = timestamp
            p.exams[examnr].registration = v
            if Data.Exam.maxexamnumber < examnr + 1:
                Data.Exam.maxexamnumber = examnr + 1
            line = ( Utils.CleanWeb( p.lname ) + ', ' +
                     Utils.CleanWeb( p.fname ) + ' (' + k + ')' )
            if v == 1:
                registered.append( line )
            else:
                unregistered.append( line )
        Data.Lock.release()

        Utils.Error( '[' + Utils.LocalTimeString() + '] Changed registrations '
                     'for exam ' + str(examnr),
                     prefix = 'BulkExamRegistration: ' )
        s = '<h3>An-/Abmeldung von Klausur ' + str(examnr) + '</h3>\n'
        if len( registered ) > 0:
            s += ( '<div>Die folgenden Personen wurden zur Klausur angemeldet:'
                   '</div>\n'
                   '<ul>\n<li>' + str('</li>\n<li>').join( registered ) + 
                   '</li>\n</ul>\n' )
        if len( unregistered ) > 0:
            s += ( '<div>Die folgenden Personen wurden von der Klausur '
                   ' abgemeldet:</div>\n'
                   '<ul>\n<li>' + str('</li>\n<li>').join( unregistered ) + 
                   '</li>\n</ul>\n' )
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

Plugins.register( BulkExamRegistration.__name__,
                  'Klausuren',
                  'Änderung von Klausuranmeldungen',
                  'Dieses Plugin erlaubt das einfache An- bzw. Abmelden aller Kursteilnehmer von einer Klausur.',
                  'Ingo Klöcker',
                  'Ingo Klöcker',
                  '2005',
                  BulkExamRegistration )
