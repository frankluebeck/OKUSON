<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Anzeige der Ergebnisse</title>
  </head>

  <body>
    <h1>Anzeige der Ergebnisse</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p><strong>Teilnehmer:</strong> <FirstName/> <LastName/>
    (<IdOfPerson/>)</p>

    <p>Sie haben auf den Übungsblättern, deren Abgabefrist
bereits abgelaufen ist, die folgenden Punktzahlen in den
Multiple-Choice-Aufgaben (MC) beziehungsweise in den schriftlichen
Aufgaben (S) erhalten (letztere, soweit diese uns mitgeteilt wurden,
sonst steht da ein `?`. <strong>ACHTUNG</strong>: Die Punkte für die
schriftlichen Aufgaben werden nicht regelmäßig erfasst, die wissen Sie
ja von den korrigierten Zetteln.):</p>

  <table>
<!-- Adjust header and <Results> attributes -->
    <tr><th>Übungsblatt</th><th>Interaktive Aufgaben</th>
        <th>Schriftliche Aufgaben</th></tr>
<!-- Specify the components you want in attribute 'components', separated 
     by commas. The default is both types of exercises in this order:
       components="interactive,homework"                     -->
  <Results components="interactive,withMaxMCScore,homework,withMaxHomeScore" />
  <!-- Alternatively, one could use the following if one does not want to 
         show the maximal scores:
  <Results components="interactive,homework" /> 
  -->
  </table>

    <p><br /></p>

    <!-- Additionally, one can use:
    <p>Sie haben im Moment insgesamt <TotalMCScore /> von <MaxTotalMCScore /> 
       Punkten in den Multi-Choice-Aufgaben und <TotalHomeScore /> von 
       <MaxTotalHomeScore /> Punkten in den schriftlichen Hausaufgaben 
       erreicht.
    </p>
    -->
    <p>Sie haben im Moment insgesamt <TotalScore /> <!-- Punkte -->
       von <MaxTotalScore /> Punkten.  <!-- comment this out if you do not
                                            want to show maximal scores. -->
    </p>

    <ExamGrades />
    <!-- Alternatively, one could use: 
    <ExamGrade nr="0" /> 
         for only exam number 0 -->

    <Grade />

    <GeneralMessages />

    <PrivateMessages />

    <hr />

    <p><a href="/index.html">Zurück zur Startseite</a></p>

    <p class="foot">Bei Fragen wenden Sie sich bitte an: <br />
      <Feedback /> 
    </p>

    <p class="foot">
      <ValidatorIcon />
    </p>
  </body>
</html>

<!-- Copyright 2003 Frank Lübeck and Max Neunhöffer
     $Id: results.tpl,v 1.8 2003/11/16 19:05:27 neunhoef Exp $ -->

