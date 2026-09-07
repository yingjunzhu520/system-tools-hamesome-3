\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hamesome-report}[2026/08/24 v1.0 Hamesome 自定义实验报告模板]

% ============ 基础文档类（内置中文支持） ============
% TeXPage 等国产在线平台【已预装中易字库】，本地 Windows 也自带该字库，
% 故统一使用 fontset=windows（SimSun/SimHei/FangSong/KaiTi），用 XeLaTeX 编译。
% 若改为在本地 Linux/macOS 编译且缺少中易字体，可把 windows 改成
% fandol / ubuntu / founder。
\LoadClass[UTF8, a4paper, 11pt, fontset=windows]{ctexart}

% ============ 页面边距 ============
\RequirePackage{geometry}
\geometry{left=2.5cm, right=2.5cm, top=2.6cm, bottom=2.6cm}

% ============ 颜色（个人主题蓝） ============
\RequirePackage{xcolor}
\definecolor{accent}{HTML}{2563EB}
\definecolor{subaccent}{HTML}{1E40AF}
\definecolor{codebg}{HTML}{F1F5F9}

% ============ 图片与浮动体 ============
\RequirePackage{graphicx}
\RequirePackage{float}

% ============ 页眉页脚 ============
\RequirePackage{fancyhdr}
\setlength{\headheight}{15pt}
\pagestyle{fancy}
\fancyhf{}
\lhead{\textcolor{accent}{\textbf{系统开发工具基础}}}
\rhead{实验报告}
\cfoot{\thepage}
\renewcommand{\headrule}{\color{accent}\hrule height 1pt}
\renewcommand{\footrule}{\color{accent!50}\hrule height 0.4pt}

% ============ 章节标题样式 ============
\RequirePackage{titlesec}
\titleformat{\section}{\Large\bfseries\color{accent}}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries\color{subaccent}}{\thesubsection}{1em}{}

% ============ 列表 ============
\RequirePackage{enumitem}
\setlist{itemsep=2pt, parsep=2pt}

% ============ 代码块 ============
\RequirePackage{listings}
\lstdefinestyle{mycode}{
  basicstyle=\ttfamily\small,
  backgroundcolor=\color{codebg},
  frame=single,
  rulecolor=\color{accent},
  breaklines=true,
  tabsize=2,
  numbers=left,
  numberstyle=\tiny\color{gray},
  captionpos=b,
}
\lstset{style=mycode}

% ============ 超链接 ============
\RequirePackage[hidelinks]{hyperref}

% ============ 学号命令 ============
% 用法：\stuid{24070030103}  或  \renewcommand{\stuidvalue}{24070030103}
\newcommand{\stuidvalue}{20260001}
\newcommand{\stuid}[1]{\renewcommand{\stuidvalue}{#1}}

% ============ 自定义标题区 ============
\renewcommand{\maketitle}{%
  \begin{center}
    \vspace*{0.2cm}
    {\color{accent}\rule{\linewidth}{2pt}}\\[0.3cm]
    {\LARGE\bfseries \@title}\\[0.2cm]
    {\color{accent}\rule{\linewidth}{2pt}}\\[0.4cm]
    {\large 课程：系统开发工具基础}\\[0.15cm]
    {\large 姓名：\@author \quad 学号：\stuidvalue}\\[0.15cm]
    {\large 提交日期：\@date}
  \end{center}
  \vspace{0.4cm}
}
\endinput
