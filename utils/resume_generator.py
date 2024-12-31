# import os
# import google.generativeai as genai
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv
# import json

# load_dotenv()

# def generate_altered_resume(original_text, analysis):
#     api_key = os.getenv('GENAI_API_KEY')
#     genai.configure(api_key=api_key)

#     model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

#     prompt = f"""
# Act like a highly skilled resume editor. Your task is to take the original resume and the analysis results and generate an improved resume. 

# Original Resume:
# {original_text}

# Analysis Results:
# {json.dumps(analysis, indent=2)}

# Based on the analysis results, update the resume to improve its JD Match, add missing keywords, remove irrelevant content, and enhance ATS friendliness.

# Generate the new resume in plain text format.
# """

#     response = model.generate_content(prompt)
#     new_resume_text = response.text.strip()

#     return new_resume_text

# def generate_html_resume(text):
#     # Parsing the plain text resume into HTML format (customize as needed)
#     experiences = "<div>{}</div>".format(text.replace("\n", "<br>"))
    
#     html_template = """
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8" />
#     <link rel="stylesheet" type="text/css" href="dep/normalize.css/normalize.css" />
#     <link rel="stylesheet" type="text/css" href="dep/Font-Awesome/css/font-awesome.css" />
#     <link rel="stylesheet" type="text/css" href="style.css" />
# </head>
# <body lang="en">
#     <section id="main">
#         <header id="title">
#             <h1>{name}</h1>
#             <span class="subtitle">{subtitle}</span>
#         </header>
#         <section class="main-block">
#             <h2>
#                 <i class="fa fa-suitcase"></i> Experiences
#             </h2>
#             {experiences}
#         </section>
#         <section class="main-block">
#             <h2>
#                 <i class="fa fa-folder-open"></i> Selected Projects
#             </h2>
#             {projects}
#         </section>
#         <section class="main-block concise">
#             <h2>
#                 <i class="fa fa-graduation-cap"></i> Education
#             </h2>
#             {education}
#         </section>
#     </section>
#     <aside id="sidebar">
#         <div class="side-block" id="contact">
#             <h1>Contact Info</h1>
#             <ul>
#                 <li><i class="fa fa-globe"></i> {website}</li>
#                 <li><i class="fa fa-linkedin"></i> {linkedin}</li>
#                 <li><i class="fa fa-envelope"></i> {email}</li>
#                 <li><i class="fa fa-phone"></i> {phone}</li>
#             </ul>
#         </div>
#         <div class="side-block" id="skills">
#             <h1>Skills</h1>
#             {skills}
#         </div>
#         <div class="side-block" id="disclaimer">
#             This r&eacute;sum&eacute; was wholly typeset with HTML/CSS &mdash; see <code>git.io/vVSYL</code>
#         </div>
#     </aside>
# </body>
# </html>
# """
#     html_content = html_template.format(
#         name="John Doe",  # Replace with actual data
#         subtitle="Plaintiff, defendant & witness",  # Replace with actual data
#         experiences=experiences,  # Replace with parsed experiences
#         projects="",  # Replace with parsed projects
#         education="",  # Replace with parsed education
#         website="johndoe.gtld",  # Replace with actual data
#         linkedin="linkedin.com/in/john",  # Replace with actual data
#         email="me@johndoe.gtld",  # Replace with actual data
#         phone="800.000.0000",  # Replace with actual data
#         skills="<ul><li>Omnipresence</li><li>Anonymity</li></ul>"  # Replace with actual data
#     )

#     return html_content

# def create_new_resume(original_pdf, analysis):
#     reader = PdfReader(original_pdf)
#     original_text = ''
#     for page in reader.pages:
#         original_text += page.extract_text()

#     new_resume_text = generate_altered_resume(original_text, analysis)
#     html_resume = generate_html_resume(new_resume_text)

#     return html_resume

