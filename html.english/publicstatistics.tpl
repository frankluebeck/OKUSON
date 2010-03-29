<?xml version="1.0" encoding="ISO-8859-1"?>

<!-- Note that this file is only usable if you have activated the
     "publicstatistics" plugin in the server/plugins.sample directory. -->

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />
    <link href="/OKUSONStatistics.css" type="text/css" rel="StyleSheet" />

    <title>Punktestatistik</title>
  </head>

  <body>
    <Header />
    <h2>Punktestatistik</h2>

    <p>
      In this statistic only those participants are considered, for
      whom at least half of the exercise sheets have scores entered.
    </p>
    <p>
      Please note that it is conceivable that not all scores from the
      written exercises have already been entered.
    </p>

    <h3>Interactive Exercises</h3>
    <ExtensionCode name="PublicStatistics" field="totalmcscore" showmax="yes"
     titles="bisher zu erreichende Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="0.5" />
    
    <h3>Written Exercises</h3>
    <ExtensionCode name="PublicStatistics" field="totalhomescore" showmax="yes"
     titles="bisher zu erreichende Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="0.5" />
    
    <h3>Total Score</h3>
    <ExtensionCode name="PublicStatistics" field="totalscore" showmax="yes"
     titles="bisher zu erreichende Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="0.5" />
    
    <h3>First part of written examination</h3>
    <ExtensionCode name="PublicStatistics" field="examscore1" showmax="yes"
     titles="maximal m&ouml;gliche Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="1" />
    
    <h3>Second part of written examination</h3>
    <ExtensionCode name="PublicStatistics" field="examscore2" showmax="yes"
     titles="maximal m&ouml;gliche Punktzahl:Punkte:H&auml;ufigkeiten:kumuliert"
     fracreturned="1" />

    <h3>Total score in written examination</h3>
    <p>
      Only participants in both written examinations will appear in
      this statistic.
    </p>
    <ExtensionCode name="PublicStatistics" field="examscore" showmax="yes"
     titles="maximal possible score:score:multiplicities:cumulated"
     fracreturned="1" />
    
    <Footer />

    <p class="foot">
      <ValidatorIcon />
    </p>
  </body>
</html>

<!-- Copyright 2004 Marc Ensenbach -->
