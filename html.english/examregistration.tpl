<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Registration for exam</title>
  </head>

  <body>
    <Header />
    <h1>Registration for exam</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <p>Here you can register and deregister for the written exam on
    ??.??.???? from ??:?? to ??:?? in lecture theatre ???. Please enter
    your ID and password. </p>
    
    <!--
    DO NOT FORGET TO SWITCH ON <ExamRegistrationPossible> in Config.xml!!!
    -->
    <form action="ExamRegistration" method="post">
     <p><input type="hidden" name="examnr" value="0" /> ***please edit***
       ID: <input size="8" maxlength="6" name="id" value="" />
       Password: 
       <input type="password" size="16" maxlength="16" name="passwd" value="" />
       <input type="radio" name="anoderab" value="an" checked="checked"/>
       register &nbsp; | &nbsp;
       <input type="radio" name="anoderab" value="ab"/>
       deregister &nbsp; | &nbsp;
       <input type="submit" name="action" value="Los" />
     </p>
    </form>
 
    <hr />

    <p><a href="/index.html">Back to the main menu</a></p>

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
     $Id: examregistration.tpl,v 1.7 2005/10/12 15:44:46 luebeck Exp $ -->

