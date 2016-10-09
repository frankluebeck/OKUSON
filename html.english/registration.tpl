<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width; initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Registration</title>
  </head>

  <body>
    <Header />
    <h1>Registration</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

<p>Most of the following data will not be used. You can enter arbitrary data.
The only things necessary is the ID and the password. 
For the ID you can choose any other string
containing only letters and digits. The length of your ID
must be between 3 and 12 letters. The ID is used to
generate a personal set of questions for you.
</p>

<form action="SubmitRegistration" method="post">
  <table>
    <tr>
      <td> <strong>Important data:</strong> </td>
      <td></td>
    </tr>

    <tr>
      <td>ID:</td>
      <td> <input size="12" maxlength="12" name="id" value="" /> </td>
    </tr>

    <tr>
      <td>Password (<a href="hinwpasswd.html">NOTE</a>):</td>
      <td> <input type="password" size="16" maxlength="16" name="passwd"
        value="" />
      </td>
    </tr>

    <tr>
      <td>Password again:</td>
      <td>
        <input type="password" size="16" maxlength="16" name="passwd2"
        value="" />
      </td>
    </tr>

    <tr>
      <td> <strong>Voluntary data:</strong> </td>
      <td></td>
    </tr>

    <tr>
      <td>Last name:</td>
      <td> <input size="30" maxlength="30" name="lname" value="" /> </td>
    </tr>

    <tr>
      <td>First names:</td>
      <td> <input size="30" maxlength="30" name="fname" value="" /> </td>
    </tr>

    <tr>
      <td>Subject:</td>
      <td> <select name="stud">
             <PossibleStudies />
           </select>
        <input size="18" maxlength="30" name="topic" value="" />
        (if "Other:").
      </td>
    </tr>

    <tr>
      <td>Year of studies:</td>
      <td> <input size="2" maxlength="2" name="sem" value="" /> </td>
    </tr>

    <!-- The following should be activated if you allow participants to
         choose their tutoring group number (see <GroupChoicePossible> in
         Config.xml . -->
    <!--
    <tr>
      <td>Übungsgruppennummer:</td>
      <td> <input size="3" maxlength="3" name="groupnr" value="" /> </td>
    </tr>
    -->

    <tr>
      <td>Email:</td>
      <td> <input size="30" maxlength="80" name="email" value="" /> </td>
    </tr>

<!--
    <tr>
      <td>Einteilungswunsch:</td>
      <td> <input size="30" maxlength="80" name="wishes" value="" /> </td>
    </tr>
-->

    <tr>
      <td> </td>
      <td> <input type="submit" name="Action" value="Submit" /> </td>
    </tr>
  </table>

<!--
  <p>Bitte geben Sie unter "Einteilungswunsch" die Matrikelnummern
  der Kommilitoninnen/Kommilitonen ein, mit denen Sie zusammen in eine
  Übungsgruppe eingeteilt werden möchten. Trennen Sie die Nummern
  durch Lücken oder Kommas.</p>
-->

</form>

    <hr />

    <p><a href="index.html">Back to main menu</a></p>

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
     $Id: registration.tpl,v 1.5 2004/10/06 10:26:44 neunhoef Exp $ -->

