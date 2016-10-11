<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Übungsblatt abrufen</title>
  </head>

  <body>
    <Header />
    <h1>Übungsblatt abrufen</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <IfIndividualSheets>
    <p>Bitte geben Sie Ihre Matrikelnummer und Ihr Passwort ein (mit dem
    Sie sich <a href="registration.html">angemeldet</a> haben).
    </p>
    </IfIndividualSheets>

<!--    <p>Auch wenn Sie nicht angemeldet sind, können Sie sich als Gast
    Beispielblätter ansehen. Benutzen Sie die Nummer <GuestId />
    mit beliebigem (auch leerem) Passwort.</p>
-->
    <form action="QuerySheet" method="post">

    <table>
    <IfIndividualSheets>
    <tr><td>Ihre Matrikelnummer: </td>
    <td><input class="short"  maxlength="6" name="id" value="" 
               tabindex="1"/></td></tr>
    <tr><td>Ihr Passwort: </td>
    <td><input type="password" class="short"
               maxlength="16" name="passwd" value="" tabindex="2" /> </td></tr>
    </IfIndividualSheets>
    <tr><td>Gewünschter Dokumenttyp 
            (<a href="doctypehelp.html">Hilfe</a>):</td>
    <td><select name="format" tabindex="10000">
    <IfIndividualSheets>
        <option selected="selected">HTML</option>
        <!--  Uncomment one of these lines for MathJax option:  -->
        <!-- <option selected="selected">HTML</option> -->
        <!-- <option>MathJax</option> -->
        <option>PDF</option>
    </IfIndividualSheets>
    <IfNoIndividualSheets>
        <option>HTML</option>
        <!--  Uncomment for MathJax option:  -->
        <!-- <option>MathJax</option> -->
        <option selected="selected">PDF</option>
    </IfNoIndividualSheets>
    </select></td></tr>
    <tr><td>Auflösung (HTML):</td>
    <td><select name="resolution" tabindex="10001">
        <AvailableResolutions />
    </select></td></tr>
    </table>

    <p>Die folgenden Übungsblätter sind verfügbar:</p>
    <p><AvailableSheetsAsButtons /></p>

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

