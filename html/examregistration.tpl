<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Anmeldung zur Klausur</title>
  </head>

  <body>
    <h1>Anmeldung zur Klausur</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p>Auf dieser Seite können Sie sich für die Klausur am ??.??.????
       von ??:?? bis ??:?? Uhr im Hörsaal ??? an- bzw. abmelden. Geben Sie 
       dafür bitte Ihre Matrikelnummer und Ihr Passwort an.</p>
    
    <!--
    DO NOT FORGET TO SWITCH ON <ExamRegistrationPossible> in Config.xml!!!
    <form action="ExamRegistration" method="post">
     <p><input type="hidden" name="examnr" value="0" /> ***please edit***
       Matrikelnummer: <input size="8" maxlength="6" name="id" value="" />
       Passwort: 
       <input type="password" size="16" maxlength="16" name="passwd" value="" />
       <input type="radio" name="anoderab" value="an" checked="checked"/>
       anmelden &nbsp; | &nbsp;
       <input type="radio" name="anoderab" value="ab"/>
       abmelden &nbsp; | &nbsp;
       <input type="submit" name="action" value="Los" />
     </p>
    </form>
    -->
 
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
     $Id: examregistration.tpl,v 1.3 2004/03/04 13:52:24 neunhoef Exp $ -->

