<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Änderung von Daten</title>
  </head>

  <body>
    <Header />
    <h1>Änderung von Daten</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

<p>Geben Sie bitte Ihre Matrikelnummer und Ihr Passwort ein, um Ihre
von uns gespeicherten Daten abzurufen und zu ändern: </p> 

<form action="QueryRegChange" method="post">
  <table>
    <tr>
      <td>Matrikelnummer:</td>
      <td> <input size="8" maxlength="6" name="id" value="" /> </td>
    </tr>

    <tr>
      <td>Passwort:</td>
      <td> <input type="password" size="16" maxlength="16" name="passwd"
        value="" />
      </td>
    </tr>

    <tr>
      <td> </td>
      <td> <input type="submit" name="Action" value="Abschicken" /> </td>
    </tr>
  </table>
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
     $Id: regchange.tpl,v 1.4 2004/10/06 10:26:44 neunhoef Exp $ -->

