<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />
    <link href="OKUSONStatistics.css" type="text/css" rel="StyleSheet" />

    <title>Punktestatistik</title>
  </head>

  <body>
    <Header />
    <h1>Punktestatistik</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p>
      In dieser Statistik sind nur diejenigen ber&uuml;cksichtigt, bei denen
      f&uuml;r mindestens die H&auml;lfte der bisher abzugebenden Bl&auml;tter
      Punkte eingetragen sind.
    </p>
    <p>
      Bitte beachten Sie, dass die Statistik der
      Punkte aus den schriftlichen Aufgaben wegen der
      unregelm&auml;&szlig;igen Erfassung dieser Daten nicht auf dem
      aktuellen Stand zu sein braucht.
    </p>

    <h3>Interaktive Aufgaben</h3>
    <ExtensionCode name="PublicStatistics" field="totalmcscore" showmax="yes"
     titles="bisher zu erreichende Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="0.5" />
    
    <h3>Schriftliche Aufgaben</h3>
    <ExtensionCode name="PublicStatistics" field="totalhomescore" showmax="yes"
     titles="bisher zu erreichende Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="0.5" />
    
    <h3>Gesamtpunktzahl</h3>
    <ExtensionCode name="PublicStatistics" field="totalscore" showmax="yes"
     titles="bisher zu erreichende Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="0.5" />
    
    <h3>Erster Teil der Scheinklausur</h3>
    <ExtensionCode name="PublicStatistics" field="examscore1" showmax="yes"
     titles="maximal m&ouml;gliche Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="1" />
    
    <h3>Zweiter Teil der Scheinklausur</h3>
    <ExtensionCode name="PublicStatistics" field="examscore2" showmax="yes"
     titles="maximal m&ouml;gliche Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="1" />

    <h3>Gesamtpunktzahl in der Scheinklausur</h3>
    <p>
      In dieser Statistik erscheinen nur diejenigen, die an beiden
      Klausurteilen teilgenommen haben.
    </p>
    <ExtensionCode name="PublicStatistics" field="examscore" showmax="yes"
     titles="maximal m&ouml;gliche Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="1" />

    <hr />

    <p><a href="index.html">Zurück zur Startseite</a></p>

    <p class="foot">Bei Fragen wenden Sie sich bitte an: <br />
      <Feedback /> 
    </p>

    <p class="foot">
      <ValidatorIcon /> <a href="http://www.math.rwth-aachen.de/~OKUSON/">
      (OKUSON <Version/>)</a>
    </p>
    <Footer />
  </body>
</html>

<!-- Copyright 2007 Marc Ensenbach -->
