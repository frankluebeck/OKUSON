<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Übungsgruppeneinteilung</title>
  </head>

  <body>
    <Header />
    <h1>Übungsgruppeneinteilung</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <h3>Übersicht über die Übungsgruppen:</h3>

    <p>
    Klicken Sie auf einen Eintrag, um weitere Informationen zu dieser
    Gruppe zu bekommen.
    </p>
    <table>

     <tr><th>Gruppennummer</th> 
         <th>Hörsaal</th>
         <th>Tutor</th>
         <th>Teilnehmerzahl</th></tr>
     <!-- Customize with attribute 'components', default is
       components="number,place,tutor,nrparticipants"
       other possible components : time, emailtutor, maxsize, groupdata.xxx 
     <GroupsOverview components="number,place,tutor,nrparticipants"/>

     Use attribute 'nodisplay' to skip certain groups separated by commas. 
     For example the default group '0' can be left out with
     <GroupsOverview nodisplay='0'/>
    --> 
    <GroupsOverview/>

    </table>

    <hr />

    <h3>Gruppeneinteilung:</h3>
    <p>
    Suchen Sie Ihre Matrikelnummer, um die Nummer Ihrer Übungsgruppe zu
    erfahren.
    </p>
    <table>
      <tr><th>Matrikelnummer</th>
          <th>Gruppennummer</th></tr>

      <GroupDistribution />
 
    </table>
    <hr />

    <p><a href="/index.html">Zurück zur Startseite</a></p>

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
     $Id: groupoverview.tpl,v 1.6 2005/04/04 10:07:29 luebeck Exp $ -->

