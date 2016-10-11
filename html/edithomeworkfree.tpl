<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Eingabe von Hausaufgabenpunkten</title>
  </head>

  <body>
    <Header />
    <h1>Eingabe von Hausaufgabenpunkten</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <form action="SubmitHomeworkFree" method="post">
    <p>Blattnummer: <Sheet /></p>
    <table>
      <tr><th align="left">Matnr.</th><th align="left">Name</th>
          <th align="left">Punkte</th>
          <th align="left">Punkte in den Einzelaufgaben</th></tr>
      <FreeHomeworkInput rows="20" />
    </table>
      <p><HiddenStatus /></p>
      <IfDataValidated
       true="Bitte Daten durch erneutes Abschicken bestaetigen"
       false="Bitte Daten eingeben oder fehlerhafte Daten (mit rotem Stern versehen) korrigieren" />
      <IfDataConfirmed
       true="Die Daten wurden im System eingetragen"
       false="" />
      <p>
        <GroupNumberInputIfRequired title="Gruppennummer" />
        <PasswordInputIfRequired title="Password" />
        <SubmitButtonIfRequired title="Abschicken" />
      </p>
    </form>

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

