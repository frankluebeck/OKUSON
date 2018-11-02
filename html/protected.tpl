<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="OKUSON.css" type="text/css" rel="StyleSheet" />

    <title>Geschützte Dateien</title>
  </head>

  <body>
    <Header />
    <h1>Geschützte Dateien</h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <form action="ProtectedFile" method="post">

    <table>
    
    <tr><td>Ihre Matrikelnummer: </td>
    <td><input class="short" maxlength="6" name="id" 
               value="" tabindex="1" /></td></tr>
    <tr><td>Ihr Passwort: </td>
    <td><input name="passwd" value="" maxlength="16" 
               type="password" class="short" tabindex="2" /> </td></tr>

    </table>

<!-- examples

    <p>
    <input type="submit" name="file" value="skript.pdf" tabindex="998"/>
    Skript zur Vorlesung
    </p>
    <p>
    <input type="submit" name="file" value="secretinfo.html" tabindex="998"/>
    Info zur Vorlesung
    </p>
-->

    </form>

    <hr />

    <p><a href="index.html">Zurück zur Startseite</a></p>

    <p class="foot">Bei Fragen wenden Sie sich bitte an: <br />
      <Feedback /> 
    </p>

    <p class="foot">
      <ValidatorIcon /> <a href="http://www.math.rwth-aachen.de/~OKUSON/">
      (OKUSON <Version/>)</a>
    </p>
    <Footer />
  </body>
</html>

<!-- Copyright 2018 Frank Lübeck -->

