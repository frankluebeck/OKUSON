<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Anmeldung zu den Übungen</title>
  </head>

  <body>
    <Header />
    <h1>Anmeldung zu den Übungen</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

<p>Die folgenden Daten werden nur zur Verwaltung des Übungsbetriebes und
zu statistischen Zwecken benutzt. Für den Abruf von Übungsblättern und
Ergebnissen brauchen Sie jeweils nur Ihre Matrikelnummer (ID) und Ihr Passwort.
</p>

<form action="SubmitRegistration" method="post">
  <table class="regdata">
    <tr>
      <td> <strong>Notwendige Angaben:</strong> </td>
      <td></td>
    </tr>

    <tr>
      <td>Matrikelnummer:</td>
      <td> <input class="short" maxlength="6" name="id" value="" /> </td>
    </tr>

    <tr>
      <td>Nachname:</td>
      <td> <input class="short" maxlength="30" name="lname" value="" /> </td>
    </tr>

    <tr>
      <td>Vorname:</td>
      <td> <input class="short" maxlength="30" name="fname" value="" /> </td>
    </tr>

    <tr>
      <td>Studiengang:</td>
      <td> <select name="stud">
             <PossibleStudies />
           </select>
        <input class="short" maxlength="30" name="topic" value="" />
        (falls "Sonstiges:").
      </td>
    </tr>

    <tr>
      <td>Fachsemester:</td>
      <td> <input class="digits" maxlength="2" name="sem" value="" /> </td>
    </tr>

    <tr>
      <td>Passwort (<a href="hinwpasswd.html">HINWEIS</a>):</td>
      <td> <input type="password" class="short" maxlength="16" name="passwd"
        value="" />
      </td>
    </tr>

    <tr>
      <td>Passwort nochmal:</td>
      <td>
        <input type="password" class="short" maxlength="16" name="passwd2"
        value="" />
      </td>
    </tr>

    <!-- The following should be activated if you allow participants to
         choose their tutoring group number (see <GroupChoicePossible> in
         Config.xml . -->
    <!--
    <tr>
      <td>Übungsgruppennummer:</td>
      <td> <input class="digits" maxlength="3" name="groupnr" value="" /> </td>
    </tr>
    -->

    <tr>
      <td> <strong>Freiwillige Angaben:</strong> </td>
      <td></td>
    </tr>

    <tr>
      <td>Email:</td>
      <td> <input class="long" maxlength="80" name="email" value="" /> </td>
    </tr>

    <tr>
      <td>Einteilungswunsch:</td>
      <td> <input class="long" maxlength="80" name="wishes" value="" /> </td>
    </tr>

    <tr>
      <td> </td>
      <td> <input type="submit" name="Action" value="Abschicken" /> </td>
    </tr>
  </table>

  <p>Bitte geben Sie unter "Einteilungswunsch" die Matrikelnummern
  der Kommilitoninnen/Kommilitonen ein, mit denen Sie zusammen in eine
  Übungsgruppe eingeteilt werden möchten. Trennen Sie die Nummern
  durch Lücken oder Kommas.</p>
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
     $Id: registration.tpl,v 1.5 2004/10/06 10:26:44 neunhoef Exp $ -->

