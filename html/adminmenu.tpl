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
    <Header />
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

    <form action="/ExportPeopleForGroups" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Export people for tutoring group distribution
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
         
    <form action="/ExportExamParticipants" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Export participants of exam number
    <input size="4" maxlength="2" name="examnr" value="" />
    sorted by
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

    <form action="/ExportResults" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Export results participants sorted by
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


    <h3>Statistics:</h3>

    <form action="/ShowExerciseStatistics" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Show Exercise Statistics for sheet
    <AvailableSheetsAsButtons />
    </p>
    </form>

    <form action="/ShowGlobalStatistics" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Show Global Statistics (for group
    <input  name="group" size="4" maxlength="4" />)
    </p>
    </form>

    <form action="/ShowGlobalStatisticsPerGroup" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Show Global Statistics, separated per Group, for sheet
    <AvailableSheetsAsButtons />
    </p>
    </form>

    <form action="/ShowCumulatedScoreStatistics" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Show Cumulated Score Statistics for
      <select name="exerciseCategory">
        <option selected="selected" value="all">MC and Homework</option>
        <option value="mc">MC only</option>
        <option value="homework">Homework only</option>
      </select>
    for group
    <input  name="group" size="4" maxlength="4" /> (leave field empty for all groups)<br />
    Who should be included in the cumulated statistics for a set of sheets?<br />
    <input type="radio" name="includeAll" value="no" checked="true" />
    Only people who returned the last sheet of the considered set of sheets.<br />
    <input type="radio" name="includeAll" value="yes" />
    All people who ever returned any sheet of the considered set of sheets.
    </p>
    </form>

    <form action="/ShowDetailedScoreTable" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Show Detailed Score Table for
      <select name="exerciseCategory">
        <option  value="all" selected="selected">MC and Homework</option>
        <option value="mc">MC only</option>
        <option value="homework">Homework only</option>
      </select>
    for group
    <input  name="group" size="4" maxlength="4" /> (leave field empty for all groups)
    sorted by  
      <select name="sortBy">
        <option value="ID" selected="selected">ID</option>
        <option value="name">name</option>
        <option value="total score">total score</option>
        <option value="total MC score">total MC score</option>
        <option value="total homework score">total homework score</option>
      </select>
    </p>
    </form>
    
    
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
     
    <form action="/DeleteMessages" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Delete messages of
    <input size="8" maxlength="6" name="msgid" value="" />
    </p></form>

    <form action="/Resubmit" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Reevaluate participants' answers for sheet
    <input size="6" maxlength="4" name="sheet" value="" />
    </p></form>

    <hr />

    <p><a href="/index.html">Zurück zur Startseite</a></p>

    <p class="foot">Bei Fragen wenden Sie sich bitte an: <br />
      <Feedback /> 
    </p>

    <p class="foot">
      <ValidatorIcon />
    </p>
    <Footer />
  </body>
</html>

<!-- Copyright 2003 Frank Lübeck and Max Neunhöffer
     $Id: adminmenu.tpl,v 1.19 2004/03/08 21:35:49 neunhoef Exp $ -->

