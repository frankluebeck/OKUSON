%% 
%% This is file a0poster.cls
%% 
%% 
%% Copyright (C) 02.03.98 Karsten Held
%%
%% Copyright (C) 07.05.97 Gerlinde Kettl and Matthias Weiser (Uni Regensburg)
%% 
%%
%% Problems, bugs and comments to 
%% karsten.held@physik.physik.uni-augsburg.de
%% 
\ProvidesClass{a0poster}[1997/05/07 v2.01b a0poster class (GK, MW)]
\NeedsTeXFormat{LaTeX2e}[1995/06/01]
\LoadClass{article}

\newif\ifportrait
\newif\ifanullb
\newif\ifanull
\newif\ifaeins
\newif\ifazwei
\newif\ifadrei
\newif\ifdraft

\newcount\xkoord
\newcount\ykoord
\newcount\xscale
\newcount\yscale

\DeclareOption{a0b}{
\anullbtrue
\xkoord=2594 % big points (1 bp=1/72 inch)
\ykoord=3370 % big points (1 bp=1/72 inch)
\xscale=2
\yscale=2
}
\DeclareOption{a0}{
\anulltrue\anullbfalse
\xkoord=2384 % big points (1 bp=1/72 inch)
\ykoord=3371 % big points (1 bp=1/72 inch)
\xscale=2
\yscale=2
}
\DeclareOption{a1}{
\aeinstrue\anullbfalse
\xkoord=1686 % big points (1 bp=1/72 inch)
\ykoord=2384 % big points (1 bp=1/72 inch)
\xscale=3
\yscale=3
}
\DeclareOption{a2}{
\azweitrue\anullbfalse
\xkoord=1192 % big points (1 bp=1/72 inch)
\ykoord=1686 % big points (1 bp=1/72 inch)
\xscale=4
\yscale=4

}
\DeclareOption{a3}{
\adreitrue\anullbfalse
\xkoord=843  % big points (1 bp=1/72 inch)
\ykoord=1192 % big points (1 bp=1/72 inch)
\xscale=6
\yscale=6
}
\DeclareOption{landscape}{
\portraitfalse
}
\DeclareOption{portrait}{
\portraittrue
}
\DeclareOption{draft}{
\drafttrue
}
\DeclareOption{final}{
\draftfalse
}
\DeclareOption*{\PackageWarning{a0poster}{Unknown Option \CurrentOption}}
\ExecuteOptions{landscape,a0,final}
\ProcessOptions\relax

\ifanullb
   \setlength{\paperwidth}{119cm}
   \setlength{\paperheight}{88cm}
   \setlength{\textwidth}{117cm}
   \setlength{\textheight}{86cm}
\else\ifanull
        \setlength{\paperwidth}{118.92cm}
        \setlength{\paperheight}{84.09cm}
        \setlength{\textwidth}{116.92cm}
        \setlength{\textheight}{82.09cm}
     \else\ifaeins
             \setlength{\paperwidth}{84.09cm}
             \setlength{\paperheight}{59.46cm}
             \setlength{\textwidth}{82.09cm}
             \setlength{\textheight}{57.46cm}
          \else\ifazwei
                  \setlength{\paperwidth}{59.46cm}
                  \setlength{\paperheight}{42.04cm}
                  \setlength{\textwidth}{57.46cm}
                  \setlength{\textheight}{40.04cm}
               \else\ifadrei
                       \setlength{\paperwidth}{42.04cm}
                       \setlength{\paperheight}{29.73cm}
                       \setlength{\textwidth}{40.04cm}
                       \setlength{\textheight}{27.73cm}
                    \else\relax
                    \fi
               \fi
          \fi
     \fi
\fi


\ifportrait
   \newdimen\tausch
   \setlength{\tausch}{\paperwidth}
   \setlength{\paperwidth}{\paperheight}
   \setlength{\paperheight}{\tausch}
   \setlength{\tausch}{\textwidth}
   \setlength{\textwidth}{\textheight}
   \setlength{\textheight}{\tausch}
\else\relax
\fi

%% Setting proper dimensions for a DIN A0 printer

