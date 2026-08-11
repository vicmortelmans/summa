\ProvidesClass{summa}[2025/08/26 Summa Theologica class for the Summa Theologica]
\LoadClass[12pt]{book}

% =======================
% Required packages
% =======================
\RequirePackage[paperwidth=156mm, paperheight=234mm,
                inner=25mm, outer=20mm,
                top=25mm, bottom=25mm]{geometry}
\RequirePackage{graphicx}   % for \scalebox
\RequirePackage{enumitem}   % custom lists
\RequirePackage{titlesec}   % custom section/chapter formats
\RequirePackage{xcolor}     % colors
\RequirePackage{ebgaramond} % main font
\RequirePackage[none]{hyphenat} % disable hyphenation
\RequirePackage{fancyhdr}   % headers/footers

\sloppy % spacing fallback when no hyphenation
\emergencystretch=0.3em

% =======================
% Page style setup
% =======================
\pagestyle{fancy}
\fancyhf{}
\makeatletter
\let\ps@plain\ps@fancy
\makeatother

% EVEN pages
\fancyfoot[LE]{\thepage}
\fancyfoot[RE]{%
  \ifnum\value{chapter}=0
  \else
    \thechapter-\thesection
  \fi
}
% ODD pages
\fancyfoot[LO]{%
  \ifnum\value{chapter}=0
  \else
    \thechapter-\thesection
  \fi
}
\fancyfoot[RO]{\thepage}

% =======================
% Custom commands
% =======================

\newcommand{\summaheading}[1]{%
  \subsection*{\textbf{\textcolor[HTML]{FB2C36}{\normalsize #1}}}%
}

\newenvironment{summaenumerate}
  {%
    \footnotesize
    \normalsize
    \begin{enumerate}[
      label={\scalebox{2.0}[2.0]{\arabic*}\hspace{0.5em}},
      labelsep=0pt,
      leftmargin=0pt,
      rightmargin=0pt,
      labelwidth=0pt,
      align=left
    ]%
  }
  {%
    \end{enumerate}%
  }

\newenvironment{quaestio}[2]
  {%
    \titleformat{\chapter}[display]%
                {\bfseries\centering}%
                {QUAESTIO \Roman{chapter}}%
                {0pt}%
                {\normalfont}%
    \chapter[Quaestio \Roman{chapter}: #1]%
            {OVER DE GEWIJDE LEER: #2}%
  }
  {} % nothing special to close

\newenvironment{articulus}[1]
  {%
    \titleformat{\section}[display]
      {\normalfont\centering}
      {ARTICULUS \Roman{section}}
      {0pt}
      {\normalfont}%
    \section[#1]{\itshape #1}%
  }
  {}

% Objectiones environment
\newenvironment{objectiones}
  {%
    \summaheading{Objectiones}%
    \begin{summaenumerate}%
  }
  {%
    \end{summaenumerate}%
  }

% Responsiones environment
\newenvironment{responsiones}
  {%
    \summaheading{Responsiones ad Objectiones}%
    \begin{summaenumerate}%
  }
  {%
    \end{summaenumerate}%
  }

\newenvironment{contra}
  {\summaheading{Sed contra}}
  {}

\newenvironment{respondeo}
  {\summaheading{Respondeo dicendum quod}}
  {}

% =======================
% Section spacing option
% =======================

\titlespacing*{\section}{0pt}{30pt}{30pt}
