<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSONAdmin.css" type="text/css" rel="StyleSheet" />

    <title>Administrator's Main Menu</title>
  </head>

  <body>
    <Header />
    <h1>Administrator's Main Menu</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <p><LoginStatus /></p>

    <p>[<a href="#contr">Server Control</a>]&nbsp;[<a href="#acc">Special
    Access</a>]&nbsp;[<a href="#stat">Statistics</a>]&nbsp;[<a
    href="#exp">Data Export</a>]&nbsp;</p>
    
<hr />

    <h3>Control of Server:<a name="contr"></a></h3>

    <form action="Restart" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Restart server </p></form>

    <form action="Shutdown" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Shutdown server </p></form>

<hr />
    
    <h3>Special Access for Administrators:<a name="acc"></a></h3>

    <form action="DisplaySheets" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Display available and future sheets</p></form>
         
    <form action="SendMessage" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Send message 
    <input size="60" maxlength="240" name="msgtext" value="" />
    to <input size="8" maxlength="6" name="msgid" value="" />
    </p></form>
     
    <form action="DeleteMessages" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Delete messages of
    <input size="8" maxlength="6" name="msgid" value="" />
    </p></form>

    <form action="Resubmit" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Reevaluate participants' answers for sheet
    <input size="6" maxlength="4" name="sheet" value="" />
    </p></form>

    <form action="ChangeGroup" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Move participant
    <input size="8" maxlength="6" name="chgrpid" value="" />
    to group number
    <input size="4" maxlength="4" name="chgrpto" value="" />
    </p></form>
    
    <hr />

    <h3>Statistics:<a name="stat"></a></h3>

    <form action="ShowExerciseStatistics" method="post">
    <p><!--<input type="submit" name="Action" value="Go" />-->
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <AdminPasswdField />
    Show Exercise Statistics for sheet
    <AvailableSheetsAsButtons />
    </p>
    </form>

    <form action="ShowGlobalStatistics" method="post">
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
    Show Global Statistics (for group
    <input  name="group" size="4" maxlength="4" />)
    </p>
    </form>

    <form action="ShowGlobalStatisticsPerGroup" method="post">
    <p><!--<input type="submit" name="Action" value="Go" />-->
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <AdminPasswdField />
    Show Global Statistics, separated per Group, for sheet
    <AvailableSheetsAsButtons />
    </p>
    </form>

    <form action="ShowCumulatedScoreStatistics" method="post">
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
    <input type="radio" name="includeAll" value="no" checked="checked" />
    Only people who returned the last sheet of the considered set of sheets.<br />
    <input type="radio" name="includeAll" value="yes" />
    All people who ever returned any sheet of the considered set of sheets.
    </p>
    </form>

    <form action="ShowDetailedScoreTable" method="post">
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
    
<hr />

    <h3>Export of Data:<a name="exp"></a></h3>

    <form action="ExportCustom" method="post">
    <p>Use the following format options for a customized export file.</p>
    
    <ExportFormatOptions/>
    <p><input type="submit" name="Action" value="Go" /><AdminPasswdField />
        Format string: <input size="50" maxlength="100" name="expformat"
        value="%i:%n:%f:%s:%a:%g:%C:%H:%T" />
    </p>
    </form>

    <form action="ExportPeopleForGroups" method="post">
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

    <form action="ExportPeople" method="post">
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
         
    <form action="ExportExamParticipants" method="post">
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

    <form action="ExportResults" method="post">
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
     $Id$ -->

