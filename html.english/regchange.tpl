<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Change of your data</title>
  </head>

  <body>
    <Header />
    <h1>Change of your data</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

<p>Please enter your ID and password to see and change the data we
have stored about you.</p>

<form action="QueryRegChange" method="post">
  <table>
    <tr>
      <td>ID:</td>
      <td> <input class="short" maxlength="12" name="id" value="" /> </td>
    </tr>

    <tr>
      <td>Password:</td>
      <td> <input type="password" class="short" maxlength="16" name="passwd"
        value="" />
      </td>
    </tr>

    <tr>
      <td> </td>
      <td> <input type="submit" name="Action" value="Submit" /> </td>
    </tr>
  </table>
</form>

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
     $Id: regchange.tpl,v 1.4 2004/10/06 10:26:44 neunhoef Exp $ -->

