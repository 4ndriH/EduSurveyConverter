file1 = open("clicker_export_eduapp.edu", "r")
file2 = open("output.tex", "w")

preamble = "\\documentclass[10pt]{article}\n\\usepackage{pgfplots}\n\\pgfplotsset{compat=1.18}\n\\usepackage{tikz}\n\\usepackage[margin=0.5in]{geometry}\n\\usepackage{fancyhdr} \\begin{document}\n"
title = "\\begin{flushleft}\n\\underline{\\huge{\\textbf{Survey Thingy}}}\\\\[1mm]\n\\end{flushleft}\n"
file2.writelines(preamble)
file2.writelines(title)

while True:
    line = file1.readline()

    if not line:
        break

    line = line.strip()

    if line.__contains__("Answer,Votes,Percent"):
        answers = []
        votes = []
        percentages = []
        while True:
            line = file1.readline().strip().replace("\"", "")

            if len(line) == 0:
                break

            split = line.split(",")
            answers.append(split[0])
            votes.append(int(split[1]))
            percentages.append(float(split[2]))

        file2.writelines("\\begin{tikzpicture}\n\\begin{axis} [xbar, bar width=25pt, symbolic y coords={"+(",".join(answers)) + "}]\n")
        file2.writelines("\\addplot [fill = orange] coordinates {\n")

        for v, a in zip(votes, answers):
            file2.writelines("(" + str(v) + "," + a + ")\n")

        file2.writelines("};\n\\end{axis}\n\\end{tikzpicture}\n")

        print(percentages)
    elif line.__contains__("Answer"):
        while True:
            line = file1.readline().strip().replace("\"", "")

            if len(line) == 0:
                break

            file2.writelines(line + "\n\\\\-\\\\\n")
    else:
        file2.writelines("\\begin{flushleft}\n\\line(1,0){530}\\\\\n" + line + "\n\\line(1,0){530}\\\\\n\\end{flushleft}\n")

file2.writelines("\\end{document}")

file2.close()
