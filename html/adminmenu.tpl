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

    <p><LoginStatus /></p>

    <h3>Control of Server:</h3>

    <form action="/Restart" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Restart server </p></form>

    <form action="/Shutdown" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Shutdown server </p></form>

    <h3>Export of Data:</h3>

    <form action="/ExportPeopleForExerciseClasses" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Export people for exercise class distribution
      <select name="together">
        <option selected="selected">all together</option>
        <option>by Studiengang</option>
      </select> sorted by
      <select name="sortedby">
        <option selected="selected">ID</option>
        <option>name</option>
        <option>Studiengang</option>
        <option>semester</option>
        <option>length of wishlist</option>
        <option>group and ID</option>
        <option>group and name</option>
      </select>
    </p></form>

    <form action="/ExportPeople" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Export people, sorted by 
      <select name="sortedby">
        <option selected="selected">ID</option>
        <option>name</option>
        <option>Studiengang</option>
        <option>semester</option>
        <option>length of wishlist</option>
        <option>group and ID</option>
        <option>group and name</option>
      </select>
    </p></form>
         
    <h3>Special Access for Administrators:</h3>

    <form action="/DisplaySheets" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Display available and future sheets</p></form>
         
    <form action="/SendMessage" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Send message 
    <input size="60" maxlength="240" name="msgtext" value="" />
    to <input size="8" maxlength="6" name="msgid" value="" />
    </p></form>
     
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
     $Id: adminmenu.tpl,v 1.7 2003/10/06 21:36:03 neunhoef Exp $ -->

