# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for printing a high score table
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

import Config, Data, Plugins

class HighScoreTable( Plugins.OkusonSimpleExtension ):
    numberOfEntries = 10
    def __init__( self, options = {} ):
        try:
            self.numberOfEntries = int(options['entries'][0])
        except:
            pass
        if self.numberOfEntries < 0:
            self.numberOfEntries = 10
    def name( self ):
        return self.__class__.__name__
    def cssCode( self ):
        return ( 'table.highscore th { text-align: center; }\n'
                 'table.highscore td { text-align: center; }\n')
    def htmlCode( self ):
        totalScore = []
        for k in Data.people.keys():
            if not(Config.conf['GuestIdRegExp'].match(k)):
                totalScore.append( Data.people[k].TotalScore() )
        totalScore.sort()
        totalScore.reverse()
        s = ( '\n<table class="highscore"><tr><th>Höchstpunktzahlen</th></tr>\n' )
        for t in totalScore[:self.numberOfEntries]:
            s += ( '<tr><td>' + locale.str(t) + '</td></tr>\n' )
        s += '</table>\n'
        return s

Plugins.register( HighScoreTable.__name__,
                  'Statistik',
                  'Ausgabe einer Highscore Tabelle',
                  'Dieses Plugin dient zur Erzeugung einer Highscore Tabelle.',
                  'Ingo Klöcker',
                  'Ingo Klöcker',
                  '2005',
                  HighScoreTable )
