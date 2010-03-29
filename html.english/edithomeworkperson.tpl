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

    <p><strong>Group:</strong> <GroupNumber /> &nbsp; &nbsp; &nbsp;
       <strong>Tutor:</strong> <GroupTutor /> &nbsp; &nbsp; &nbsp;
       <strong>ID:</strong> <IdOfPerson />&nbsp; &nbsp; &nbsp;
       <strong>Name:</strong> <FirstName/>  <LastName/>   </p>

    <form action="/SubmitHomeworkPerson" method="post">
    <div><HiddenNumberOfGroup /><HiddenIdOfPerson /></div>
    <table>
      <tr><th align="left">Sheet</th><th align="left">Score</th>
          <th align="left">Score in individual exercises</th></tr>

      <HomeworkPersonInput />

    </table>
    <p>Password: <input type="password" size="16" maxlength="12" 
                        name="passwd" value="" />
                 <input type="submit" name="action" value="Abschicken" /></p>
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
     $Id: edithomeworkperson.tpl,v 1.9 2004/10/12 01:47:10 neunhoef Exp $ -->

