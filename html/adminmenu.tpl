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

    <form action="/AdminWork" method="post">
      <p><OKUSONLoginStatus /></p>

      <table>
       <tr><th align="left">Control of Server:</th><th></th></tr>
       <tr><td>Restart server:</td>
           <td><input type="submit" name="Action" value="Restart" /></td></tr>
       <tr><td>Shutdown server:</td>
           <td><input type="submit" name="Action" value="Shutdown" /></td></tr>
       <tr><th align="left">Export of Data:</th><th></th></tr>
       <tr><td>Export people for exercise classes distribution:
                 <select name="exportexclass">
                   <option selected="selected">all together</option>
                   <option>by Studiengang</option>
                 </select></td>
           <td><input type="submit" name="Action" 
                      value="Export people for exercise classes" /></td></tr>
       <tr><td>Export people:</td>
           <td><input type="submit" name="Action" value="Export people" /></td>
           </tr>
       <tr><th align="left">
           Special Access for Administrators:</th><th></th></tr>
       <tr><td>Display available and future sheets:</td>
           <td><input type="submit" name="Action" value="Display Sheets" /></td>
           </tr>
       <tr><td>Send message to
               <input size="8" maxlength="6" name="msgid" value="" /></td>
           <td><input type="submit" name="Action" value="Send message" /></td>
           </tr>
       <tr><td colspan="2">
           <input size="80" maxlength="240" name="msgtext" value="" /></td>
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
     $Id: adminmenu.tpl,v 1.6 2003/10/05 22:48:32 neunhoef Exp $ -->

