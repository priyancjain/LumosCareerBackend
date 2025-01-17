# import subprocess
# from pylatex.base_classes import CommandBase
# from pylatex.package import Package
# from pylatex import Document, Command, UnsafeCommand
# from pylatex.utils import NoEscape

# class MyName(CommandBase):
#     _latex_name = 'MyName'

# class MySlogan(CommandBase):
#     _latex_name = 'MySlogan'

# class NewPart(CommandBase):
#     _latex_name = 'NewPart'

# class PersonalEntry(CommandBase):
#     _latex_name = 'PersonalEntry'

# class SkillsEntry(CommandBase):
#     _latex_name = 'SkillsEntry'

# class EducationEntry(CommandBase):
#     _latex_name = 'EducationEntry'

# class WorkEntry(CommandBase):
#     _latex_name = 'WorkEntry'

# if __name__ == '__main__':
#     doc = Document(documentclass='scrartcl', document_options=["paper=a4", "fontsize=11pt"])

#     doc.preamble.append(Command("usepackage", "mdframed"))
#     doc.preamble.append(Command("usepackage", "babel", "english"))
#     doc.preamble.append(Command("usepackage", "microtype", ["protrusion=true", "expansion=true"]))
#     doc.preamble.append(Command("usepackage", "amsmath"))
#     doc.preamble.append(Command("usepackage", "amsfonts"))
#     doc.preamble.append(Command("usepackage", "amsthm"))
#     doc.preamble.append(Command("usepackage", "graphicx"))
#     doc.preamble.append(Command("usepackage", "xcolor", "svgnames"))
#     doc.preamble.append(Command("usepackage", "geometry"))
#     doc.preamble.append(Command("usepackage", "url"))
#     doc.preamble.append(Command("usepackage", "sectsty"))

#     doc.append(Command('frenchspacing'))
#     doc.append(Command('pagestyle', 'empty'))
#     doc.append(Command("textheight=700px"))
#     doc.append(Command("sectionfont", NoEscape(r"\usefont{OT1}{phv}{b}{n} \sectionrule{0pt}{0pt}{-5pt}{3pt}}")))

#     doc.append(Command("newlength", Command("spacebox")))
#     doc.append(Command("settowidth", [Command("spacebox"), "8888888888"]))

#     sepspace = UnsafeCommand('newcommand', r'\sepspace',
#                              extra_arguments=r"""
#                              \vspace*{1em}
# """)
#     doc.append(sepspace)

#     MyName = UnsafeCommand('newcommand', r'\MyName', options=1,
#                            extra_arguments=r"""
#             \Huge \usefont{OT1}{phv}{b}{n} \hfill #1
#             \par \normalsize \normalfont
# """)
#     doc.append(MyName)

#     MySlogan = UnsafeCommand('newcommand', r'\MySlogan', options=1,
#                              extra_arguments=r"""
#         \large \usefont{OT1}{phv}{m}{n}\hfill \textit{#1}
#         \par \normalsize \normalfont
# """)
#     doc.append(MySlogan)

#     NewPart = UnsafeCommand('newcommand', r'\NewPart', options=1,
#                              extra_arguments=r"""
#                              \section*{\uppercase{#1}}
# """)
#     doc.append(NewPart)

#     PersonalEntry = UnsafeCommand('newcommand', r'\PersonalEntry', options=2,
#                                   extra_arguments=r"""
#         \noindent\hangindent=2em\hangafter=0 % Indentation
#         \parbox{\spacebox}{        % Box to align text
#         \textit{#1}}               % Entry name (birth, address, etc.)
#         \hspace{1.5em} #2 \par}    % Entry value
#  """)
#     doc.append(PersonalEntry)

#     SkillsEntry = UnsafeCommand('newcommand', r'\SkillsEntry', options=2,
#                                 extra_arguments=r"""
#         \noindent\hangindent=2em\hangafter=0 % Indentation
#         \parbox{\spacebox}{        % Box to align text
#         \textit{#1}}			   % Entry name (birth, address, etc.)
#         \hspace{1.5em} #2 \par    % Entry value
# """)
#     doc.append(SkillsEntry)

