<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSONAdmin.css" type="text/css" rel="StyleSheet" />

    <title>Administrator-Login</title>
  </head>

  <body>
    <Header />
    <h1>Administrator-Login</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <h3><ServerStatus /></h3>

    <p>Bitte geben Sie das Administratorpasswort ein, um sich einzuloggen.
    Beachten Sie, dass der Einloggvorgang darin besteht, dass in Ihrem
    Browser ein Cookie gespeichert wird. Sie müssen also Cookies zulassen.
    Ansonsten bleibt Ihnen nichts übrig, als bei jedem einzelnen Schritt
    das Administratorpasswort einzugeben.</p>

    <form action="/AdminLogin" method="post">
     <p>Administratorpasswort:
     <input type="password" size="16" maxlength="16" name="passwd" value="" />
     <input type="submit" name="action" value="Login" />
    </p></form>
     
    <hr />

    <p><a href="/index.html">Zurück zur Startseite</a></p>

    <p class="foot">Bei Fragen wenden Sie sich bitte an: <br />
      <Feedback /> 
    </p>

    <p class="foot">
      <ValidatorIcon /> OKUSON-Version: <Version/>
    </p>
    <Footer />
  </body>
</html>

<!-- Copyright 2003 Frank Lübeck and Max Neunhöffer
     $Id: adminlogin.tpl,v 1.5 2004/10/05 09:04:20 neunhoef Exp $ -->