\setlength{\headheight}{0 cm}
\setlength{\headsep}{0 cm}
\setlength{\topmargin}{-15.4 mm}  % -1in +1cm
\setlength{\oddsidemargin}{-15.4 mm} % -1in +1cm
\setlength{\topskip}{0 cm}
\setlength{\footskip}{0 cm}
\setlength{\parindent}{0 cm}

\catcode`\%=11
\newwrite\Ausgabe
\immediate\openout\Ausgabe=a0header.ps
\write\Ausgabe{%%BeginFeature *PageSize ISOA0/ISO A0}
\ifdraft\write\Ausgabe{2 dict dup /PageSize [595 842] put dup /ImagingBBox null put}
\else\write\Ausgabe{2 dict dup /PageSize [\number\xkoord\space \number\ykoord] put dup /ImagingBBox null put}\fi
\ifdraft\write\Ausgabe{38 84 translate}
\write\Ausgabe{0.\number\xscale\space 0.\number\yscale\space scale}\else\relax\fi
\write\Ausgabe{%%EndFeature}
\closeout\Ausgabe
\catcode`\%=14

\special{header=./a0header.ps}

\input{a0size.sty}

\renewcommand{\tiny}{\fontsize{12}{14}\selectfont}
\renewcommand{\scriptsize}{\fontsize{14.4}{18}\selectfont}   
\renewcommand{\footnotesize}{\fontsize{17.28}{22}\selectfont}
\renewcommand{\small}{\fontsize{20.74}{25}\selectfont}
\renewcommand{\normalsize}{\fontsize{24.88}{30}\selectfont}
\renewcommand{\large}{\fontsize{29.86}{37}\selectfont}
\renewcommand{\Large}{\fontsize{35.83}{45}\selectfont}
\renewcommand{\LARGE}{\fontsize{43}{54}\selectfont}
\renewcommand{\huge}{\fontsize{51.6}{64}\selectfont}
\renewcommand{\Huge}{\fontsize{61.92}{77}\selectfont}
\newcommand{\veryHuge}{\fontsize{74.3}{93}\selectfont}
\newcommand{\VeryHuge}{\fontsize{89.16}{112}\selectfont}
\newcommand{\VERYHuge}{\fontsize{107}{134}\selectfont}
\renewcommand{\section}{\@startsection {section}{1}{\z@}%
  {-3.5ex \@plus -1ex \@minus -.2ex}%
  {2.3ex \@plus.2ex}%
  {\reset@font\Large\bfseries\sffamily}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
  {-3.25ex\@plus -1ex \@minus -.2ex}%
  {1.5ex \@plus .2ex}%
  {\reset@font\large\bfseries\sffamily}}

\setlength\smallskipamount{6pt plus 2pt minus 2pt}
\setlength\medskipamount{12pt plus 4pt minus 4pt}
\setlength\bigskipamount{24pt plus 8pt minus 8pt}

\setlength\abovecaptionskip{25pt}
\setlength\belowcaptionskip{0pt}
\setlength\abovedisplayskip{25pt plus 6pt minus 15 pt}
\setlength\abovedisplayshortskip{0pt plus 6pt}
\setlength\belowdisplayshortskip{13pt plus 7pt minus 6pt}
\setlength\belowdisplayskip\abovedisplayskip

\normalsize


