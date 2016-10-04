<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />

    <link href="OKUSONSheet.css" type="text/css" rel="StyleSheet" />

    <title>Übungsblatt <SheetName /></title>
  </head>

  <body>
    <Header />
    <h1>Übungsblatt <SheetName /></h1>

    <h2>Vorlesung: <CourseName />, <Semester />, <Lecturer /></h2>

    <IfIndividualSheets>
    <p>Für Matrikelnummer: <IdOfPerson /></p>
    </IfIndividualSheets>

    <p>Abgabe bis: <OpenTo /></p>

    <IfIndividualSheets>
    <p>Diese Seite wurde erstellt: <CurrentTime /></p>

    <p>
     <IfClosed><strong>Abgabefrist ist bereits abgelaufen</strong></IfClosed>
     <IfOpen>Die Abgabefrist ist noch nicht abgelaufen.</IfOpen>
    </p>
    </IfIndividualSheets>

    <form action="SubmitSheet" method="post">
     <IfIndividualSheets>
     <div>
     <HiddenIdOfPerson />
     <HiddenNameOfSheet />
     </div>
     </IfIndividualSheets>
     
     <WebSheetTable />
     
     <IfIndividualSheets>
     <IfOpen>
      <p>Passwort:
         <input type="password" size="16" maxlength="16" name="passwd"
                value="" />
         <input type="submit" value="Abgeben" name="action" />
      </p>
     </IfOpen>
     <IfClosed>
      <p><strong>Abgabefrist ist bereits abgelaufen!</strong></p>
     </IfClosed>
     </IfIndividualSheets>
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

<!-- Copyright 2003 Frank Lübeck and Max Neunhöffer
     $Id: sheet.tpl,v 1.6 2004/10/06 10:26:44 neunhoef Exp $ -->

