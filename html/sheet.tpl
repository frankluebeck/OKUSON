<?xml version="1.0" encoding="ISO-8859-1"?>

<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="shortcut icon" href="favicon.ico" />
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta http-equiv="Expires" content="now" />
    <meta http-equiv="Cache-Control" content="no-cache" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <IfMathJax>
      <script type="text/javascript"
              src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
      </script>
    </IfMathJax>

    <link href="OKUSONSheet.css" type="text/css" rel="StyleSheet" />

    <title>Übungsblatt <SheetName /></title>
  </head>
  <body>

<IfMathJax> <!--  put here some macro definitions you want to use in
                  formulae in exercises -->
<p class="hidden">
\(
\def\Z{\mathbb{Z}}
\def\N{\mathbb{N}}
\def\Q{\mathbb{Q}}
\def\R{\mathbb{R}}
\def\C{\mathbb{C}}
\def\F{\mathbb{F}}
\)
</p>
</IfMathJax>

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

    <form action="SubmitSheet" method="post" class="sheet">
     <IfIndividualSheets>
     <div>
     <HiddenIdOfPerson />
     <HiddenNameOfSheet />
     </div>
     </IfIndividualSheets>
     
     <IfHTML>
       <WebSheetTable />
     </IfHTML>
     <IfMathJax>
       <WebSheetTableMathJax />
     </IfMathJax>
     <IfIndividualSheets>
     <IfOpen>
      <p>Passwort:
         <!-- To avoid autocompletion in the last excercise text field-->
         <input type="text" style="display: none;" name="fakename" autocomplete="username" />
         <input type="password" class="short" maxlength="16" name="passwd" autocomplete="current-password" />
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
      -->

