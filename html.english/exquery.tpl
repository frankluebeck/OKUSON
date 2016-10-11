<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Get exercise sheet</title>
  </head>

  <body>
    <Header />
    <h1>Get exercise sheet</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <IfIndividualSheets>
    <p>Please enter your ID and password (which you used to register
    <a href="registration.html">here</a>).
    </p>
    </IfIndividualSheets>

<!--    <p>Even though you have not yet registered, you can still download
    example sheets as guest. Please use the login <GuestId /> with an
    arbitrary (possibly empty) password.</p>
-->
    <form action="QuerySheet" method="post">

    <table>
    <IfIndividualSheets>
    <tr><td>Your ID: </td>
    <td><input class="short"  maxlength="12" name="id" value="" 
               tabindex="1"/></td></tr>
    <tr><td>Your password: </td>
    <td><input type="password" class="short"
               maxlength="16" name="passwd" value="" tabindex="2" /> </td></tr>
    </IfIndividualSheets>
    <tr><td>Document type:
            (<a href="doctypehelp.html">Help</a>):</td>
    <td><select name="format" tabindex="10000">
    <IfIndividualSheets>
        <option selected="selected">HTML</option>
        <!--  Uncomment one of these lines for MathJax option:  -->
        <!-- <option selected="selected">HTML</option> -->
        <!-- <option>MathJax</option> -->
        <option>PDF</option>
    </IfIndividualSheets>
    <IfNoIndividualSheets>
        <option>HTML</option>
        <!--  Uncomment for MathJax option:  -->
        <!-- <option>MathJax</option> -->
        <option selected="selected">PDF</option>
    </IfNoIndividualSheets>
    </select></td></tr>
    <tr><td>Resolution (HTML):</td>
    <td><select name="resolution" tabindex="10001">
        <AvailableResolutions />
    </select></td></tr>
    </table>

    <p>The following exercise sheets are available:</p>
    <p><AvailableSheetsAsButtons /></p>

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
      -->

