<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSONAdmin.css" type="text/css" rel="StyleSheet" />

    <title>Administrator Login</title>
  </head>

  <body>
    <Header />
    <h1>Administrator Login</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <h3><ServerStatus /></h3>

    <p>Please enter the administrator's password to log in. Please note
    that logging in amounts to storing a cookie in your browser. That
    is, you have to allow cookies in your browser. Otherwise you will
    have to enter the administrator's password in every single step.
    </p>

    <form action="/AdminLogin" method="post">
     <p>Administrator password:
     <input type="password" size="16" maxlength="16" name="passwd" value="" />
     <input type="submit" name="action" value="Login" />
    </p></form>
     
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
     $Id: adminlogin.tpl,v 1.6 2004/10/06 10:26:44 neunhoef Exp $ -->

