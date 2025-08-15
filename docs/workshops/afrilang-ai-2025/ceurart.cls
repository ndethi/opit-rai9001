% CEUR-WS Article Format
% This is a simplified version for compilation purposes
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ceurart}[2025/01/01 CEUR-WS Article Format]

% Base class
\LoadClass[11pt,a4paper]{article}

% Required packages
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{url}
\RequirePackage{hyperref}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{fancyhdr}
\RequirePackage{geometry}

% Page geometry
\geometry{a4paper,margin=2.5cm}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\small AfriLang AI 2025 Proceedings}
\fancyfoot[C]{\thepage}

% Title and author commands
\newcommand{\copyrightyear}[1]{\def\@copyrightyear{#1}}
\newcommand{\copyrightclause}[1]{\def\@copyrightclause{#1}}
\newcommand{\conference}[1]{\def\@conference{#1}}
\newcommand{\cormark}[1]{}
\newcommand{\cortext}[2]{}

% Author command with options
\renewcommand{\author}[2][]{\def\@author{#2}}
\newcommand{\address}[2][]{\def\@address{#2}}

% Abstract environment
\renewenvironment{abstract}{%
  \small
  \begin{center}%
    \bfseries \abstractname\vspace{-.5em}\vspace{\z@}%
  \end{center}%
  \quotation
}{%
  \endquotation
}

% Keywords environment
\newenvironment{keywords}{%
  \small
  \vspace{1em}
  \noindent\textbf{Keywords:}\space
}{%
  \par
}

% Separator for keywords
\newcommand{\sep}{, }

% Acknowledgments environment
\newenvironment{acknowledgments}{%
  \section*{Acknowledgments}
}{%
}

% Maketitle customization
\renewcommand{\maketitle}{%
  \begin{center}
    {\LARGE\bfseries\@title\par}
    \vspace{1em}
    {\large\@author\par}
    \vspace{0.5em}
    {\@address\par}
    \vspace{1em}
  \end{center}
}

\endinput
