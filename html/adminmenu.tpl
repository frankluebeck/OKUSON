<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSONAdmin.css" type="text/css" rel="StyleSheet" />

    <title>Administrator's Main Menu</title>
  </head>

  <body>
    <h1>Administrator's Main Menu</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <h3><OKUSONServerStatus /></h3>

    <form action="/AdminWork" method="post">
      <p><OKUSONLoginStatus /></p>

     <!--<p>
     Text:
     <input size="16" maxlength="16" name="Eingabe" value="" />
     <input type="submit" name="Hallo" value="Max" />
      </p>-->
     <p>Restart server: <input type="submit" name="Action" value="Restart" />
     </p>
     <p>Shutdown server: <input type="submit" name="Action" value="Shutdown" />
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
     $Id: adminmenu.tpl,v 1.1 2003/09/23 08:14:40 neunhoef Exp $ -->

