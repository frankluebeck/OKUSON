<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Anzeige der Ergebnisse</title>
  </head>

  <body>
    <Header />
    <h1>Anzeige der Ergebnisse</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p><strong>Teilnehmer:</strong> <FirstName/> <LastName/>
    (<IdOfPerson/>)</p>

    <IfIndividualSheets>
    <p>Sie haben auf den Übungsblättern, deren Abgabefrist
bereits abgelaufen ist, die folgenden Punktzahlen in den
Multiple-Choice-Aufgaben (MC) beziehungsweise in den schriftlichen
Aufgaben (S) erhalten (letztere, soweit diese uns mitgeteilt wurden,
sonst steht da ein `?`. <strong>ACHTUNG</strong>: Die Punkte für die
schriftlichen Aufgaben werden nicht regelmäßig erfasst, die wissen Sie
ja von den korrigierten Zetteln.):</p>
    </IfIndividualSheets>
    <IfNoIndividualSheets>
    <p>Sie haben für die abgelaufenen Übungsblätter die folgenden
    Punktzahlen erreicht (soweit diese bereits eingegeben wurden):</p>
    </IfNoIndividualSheets>

<IfIndividualSheets>
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
</IfIndividualSheets>
<IfNoIndividualSheets>
  <table>
    <tr><th>Übungsblatt</th>
        <th>Punktzahl</th></tr>
        <Results components="homework,withMaxHomeScore" />
  </table>
</IfNoIndividualSheets>
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

    <!-- To display the registration status of participants use something
         like: -->
    <!--
    <IfExamRegistered nr="0">Sie sind zur Klausur angemeldet.
    </IfExamRegistered>
    <IfNotExamRegistered nr="0">Sie sind nicht zur Klausur angemeldet.
    </IfNotExamRegistered>
    -->

    <Grade />

    <GeneralMessages />

    <PrivateMessages />

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

<!-- Copyright 2003 Frank Lübeck and Max Neunhöffer
      -->

