<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Tutoren-Seite</title>
  </head>

  <body>
    <h1>Tutoren-Seite</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p>Über diese Seite können Sie Ihr Passwort ändern und die Seiten
       zur Eingabe der Hausaufgaben-Ergebnisse abrufen:</p>

    <form action="/TutorRequest" method="post">
      <p>Gruppennummer:
         <input size="4" maxlength="2" name="group" value="" />
         Passwort:
         <input type="password" size="16" maxlength="16" name="passwd" 
                value="" /></p>
      <p>Für Passwort-Wechsel: neues Passwort:
         <input type="password" size="16" maxlength="16" name="pw1" value="" />
         Wiederholung: 
         <input type="password" size="16" maxlength="16" name="pw2" value="" />
      </p>
      <p>Bitte Eingabeseite für Blatt Nummer:
         <!--<input size="4" maxlength="2" name="sheet" value="" />-->
         <AvailableSheetsAsButtons />
      </p>
      <p><strong> oder </strong></p>
      <p>Bitte Eingabeseite für Teilnehmer mit Matrikelnummer:
         <input size="8" maxlength="6" name="id" value="" />
         <input type="submit" name="Action" value="Los" />
      </p>
    </form>
               
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
     $Id: tutors.tpl,v 1.2 2003/10/28 16:18:09 neunhoef Exp $ -->

