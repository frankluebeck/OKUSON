<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width; initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Change of your data</title>
  </head>

  <body>
    <Header />
    <h1>Change of your data</h1>

    <h2>Course: <CourseName />, <Semester />, <Lecturer /></h2>

<p>We have stored the following data for statistical purposes. Here you can
make changes. If you want to change your password, then enter below
the old one once and the new one twice. Leave the two entries for the
new password empty to keep your old password.
</p>

<form action="SubmitRegChange" method="post">
  <table>
    <tr>
      <td> <strong>Important data:</strong> </td>
      <td></td>
    </tr>

    <tr>
      <td>ID:</td>
      <td> <HiddenIdField /> </td>
    </tr>

    <tr>
      <td>Password: <input type="password" size="16" maxlength="16" 
                           name="passwd" value="" /></td>
      <td> <input type="submit" name="Action" value="Abschicken" /> </td>
    </tr>

    <tr>
      <td>New password (<a href="hinwpasswd.html">NOTE</a>):</td>
      <td> <input type="password" size="16" maxlength="16" name="pw1"
        value="" />
      </td>
    </tr>

    <tr>
      <td>New password again:</td>
      <td> <input type="password" size="16" maxlength="16" name="pw2"
        value="" />
      </td>
    </tr>

    <tr>
      <td> <strong>Voluntary data:</strong> </td>
      <td></td>
    </tr>

    <tr>
      <td>Last name:</td>
      <td> <LastNameField /> </td>
    </tr>

    <tr>
      <td>First names:</td>
      <td> <FirstNameField /> </td>
    </tr>

    <tr>
      <td>Subject:</td>
      <td> <select name="stud">
             <PossibleStudies />
           </select>
        <TopicField />
        (if "Other:").
      </td>
    </tr>

    <tr>
      <td>Year of studies:</td>
      <td> <SemesterField /> </td>
    </tr>

    <!-- The following should be activated if you allow participants to
         change their tutoring group number (see <GroupChangePossible> in
         Config.xml . -->
    <!--
    <tr>
      <td>Übungsgruppennummer:</td>
      <td> <GroupField /> </td>
    </tr>
    -->

    <tr>
      <td>Email:</td>
      <td> <EmailField /> </td>
    </tr>

<!--
    <tr>
      <td>Einteilungswunsch:</td>
      <td> <WishesField /> </td>
    </tr>
-->

  </table>

<!--
  <p>Bitte geben Sie unter "Einteilungswunsch" die Matrikelnummern
  der Kommilitoninnen/Kommilitonen ein, mit denen Sie zusammen in eine
  Übungsgruppe eingeteilt werden möchten. Trennen Sie die Nummern
  durch Lücken oder Kommas.</p>
-->

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
     $Id: regchange2.tpl,v 1.7 2004/10/06 10:26:44 neunhoef Exp $ -->

