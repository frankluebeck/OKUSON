<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Eingabe von Hausaufgabenpunkten</title>
  </head>

  <body>
    <h1>Eingabe von Hausaufgabenpunkten</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p><strong>Gruppe:</strong> <GroupNumber /> &nbsp; &nbsp; &nbsp;
       <strong>Tutor:</strong> <GroupTutor /> &nbsp; &nbsp; &nbsp;
       <strong>Matrikelnummer:</strong> <IdOfPerson /></p>

    <form action="/SubmitHomeworkPerson" method="post">
    <div><HiddenIdOfPerson /></div>
    <table>
      <tr><th align="left">Übungsblatt</th><th align="left">Punkte</th></tr>

      <HomeworkPersonInput />

      <tr><td>Passwort:
              <input type="password" size="16" maxlength="12" 
                     name="passwd" value="" />
          </td>
          <td><input type="submit" name="action" value="Abschicken" /></td>
      </tr>
    </table>
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
     $Id: edithomeworkperson.tpl,v 1.1 2003/10/08 20:36:38 neunhoef Exp $ -->

