<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="/OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Display of results</title>
  </head>

  <body>
    <Header />
    <h1>Display of results</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

    <p><strong>Participant:</strong> <FirstName/> <LastName/>
    (<IdOfPerson/>)</p>

    <IfIndividualSheets>
    <p>You have the following scores in the exercise sheets which
       are past their due date:</p>
    </IfIndividualSheets>
    <IfNoIndividualSheets>
    <p>You have the following scores in the exercise sheets which
       are past their due date (if the data has already been entered
       by your tutor):
    </p>
    </IfNoIndividualSheets>

<IfIndividualSheets>
  <table>
<!-- Adjust header and <Results> attributes -->
    <tr><th>Sheet</th><th>Online exercises</th>
        <!--<th>Written exercises</th>--></tr>
<!-- Specify the components you want in attribute 'components', separated 
     by commas. The default is both types of exercises in this order:
       components="interactive,homework"                     -->
  <!--<Results components="interactive,withMaxMCScore,homework,withMaxHomeScore" />-->
  <Results components="interactive,withMaxMCScore" />
  <!-- Alternatively, one could use the following if one does not want to 
         show the maximal scores:
  <Results components="interactive,homework" /> 
  -->
  </table>
</IfIndividualSheets>
<IfNoIndividualSheets>
  <table>
    <tr><th>Sheet</th>
        <th>Score</th></tr>
        <Results components="homework,withMaxHomeScore" />
  </table>
</IfNoIndividualSheets>
    <p><br /></p>

    <!-- Additionally, one can use:
    <p>Sie haben im Moment insgesamt <TotalMCScore /> von <MaxTotalMCScore /> 
       Punkten in den Multi-Choice-Aufgaben und <TotalHomeScore /> von 
       <MaxTotalHomeScore /> Punkten in den schriftlichen Hausaufgaben 
       erreicht.
    </p>
    -->
    <p>Currently you have altogether <TotalScore /> <!-- Punkte -->
       of <MaxTotalScore /> points.  <!-- comment this out if you do not
                                          want to show maximal scores. -->
    </p>

    <ExamGrades />
    <!-- Alternatively, one could use: 
    <ExamGrade nr="0" /> 
         for only exam number 0 -->

    <!-- To display the registration status of participants use something
         like: -->
    <!--
    <IfExamRegistered nr="0">Sie sind zur Klausur angemeldet.
    </IfExamRegistered>
    <IfNotExamRegistered nr="0">Sie sind nicht zur Klausur angemeldet.
    </IfNotExamRegistered>
    -->

    <Grade />

    <GeneralMessages />

    <PrivateMessages />

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
     $Id: results.tpl,v 1.13 2004/10/06 10:26:44 neunhoef Exp $ -->

