<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Tutor page</title>
  </head>

  <body>
    <Header />
    <h1>Tutor page</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <p>On this page you can change your password and query the pages
       for entering written homework results: </p>

    <form action="TutorRequest" method="post">
      <p>Group number:
         <input size="4" maxlength="2" name="group" value="" />
         Password:
         <input type="password" size="16" maxlength="16" name="passwd" 
                value="" /></p>
      <p>For password change: new password:
         <input type="password" size="16" maxlength="16" name="pw1" value="" />
         Again: 
         <input type="password" size="16" maxlength="16" name="pw2" value="" />
      </p>
      <p>Please get me input page for sheet number:
         <!--<input size="4" maxlength="2" name="sheet" value="" />-->
         <AvailableSheetsAsButtons />
      </p>
      <p><strong> or </strong></p>
      <p>Please get me input page for participant with ID:
         <input size="12" maxlength="12" name="id" value="" />
         <input type="submit" name="Action" value="Query" />
      </p>
    </form>
   
    <p><br /></p>
    <p><br /></p>

    <h3>Statistics for the results in your group:</h3>
    
    <form action="ShowGlobalStatistics" method="post">
    <p>
    Group number:
    <input  name="group" size="4" maxlength="4" />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input type="password" size="16" maxlength="16" name="passwd" 
                value="" />
    </p>
    <p><input type="submit" name="Action" value="Show" />
    </p>
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

