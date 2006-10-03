# -*- coding: ISO-8859-1 -*-
#
#   Okuson extension for public statistics
#
#   Copyright (C) 2006  Marc Ensenbach <Marc.Ensenbach@matha.rwth-aachen.de>
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

import Config, Data, Exercises, locale, Plugins

class PublicStatistics (Plugins.OkusonExtension):
    __field = 'totalscore'
    __showmax = False
    __titles = ['maximum', 'points', 'frequencies', 'cumulated']
    __fracreturned = 0.5

    def __init__ (self, options = {}):
        try:
            self.__field = options['field'][0].encode('ISO-8859-1', 'replace')
        except:
            pass
        try:
            showmax = options['showmax'][0].encode('ISO-8859-1', 'replace')
        except:
            showmax = ''
        if showmax.lower() <> 'no':
            self.__showmax = True
        try:
            titles = \
              options['titles'][0].encode('ISO-8859-1', 'replace').split(':')
        except:
            titles = []
        if len(titles) == 4:
            self.__titles = titles
        try:
            self.__fracreturned = \
              float(options['fracreturned'][0].replace(',', '.'))
        except:
            pass

    def name (self):
        return self.__class__.__name__

    def isAdminExtension (self):
        return False

    def onlyTag (self):
        return True

    def returnType (self):
        return Plugins.HTML

    def title (self):
        return 'Punktestatistik'

    def formCode (self):
        return ''

    def cssCode (self):
        return '@import url(/OKUSONStatistics.css);'

    def htmlCode (self):
        scoreDict = {}
        returnDict = {}
        maxScore = 0
        maxReturns = 0
        s = ''
        if self.__field[:9] == 'examscore':
            try:
                examnrlist = self.__field[9:].split('+')
            except:
                examnrlist = []
            if examnrlist == [] or examnrlist == ['']: examnrlist = range(24)
            for i in range(len(examnrlist)):
                try:
                    examnrlist[i] = int(examnrlist[i])
                except:
                    examnrlist[i] = 0
                if examnrlist[i] < 0: examnrlist[i] = 0
            for k in Data.people.keys():
                scoreDict[k] = 0
                returnDict[k] = 0
                if not(Config.conf['GuestIdRegExp'].match(k)):
                    p = Data.people[k]
                    currMaxScore = 0
                    currMaxReturns = 0
                    for examnr in examnrlist:
                        if examnr < len(p.exams):
                            if p.exams[examnr] <> None:
                                currMaxReturns += 1
                                if p.exams[examnr].totalscore <> -1:
                                    scoreDict[k] += p.exams[examnr].totalscore
                                    returnDict[k] += 1
                                if currMaxScore > -1:
                                    currMaxScore += p.exams[examnr].maxscore
                                    if p.exams[examnr].maxscore == -1:
                                        currMaxScore = -1
                    if currMaxScore > maxScore: maxScore = currMaxScore
                    if currMaxReturns > maxReturns: maxReturns = currMaxReturns
        else:
            fieldtitlelength = len('totalscore')
            if 'totalmcscore' in self.__field:
                fieldtitlelength = len('totalmcscore')
            if 'totalhomescore' in self.__field:
                fieldtitlelength = len('totalhomescore')
            try:
                sheetnrlist = self.__field[fieldtitlelength:].split('+')
            except:
                sheetnrlist = []
            if sheetnrlist == ['']: sheetnrlist = []
            for i in range(len(sheetnrlist)):
                try:
                    sheetnrlist[i] = int(sheetnrlist[i])
                except:
                    sheetnrlist[i] = 0
            for sheetNumber, sheetName, sheet in Exercises.SheetList():
                if not sheet.IsClosed():
                    continue
                if not sheet.counts:
                    continue
                if sheetnrlist <> [] and sheetNumber not in sheetnrlist:
                    continue
                maxReturns += 1
                maxScoreSheet = 0
                if 'totalmcscore' in self.__field:
                    maxScoreSheet = sheet.MaxMCScore()
                elif 'totalhomescore' in self.__field:
                    maxScoreSheet = sheet.maxhomescore
                elif 'totalscore' in self.__field:
                    if sheet.maxhomescore == -1:
                        maxScoreSheet = -1
                    else:
                        maxScoreSheet = sheet.MaxMCScore() + sheet.maxhomescore
                if maxScoreSheet == -1:
                    maxScore = -1
                elif maxScore <> -1:
                    maxScore += maxScoreSheet
            for k in Data.people.keys():
                p = Data.people[k]
                if not(Config.conf['GuestIdRegExp'].match(k)):
                    scoreDict[k] = 0
                    returnDict[k] = 0
                    for sheetNumber, sheetName, sheet in Exercises.SheetList():
                        if not sheet.IsClosed():
                            continue
                        if not sheet.counts:
                            continue
                        if sheetnrlist <> [] and sheetNumber not in sheetnrlist:
                            continue
                        returned = 0
                        if 'totalscore' in self.__field or \
                          'totalhomescore' in self.__field:
                            if p.homework.has_key(sheetName):
                                if p.homework[sheetName].totalscore != -1:
                                    scoreDict[k] += \
                                      p.homework[sheetName].totalscore
                                    returned = 1
                        if 'totalscore' in self.__field or \
                          'totalmcscore' in self.__field:
                            if p.mcresults.has_key(sheetName):
                                scoreDict[k] += \
                                  p.mcresults[sheetName].score
                                returned = 1
                        returnDict[k] += returned
        for k in scoreDict.keys():
            if returnDict[k] < self.__fracreturned * maxReturns:
                del scoreDict[k]
        if len(scoreDict) != 0:
            if self.__showmax and maxScore <> -1:
                s += '<p>%s: %d</p>\n' % (self.__titles[0], maxScore)
            s += '<table class="detailedscoretable">\n'
            s += '<thead>\n'
            if self.__showmax and maxScore > 0:
                s += ('<tr class="head"><th colspan="2">%s</th>' + \
                  '<th colspan="2">%s</th>' + \
                  '<th colspan="2">%s</th></tr>\n') % (self.__titles[1], \
                  self.__titles[2], self.__titles[3])
            else:
                s += ('<tr class="head"><th>%s</th>' + \
                  '<th colspan="2">%s</th>' + \
                  '<th colspan="2">%s</th></tr>\n') % (self.__titles[1], \
                  self.__titles[2], self.__titles[3])
            s += '</thead>\n'
            s += '<tbody>\n'
            scores = {}
            for score in scoreDict.values():
                if scores.has_key(score):
                    scores[score] = scores[score] + 1
                else:
                    scores[score] = 1
            k = scores.keys()
            k.sort ()
            k.reverse ()
            row = 0
            sumoffreqs = 0
            for score in k:
                row += 1
                sumoffreqs += scores[score]
                if row % 2 == 0:
                    s += '<tr class="even">'
                else:
                    s += '<tr class="odd">'
                s += '<td>%s</td>' % locale.str(score)
                if self.__showmax and maxScore > 0:
                    s += '<td>(%s%%)</td>' % locale.format('%.2f', \
                      100.0 * score / maxScore)
                s += ('<td>%d</td><td>%s%%</td><td>%d</td><td>%s%%</td>' + \
                  '</tr>\n') % (scores[score], \
                  locale.format('%.2f', 100.0 * scores[score] / \
                  len(scoreDict)), sumoffreqs, \
                  locale.format('%.2f', 100.0 * sumoffreqs / \
                  len(scoreDict)))
            s += '</tbody>\n'
            s += '</table>\n'
            s += '<p />\n'
        return s

    def headAndBody (self):
        return ''

Plugins.register (PublicStatistics.__name__, '', 'Punktestatistik', \
  'Dieses Plugin dient der Erzeugung einer Statistik zu Übungs- und ' + \
  'Klausurpunkten', 'Marc Ensenbach', 'Marc Ensenbach', '2006', \
  PublicStatistics)