\AtBeginDocument{
\ifanullb
   \ifportrait\special{papersize=88.00cm,119cm}\else\special{papersize=119cm,88.00cm}\fi
\else\ifanull
        \ifportrait\special{papersize=84.09cm,118.92cm}\else\special{papersize=118.92cm,84.09cm}\fi
     \else\ifaeins
             \ifportrait\special{papersize=59.46cm,84.09cm}\else\special{papersize=84.09cm,59.46cm}\fi
          \else\ifazwei
                  \ifportrait\special{papersize=42.04cm,59.46cm}\else\special{papersize=59.46cm,42.04cm}\fi
               \else\ifadrei
                      \ifdraft
                       \ifportrait\special{papersize=29.73cm,42.04cm}\else\special{papersize=42.04cm,29.73cm}\fi
                      \else
                       \ifportrait\special{papersize=29.73cm,42.04cm}\else\special{papersize=42.04cm,29.73cm}\fi
                      \fi
                    \else\relax
                    \fi
               \fi
          \fi
     \fi
\fi
\pagestyle{empty}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%               Hintergrund                    %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\background}[3]{\newrgbcolor{cgradbegin}{#1}
  \newrgbcolor{cgradend}{#2} 
  \psframe[fillstyle=gradient,gradend=cgradend,
  gradbegin=cgradbegin,gradmidpoint=#3](0.,0.)(1.\textwidth,-1.\textheight)}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Header                        %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{header}[1][1. 1. 1.] {
    \vspace{2em}
    
    \begin{center}
    \newrgbcolor{hcolor}{#1}
    \begin{lrbox}{\dummybox} 
    \begin{minipage}[t]{.9\textwidth}
 }   
 {  \end{minipage} \end{lrbox}
      \raisebox{-\depth}{\hspace{.5in}\hspace{-4mm}
       \psshadowbox[fillstyle=solid,fillcolor=hcolor,framesep=8mm]
    {\usebox{\dummybox}}} \end{center}
     \vspace{2em}
 }


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Header no shadow              %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{headerns}[1][1. 1. 1.] {
    \vspace{2em}
    
    \begin{center}
    \newrgbcolor{hcolor}{#1}
    \begin{lrbox}{\dummybox} 
    \begin{minipage}[t]{.9\textwidth}
 }   
 {  \end{minipage} \end{lrbox}
      \raisebox{-\depth}{\hspace{.5in}\hspace{-4mm}
       \psshadowbox[fillstyle=solid,fillcolor=hcolor,framesep=8mm,shadowsize=0pt]
    {\usebox{\dummybox}}} \end{center}
     \vspace{2em}
 }



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Poster                        %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newsavebox{\dummybox}
\newsavebox{\spalten}

\newenvironment{poster} {
   \vfill \begin{minipage}{\textwidth}\hfill }
  {\hfill\end{minipage} \vfill}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                pcolumn                       %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\columnfrac}{.3}
\newenvironment{pcolumn}{%
%\hfill%
\begin{minipage}[t]{\columnfrac\textwidth}}{\end{minipage}\hfill%
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                pbox                          %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{pbox}[1][1. 1. 1.] {
   \newrgbcolor{bcolor}{#1}
  \begin{lrbox}{\dummybox}%
    \begin{minipage}{0.92\linewidth}}%
    {\end{minipage}
  \end{lrbox}
  \raisebox{-\depth}{%
\psshadowbox[fillstyle=solid,fillcolor=bcolor,framesep=1em]{\usebox{\dummybox}}%
}\vspace{2em}\vfill}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                pbox   no shadow              %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{pboxns}[1][1. 1. 1.] {
   \newrgbcolor{bcolor}{#1}
  \begin{lrbox}{\dummybox}%
    \begin{minipage}{0.92\linewidth}}%
    {\end{minipage}
  \end{lrbox}
  \raisebox{-\depth}{%
\psshadowbox[fillstyle=solid,fillcolor=bcolor,framesep=1em,shadowsize=0pt]{\usebox{\dummybox}}%
}\vspace{2em}\vfill}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%             prbox   round corners           %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{prbox}[1][1. 1. 1.] {
   \newrgbcolor{bcolor}{#1}
  \begin{lrbox}{\dummybox}%
    \begin{minipage}{0.92\linewidth}}%
    {\end{minipage}
  \end{lrbox}
  \raisebox{-\depth}{%
\psshadowbox[fillstyle=solid,fillcolor=bcolor,framesep=2em, framearc=.2]{\usebox{\dummybox}}}\vspace{2em} \vfill}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%             prbox   round corners           %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{prboxns}[1][1. 1. 1.] {
   \newrgbcolor{bcolor}{#1}
  \begin{lrbox}{\dummybox}%
    \begin{minipage}{0.92\linewidth}}%
    {\end{minipage}
  \end{lrbox}
  \raisebox{-\depth}{%
\psshadowbox[fillstyle=solid,fillcolor=bcolor,framesep=2em, framearc=.2, shadowsize=0pt]{\usebox{\dummybox}}}\vspace{2em}\vfill}

\endinput
%% 
%% End of file `a0poster.cls'.





