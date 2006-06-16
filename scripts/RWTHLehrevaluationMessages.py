#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
#   Copyright (C) 2005 by  Frank Lübeck  and   Max Neunhöffer
#
#   $Id: RWTHLehrevaluationMessages.py,v 1.3 2006/06/16 14:31:34 luebeck Exp $
#
# This script is part of OKUSON.
#

import sys, os, string
sys.path = [os.path.join(sys.path[0], '../server')] + sys.path
from fmTools import Utils, AsciiData

if len(sys.argv) < 4:
    print r"""
Erzeugung von 'messages' zur Online-Abgabe der Lehrevaluationsfragebögen
========================================================================
                 (Stand WS 04/05)

Usage:
     RWTHLehrevaluationMessages.py id_file tan_url_file message_text

wobei die Argumente folgende Dateien sind:
  id_file        Liste der Matrikelnummern (IDs), kann etwa über die OKUSON
                 Administratorseite via 'custom export' mit Format '%i' 
                 erhalten werden
  tan_url_file   jede Zeile ist die URL zu einem Fragebogen zur
                 Veranstaltung; die (einmalige) Zugangsberechtigung und 
                 die zugehörige Veranstaltung sind in einer im Evasys System
                 generierten TAN kodiert;  siehe unten, wie die aus einer
                 PDF-Datei mit freigeschalteten TANs generiert werden kann
  message_text   den 'message' Text, den die Teilnehmenden auf Ihrer 
                 Ergebnisabfrageseite finden sollen, darin ist die TAN
                 abhängige URL durch ein '%s' als Platzhalter ersetzt

Angenommen, vom Evasys System wird eine PDF-Datei mit TAN-Nummern zum
Ausdrucken, Ausschneiden und Verteilen geschickt, diese heiße 'TAN.pdf'.
Dann kann mit folgender langer Zeile 

   pdftotext TAN.pdf - | sed -e "s/Ihre TAN/\nIhre TAN/g" | grep "^Ihre TAN" | cut -d : -f 2 | sed -e "s/ //g" | sed -e "s/^/http:\/\/www.campus.rwth-aachen.de\/evasys\/indexstud.php?typ=html\&amp;user_tan=/" > TAN_URLs

[ EINSCHUB
 Die obige Zeile muss jedes Semester angepasst werden, man schaue dazu in den
 Output von "pdftotext TAN.pdf -". Im SS06 etwa muss es so geändert werden:

    pdftotext TAN.pdf - | grep -v ^Your | grep -v ^http | grep -v Surve | grep -v Diese | grep -v PSWD | grep -v '^$' | grep -v '^L'  | sed -e "s/^/http:\/\/www.campus.rwth-aachen.de\/evasys\/indexstud.php?typ=html\&amp;user_tan=/" > TAN_URLs
]

eine Datei 'TAN_URLs' erzeugt werden, die oben als Argument 'tan_url_file'
benutzt werden kann. (Beachte das '&amp;' in der URL, damit bei der
Verwendung in einem Link valides HTML entsteht.)

Hier ist noch eine Beispieldatei, die als 'message_text' verwendet werden
kann:

---- message_text  Beispiel ----------------------------------
<b style="color: red;">Achtung Lehrevaluation:</b> Bitte nehmen Sie an der Lehrevaluation zu dieser
Vorlesung/Übung teil! Hierzu klicken Sie auf diesen
<a href="%s"><em>Link zur Einmaligen Abgabe Ihrer Bewertung</em></a>.
<br />
Ihre Daten werden anonym an das 'Evasys' System geschickt. Jeder bekommt nur
eine, einmalig nutzbare Zugangsnummer pro Veranstaltung. Wir bekommen nur
eine statistische Gesamtauswertung und die anonyme Liste Ihrer Kommentare.
--------------------------------------------------------------

"""
    sys.exit(0)

# id's
f = file(sys.argv[1],"r")
ids = f.read()
f.close()
ids = ids.split('\n')
ids = filter(lambda a: len(a) > 0 and a[0] <> '#', ids)

# TAN URLs
f = file(sys.argv[2],"r")
tanurls = f.read()
f.close()
tanurls = tanurls.split('\n')

if len(tanurls) < len(ids):
  print "Not enough TANs: "+str(len(ids))+" participants and only "+str(len(
        tanurls))+" TANs.\n"
  sys.exit(2)
  
# message template
f = file(sys.argv[3],"r")
message = f.read()
f.close()

for i in xrange(len(ids)):
  print AsciiData.LineTuple((ids[i], message % tanurls[i]))

sys.exit(0)