#     EducationEntry = UnsafeCommand('newcommand', r'\EducationEntry', options=4,
#                                    extra_arguments=r"""
#         \noindent \textbf{#1} \hfill      % Study
#         \colorbox{Black}{%
#             \parbox{6em}{%
#             \hfill\color{White}#2}} \par  % Duration
#         \noindent \textit{#3} \par        % School
#         \noindent\hangindent=2em\hangafter=0 \small #4 % Description
#         \normalsize \par
#  """)
#     doc.append(EducationEntry)

#     WorkEntry = UnsafeCommand('newcommand', r'\WorkEntry', options=4,
#                               extra_arguments=r"""
#          % Same as \EducationEntry
#         \noindent \textbf{#1} \hfill      % Jobname
#         \colorbox{Black}{\color{White}#2} \par  % Duration
#         \noindent \textit{#3} \par              % Company
#         \noindent\hangindent=2em\hangafter=0 \small #4 % Description
#         \normalsize \par
#  """)
#     doc.append(WorkEntry)

#     doc.append(Command("MyName", "Abhinav Sharma"))
#     doc.append(Command('MySlogan', 'Curriculum Vitae'))
#     doc.append(Command('sepspace'))

#     doc.append(Command('NewPart', ["Personal details", NoEscape("")]))
#     doc.append(Command('PersonalEntry', ["Birth", "January 1, 1980"]))
#     doc.append(Command('PersonalEntry', ["Address", "111 First St, New York"]))
#     doc.append(Command('PersonalEntry', ["Phone", "(123) 000-0000"]))

#     doc.append(Command('NewPart', ["Education details", NoEscape("")]))
#     doc.append(Command("EducationEntry", ["MSc. Name of Education", NoEscape("2010-2012"), "Name of University", """Descriptive text goes here. In order to maintain a stylish look, try to fill this description with a few lines of text. Do the same for the other entries in the education section."""]))

#     doc.append(Command('sepspace'))

#     doc.append(Command('NewPart', ["Skills", NoEscape("")]))
#     doc.append(Command("SkillsEntry", ["Human Languages", "English (fluent)"]))
#     doc.append(Command("SkillsEntry", [NoEscape(""), "Portuguese (fluent)"]))
#     doc.append(Command("SkillsEntry", ["Programming Languages", "Clojure"]))

#     doc.append(Command('NewPart', ["Work details", NoEscape("")]))
#     doc.append(Command("WorkEntry", ["Chief Technology Officer", NoEscape("August 2018 - Present"), "Cyber Indian App Stores", """I am leading a team of 8 in the core engineering wing."""]))
#     doc.append(Command('sepspace'))
#     doc.append(Command("WorkEntry", [NoEscape("Software Engineer - Machine Learning"), NoEscape("August 2016 - July 2017"), "Fourtek (IT) Solutions Pvt. Ltd.", """I worked as a co-founder of a product targeting the StartUp ecosystem."""]))
#     doc.append(Command('sepspace'))

#     doc.generate_tex("./simple-resume")

#     # Generate PDF from LaTeX using latexmk
#     subprocess.run(["latexmk", "-pdf", "./simple-resume.tex"])
import subprocess

def tex_to_pdf(tex_file):
  """Converts a LaTeX file to PDF.

  Args:
    tex_file: Path to the .tex file.

  Returns:
    True on success, False otherwise.
  """
  # Compile LaTeX
  process = subprocess.run(["pdflatex", tex_file])
  if process.returncode != 0:
    print("Error: LaTeX compilation failed.")
    return False

  # Optionally convert DVI to PDF (if not done by pdflatex)
  # ... (code for dvipdfmx)

  return True

# Example usage
if tex_to_pdf("mydocument.tex"):
  print("PDF generated successfully!")
