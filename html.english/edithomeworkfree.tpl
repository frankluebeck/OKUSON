<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Input of homework scores</title>
  </head>

  <body>
    <Header />
    <h1>Input of homework scores</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <form action="/SubmitHomeworkFree" method="post">
    <p>Sheet number: <Sheet /></p>
    <table>
      <tr><th align="left">ID</th><th align="left">Name</th>
          <th align="left">Score</th>
          <th align="left">Scores in individual exercises</th></tr>
      <FreeHomeworkInput rows="20" />
    </table>
      <p><HiddenStatus /></p>
      <IfDataValidated
       true="Please confirm data by submitting again."
       false="Please enter data or correct wrong entries (marked with 
a red star)." />
      <IfDataConfirmed
       true="The data has been accepted by the system."
       false="" />
      <p>
        <GroupNumberInputIfRequired title="Gruppennummer" />
        <PasswordInputIfRequired title="Password" />
        <SubmitButtonIfRequired title="Abschicken" />
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
     $Id: edithomeworkfree.tpl,v 1.1 2005/10/11 23:11:48 neunhoef Exp $ -->

