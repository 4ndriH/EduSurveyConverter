file1 = open("clicker_export_eduapp.edu", "r")
file2 = open("output.tex", "w")

preamble = "\\documentclass[10pt]{article}\n" \
           "\\usepackage{pgfplots}\n" \
           "\\pgfplotsset{compat=1.18}\n" \
           "\\usepackage{tikz}\n" \
           "\\usepackage[margin=0.5in]{geometry}\n" \
           "\\usepackage{fancyhdr}\n\n" \
           "\\begin{document}\n"

noPageBreak = "\\newenvironment{absolutelynopagebreak}\n" \
              "{\\par\\nobreak\\vfil\penalty0\\vfilneg \\vtop\\bgroup}\n" \
              "{\\par\\xdef\\tpd{\\the\prevdepth}\\egroup\\prevdepth=\\tpd}"

title = "\\begin{flushleft}\n" \
        "\\underline{\\huge{\\textbf{Survey Thingy}}}\\\\[1mm]\n" \
        "\\end{flushleft}\n"

file2.writelines(preamble)
file2.writelines(noPageBreak)
file2.writelines(title)

questions = []

while True:
    question = file1.readline()

    if not question:
        break

    tempTex = "\\line(1,0){530}\\\\\n" + question.strip() + "\n\\line(1,0){530}\\\\\n"
    line = file1.readline().strip()

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

        tempPlot = ""

        for v, a in zip(votes, answers):
            tempPlot += "(" + str(v) + "," + a + ")\n"

        tempTex += "\\begin{tikzpicture}\n" \
                   "\\begin{axis} [xbar, bar width=25pt, symbolic y coords={" + (",".join(answers)) + "}]\n" \
                   "\\addplot [fill = orange] coordinates {" + tempPlot + "};\n" \
                   "\\end{axis}\n" \
                   "\\end{tikzpicture}\n"

    elif line.__contains__("Answer"):
        tempFeedback = ""

        while True:
            line = file1.readline().strip().replace("\"", "")

            if len(line) == 0:
                break

            tempFeedback += line + "\\\\\n-\\\\\n"

        tempTex += tempFeedback

    questions.append(tempTex)

for question in questions:
    file2.writelines("\\begin{flushleft}\n"
                     "\\begin{absolutelynopagebreak}\n"
                     + question + "\n"
                     "\\end{absolutelynopagebreak}\n"
                     "\\end{flushleft}\n")

file2.writelines("\\end{document}")

file2.close()
