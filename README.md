# MVP Lab Technical Report Template

LaTeX template for the technical reports and arXiv papers of MVP Lab. It is a single package, `mvplab.sty`, for the
standard `article` class. It is used by the arXiv version of
[SpatialArena](https://mvp-ai-lab.github.io/SpatialArena).

[`example.tex`](example.tex) shows every feature, and [`example.pdf`](example.pdf) is the compiled result.

## Features

- **Title page:** the MVP Lab logo with a gradient "MVP Lab", the title above a gradient rule, and the authors. The
  project leader (blue †) and the corresponding author (pink envelope) are marked.
- **Abstract box:** the abstract, then the date, the project page, the GitHub and Hugging Face links with their logos,
  the project leader, and the correspondence address.
- **Running header:** the title (or `\shorttitle`) and the logo on every page after the first.
- **Numbered citations:** sorted and compressed (`natbib` with `numbers,sort&compress`).
- **Colors:** citations and references to sections, figures, tables, and equations are pink; web links are blue.
  Headings and caption labels are blue. All colors come from the lab webpages (primary `#4361EE`, indigo `#3F37C9`,
  accent `#F72585`, ink `#1F2430`).
- **Fonts:** Latin Modern for the text; Inter for the title page, headings, captions, and header.
- **Boxes:** `mvpbox` (a rounded box, optionally with a title) and `mvpprompt` (small typewriter text, for prompts).
- **Appendix:** `\appendixpage` starts the appendix on a new page with its own heading and no running header.

## Usage

Copy `mvplab.sty` and the `template/` folder (the logos) next to your main `.tex` file:

```latex
\documentclass[10pt,letterpaper]{article}
\usepackage{mvplab}

\title{Your Title}
\shorttitle{Short Title for the Header}            % optional
\author{First~Author\projectlead \and Second~Author \and Last~Author\corresponding}
\affiliation{MVP Lab \& Imperial College London}
\mvpdate{\today}
\projecturl{https://mvp-ai-lab.github.io/your-project}    % each link line is optional
\githuburl{https://github.com/mvp-ai-lab/your-project}
\huggingfaceurl{https://huggingface.co/datasets/mvp-lab/your-dataset}
\projectleader{First Author}{first.author@example.com}
\correspondence{Last Author}{last.author@example.com}

\begin{document}
\begin{abstract}
...
\end{abstract}
\maketitle             % after the abstract: the abstract is typeset in the title box

\section{Introduction}
...
\bibliographystyle{plainnat}
\bibliography{refs}

\appendixpage
\appendix
\section{More Results}
...
\end{document}
```

Notes:

- **Several affiliations:** add `\affilmark{1}`, `\affilmark{2}`, … after the names and before each affiliation:
  `\affiliation{\affilmark{1}MVP Lab\qquad\affilmark{2}Another Institution}`.
- **Names:** write them with `~` so a line break never splits one.
- **hyperref and cleveref:** the package loads both at the end of the preamble. Use `\cref` and `\Cref` for
  references. Load your own packages as usual; if you load `hyperref` yourself, the package keeps your options and
  sets only the link colors.
- **Logo folder:** to keep the logos elsewhere, set the folder before `\begin{document}`, e.g.
  `\renewcommand{\mvpassetdir}{styles/template/}`.

## Compiling

Compile with **pdfLaTeX**; the gradient text uses pdfTeX primitives:

```sh
latexmk -pdf example.tex
# or: pdflatex example && bibtex example && pdflatex example && pdflatex example
```

Overleaf works with the default pdfLaTeX compiler. A full TeX Live installation has every package the template
needs. With a minimal installation, add them with `tlmgr install`:

```
inter fontaxes mweights lm titlesec tcolorbox environ pdfrender fontawesome5 fancyhdr
caption enumitem natbib cleveref xcolor pgf microtype geometry
```

## Files

| File | Content |
| --- | --- |
| `mvplab.sty` | the template |
| `template/mvplab_logo.png` | MVP Lab logo (title page, abstract box, running header) |
| `template/mvplab_wordmark.pdf` | "MVP Lab" in the gradient colors, as vector outlines (title page) |
| `template/huggingface_logo.pdf` | Hugging Face logo (data link) |
| `example.tex`, `example.bib` | example report |
| `example.pdf` | compiled example |
| `tools/` | sources of `mvplab_wordmark.pdf` (see `tools/wordmark.tex` to regenerate it) |

The gradient "MVP Lab" on the title page is a pre-made PDF rather than live text: the letter outlines are an
ordinary clipping path with the gradient drawn through them. Every PDF viewer renders this, including macOS Preview.
The template also keeps `\mvpgradienttext{...}`, which applies the gradient to any text. Apple's PDF viewers don't
support it and show a filled rectangle instead, so avoid it in documents that people may open on a Mac.
