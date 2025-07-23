import os

# Configuration
CELL_HEIGHT = "1.32cm"
CELL_WIDTH = "1.19cm"
CELL_INNER_PADDING = "2pt"
COLUMN_COUNT = 15 # Number of columns per row (adjust based on page width)
FONT_FAMILY = "phv" # Font family: e.g. cmr (Computer Modern), lmr (Latin Modern), ptm (Times), phv (Helvetica)
FONT_SIZE = 7
FONT_LINE_SPACING = 9
INPUT_FILE = "input_labels.txt"  # Input file with switch names (one per line)
OUTPUT_FILE = "output_labels.tex"

assert CELL_INNER_PADDING[-2:] in ['pt', 'cm'], f'Unexpected CELL_INNER_PADDING measurement unit. Value: {CELL_INNER_PADDING}'
_CELL_INNER_PADDING_DOUBLED_FLOAT = float(CELL_INNER_PADDING[:-2]) * 2
_CELL_INNER_PADDING_DOUBLED = str(_CELL_INNER_PADDING_DOUBLED_FLOAT if _CELL_INNER_PADDING_DOUBLED_FLOAT % 1 > 0 else int(_CELL_INNER_PADDING_DOUBLED_FLOAT)) + CELL_INNER_PADDING[-2:]

# Read switch names from file
def read_switch_names(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file {file_path} not found")
    
    nameDict = {}
    with open(file_path, mode='r') as f:
        for line in f:
            name = line.strip()
            if len(name) == 0:
                continue
            if name in nameDict:
                print(f'Skipping duplicate label: "{name}"')
                continue
            nameDict[name] = None

    with open('input_labels_sorted.log', mode='w') as sortedLogF:
        sortedNames = list(nameDict.keys())
        sortedNames.sort(reverse=False)
        sortedLogF.write('\n'.join(sortedNames))

    names = list(nameDict.keys())
    print(f'Found {len(names)} labels to generate')
    return names

# Generate LaTeX code
def generate_latex(names):
    # LaTeX preamble
    latex = r'''\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{a4paper, margin=1cm}
\usepackage{array}
\usepackage{lmodern}
\usepackage[table]{xcolor}
\usepackage{arydshln}

\definecolor{lightgray}{RGB}{140,140,140} % Light gray color
\arrayrulecolor{lightgray}

\setlength{\dashlinedash}{2pt}
\setlength{\dashlinegap}{4pt}

% centerinig column type with horizontal padding
\newcolumntype{C}[1]{%
  >{\begin{minipage}[c][1.32cm][c]{#1}% Outer minipage (fixed dimensions)
    \hspace*{''' + CELL_INNER_PADDING + r'''}% Left padding
    \begin{minipage}[c]{\dimexpr#1-''' + _CELL_INNER_PADDING_DOUBLED + r'''}% Inner minipage (adjusted width)
    \centering\arraybackslash
  }%
  p{#1}% Column width specification
  <{%
    \end{minipage}% Close inner minipage
    \hspace*{''' + CELL_INNER_PADDING + r'''}% Right padding
  \end{minipage}}% Close outer minipage
}
\setlength{\tabcolsep}{0pt} % Remove inter-column padding


\begin{document}
\pagestyle{empty}
\begin{center}
\fontsize{''' + str(FONT_SIZE) + r'''}{''' + str(FONT_LINE_SPACING) + r'''}\selectfont
{\fontfamily{''' + FONT_FAMILY + r'''}\selectfont
\begin{tabular}{ : *{''' + str(COLUMN_COUNT) + r'''}{C{''' + str(CELL_WIDTH) + r'''}:} }
\hdashline
'''

    # Add switch names to tabular environment
    for i, name in enumerate(names):
        # Escape special LaTeX characters
        name = name.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
        latex += name
        if (i + 1) % COLUMN_COUNT == 0 and i < len(names) - 1:
            latex += r" \\ " + "\n" + r"\hdashline" + "\n"
        elif i < len(names) - 1:
            latex += " & "
        else:
            # Fill remaining cells in the last row with empty cells
            if (i + 1) % COLUMN_COUNT != 0:
                latex += " & " * (COLUMN_COUNT - (i + 1) % COLUMN_COUNT)
            latex += r" \\ " + "\n" + r"\hdashline"

    # Close LaTeX document
    latex += r'''
\end{tabular}
}
\end{center}
\end{document}'''
    return latex

def main():
    try:
        switch_names = read_switch_names(INPUT_FILE)
        latex_code = generate_latex(switch_names)
        
        with open(OUTPUT_FILE, 'w') as f:
            f.write(latex_code)
        print(f"LaTeX file generated: {OUTPUT_FILE}")
        
        print(f"Next you'll need to compile the tex file to create a pdf. Either use an online tex compiler like https://www.overleaf.com or download a compiler such as https://miktex.org/download")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()