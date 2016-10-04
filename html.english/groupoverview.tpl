<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Distribution into exercise groups</title>
  </head>

  <body>
    <Header />
    <h1>Distribution into exercise groupsÜbungsgruppeneinteilung</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <h3>Overview over exercise groups:</h3>

    <p>
    Click on an entry to get further information about a group.
    </p>
    <table>

     <tr><th>Group number</th> 
         <th>Place</th>
         <th>Tutor</th>
         <th>Number of participants</th></tr>
     <!-- Customize with attribute 'components', default is
       components="number,place,tutor,nrparticipants"
       other possible components : time, emailtutor, maxsize, groupdata.xxx 
     <GroupsOverview components="number,place,tutor,nrparticipants"/>

     Use attribute 'nodisplay' to skip certain groups separated by commas. 
     For example the default group '0' can be left out with
     <GroupsOverview nodisplay='0'/>
    --> 
    <GroupsOverview/>

    </table>

    <hr />

    <h3>Distribution into exercise groups:</h3>
    <p>
    Look for your ID to find out in which exercise group you are.
    </p>
    <table>
      <tr><th>ID</th>
          <th>Group number</th></tr>

      <GroupDistribution />
 
    </table>
    <hr />

    <p><a href="index.html">Back to the main menu</a></p>

    <p class="foot">If there is any question please contact: <br />
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
     $Id: groupoverview.tpl,v 1.6 2005/04/04 10:07:29 luebeck Exp $ -->