# if __name__ == "__main__":
#     # Sample usage
#     sample_analysis = {
#         "JD Match": "75%",
#         "MissingKeywords": ["Python", "Machine Learning"],
#         "Profile Summary": "Experienced software engineer with a background in data science.",
#         "ATS Friendliness": "Moderately ATS-friendly",
#         "ThingsToBeRemoved": ["Objective statement"],
#         "ThingsToBeAdded": ["Technical skills section", "Projects section"]
#     }

#     with open("sample_resume.pdf", "rb") as original_pdf:
#         html_resume = create_new_resume(original_pdf, sample_analysis)
#         print(html_resume)


from flask import render_template_string
from utils.pdf_extractor import input_pdf_text
from utils.resume_analyzer import analyze_resume

# Template for generating the HTML resume
resume_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <link rel="stylesheet" type="text/css" href="dep/normalize.css/normalize.css" />
    <link rel="stylesheet" type="text/css" href="dep/Font-Awesome/css/font-awesome.css" />
    <link rel="stylesheet" type="text/css" href="style.css" />
  </head>
  <body lang="en">
    <section id="main">
      <header id="title">
        <h1>{{ name }}</h1>
        <span class="subtitle">{{ subtitle }}</span>
      </header>
      <section class="main-block">
        <h2>
          <i class="fa fa-suitcase"></i> Experiences
        </h2>
        {% for experience in experiences %}
        <section class="blocks">
          <div class="date">
            <span>{{ experience.start_date }}</span><span>{{ experience.end_date }}</span>
          </div>
          <div class="decorator">
          </div>
          <div class="details">
            <header>
              <h3>{{ experience.position }}</h3>
              <span class="place">{{ experience.workplace }}</span>
              {% if experience.location %}
              <span class="location">{{ experience.location }}</span>
              {% endif %}
            </header>
            <div>
              <ul>
                {% for point in experience.points %}
                <li>{{ point }}</li>
                {% endfor %}
              </ul>
            </div>
          </div>
        </section>
        {% endfor %}
      </section>
      <!-- Other sections like Projects, Education, Contact Info, Skills can be similarly templated -->
    </section>
    <aside id="sidebar">
      <!-- Sidebar content (Contact Info, Skills, etc.) -->
    </aside>
  </body>
</html>
"""

def create_new_resume(original_resume_file, analysis_result):
    # Extract text from original resume PDF
    original_resume_text = input_pdf_text(original_resume_file)

    # Example analysis_result structure: Replace with actual analysis result structure
    # Example structure: analysis_result = {"experiences": [{"position": "Software Engineer", "points": ["Developed web applications", "Led a team of 5 developers"]}, ...]}
    
    # Use the original_resume_text and analysis_result to modify the resume content
    modified_resume_content = modify_resume(original_resume_text, analysis_result)

    # Render the modified content using the template
    rendered_html_resume = render_template_string(resume_template, **modified_resume_content)

    return rendered_html_resume

def modify_resume(original_resume_text, analysis_result):
    # Logic to modify the original_resume_text based on analysis_result
    # For example, updating experiences, projects, education sections, etc.
    # Implement this based on your specific requirements and analysis result structure
    modified_resume_content = {
        "name": "John Doe",
        "subtitle": "Plaintiff, defendant & witness",
        "experiences": [
            {
                "start_date": "2015",
                "end_date": "present",
                "position": "Software Engineer",
                "workplace": "Some Workplace",
                "location": "(remote)",
                "points": [
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec mi ante. Etiam odio eros, placerat eu metus id, gravida eleifend odio. Vestibulum dapibus pharetra odio, egestas ullamcorper ipsum congue ac. Maecenas viverra tortor eget convallis vestibulum. Donec pulvinar venenatis est, non sollicitudin metus laoreet sed. Fusce tincidunt felis nec neque aliquet porttitor"
                ]
            },
            # Add more experiences as needed
        ]
        # Add other sections like projects, education, contact info, skills, etc.
    }

    return modified_resume_content
