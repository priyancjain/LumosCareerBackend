from flask import Flask, request, render_template, jsonify
import PyPDF2
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json  # Assuming you have access

# Load environment variables (assuming you have a .env file)
load_dotenv()

app = Flask(__name__)

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def cover_letter(text, jd):
    api_key=os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model
    
    # Prompt for cover letter generation
    prompt = f"""
Instructions:
Please write a cover letter tailored to the job description and resume provided below. Highlight relevant experiences, skills, and accomplishments that align with the requirements and responsibilities of the job. Ensure the cover letter is professional, concise, and compelling.

Job Description:
{jd}

Resume Highlights:
You can access the resume highlights from the uploaded file: {text}

Things to Avoid:
- Do not add any additional information from your side.
- Only use the provided job description {jd} and resume highlights {text} to generate the cover letter.
- Do not add any extra skills from your side
- Do not add any address or contact information.
Things to Include:
- Instead of Your Name, use the name from the first two words of{text}
- Ensure the tone is professional and enthusiastic, expressing genuine interest in the position and the company.
- Add the company name from {jd} in the cover letter.

"""



    response = model.generate_content(prompt)
    return response.text.strip()

# Function to summarize job description using Gemini
def summarize_job_description(jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    # Prompt for summarizing job description
    prompt = f"""Summarize the following job description in 3-4 sentences, highlighting the key requirements and responsibilities:

Description: {jd}

Additional Notes:
Do not add any additional information from your side instead use the {jd} to summarize the job description.
"""

    response = model.generate_content(prompt)
    return response.text.strip()  # Get summarized text

# Function to analyze resume using Gemini (chained with summarization)
def analyze_resume(text, jd):
    # Summarize the job description first
    summary = summarize_job_description(jd)

    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    # Prompt template (using summarized JD)
    prompt = """
Hey, act like a highly skilled and experienced ATS (Application Tracking System) with a deep understanding of the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the following summarized job description:

{summary}

The original job description is available here: {jd} (assuming you store it somewhere)

For each evaluation, you should:

1. Assign a percentage matching score based on the job description.
2. Identify and list the missing keywords that are important for the job description.
3. Provide a profile summary that highlights the strengths and relevance of the resume to the job description.
4. Assess the ATS friendliness of the resume, considering factors like formatting, use of keywords, and clarity.
5. Suggest things to be removed from the resume to enhance its relevance and readability.
6. Suggest things to be added to the resume to improve its alignment with the job description.

Evaluate the following resume and job description:

Resume: {text}
Description: {jd}

I want the response in one single string with the following structure:
{
    "JD Match": "%",
    "MissingKeywords": [],
    "Profile Summary": "",
    "ATS Friendliness": "",
    "ThingsToBeRemoved": [],
    "ThingsToBeAdded": [],
    "JD Summary": "{summary}",
}

Additional Notes:
Do not add any additional information from your side instead use the {jd} and {text} to analyze resume.
"""

    response = model.generate_content(prompt)
    return json.loads(response.text)  # Ensure the response is JSON serializable

# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route to summarize job description
@app.route("/summarize", methods=["POST"])
def summarize():
    
    data = request.get_json()
    jd = data.get("job_description")

    if jd:
        summary = summarize_job_description(jd)
        return jsonify({"summary": summary})
    else:
        return jsonify({"error": "No job description provided"})

# Route to handle resume upload and analysis
@app.route("/analyze", methods=["POST"])
def analyze():
    jd = request.form["job_description"]
    uploaded_file = request.files["resume"]

    if uploaded_file and jd:
        text = input_pdf_text(uploaded_file)
        analysis_result = analyze_resume(text, jd)
        return jsonify(analysis_result)  # Return JSON response
    else:
        return jsonify({"error": "No resume or job description provided"})
@app.route("/coverletter", methods=["POST"])
def coverletter():
    jd = request.form["job_description"]
    uploaded_file = request.files["resume"]

    if uploaded_file and jd:
        text = input_pdf_text(uploaded_file)
        cover_letter_text = cover_letter(text, jd)
        return jsonify({"cover_letter": cover_letter_text})
# Run the Flask app (assuming you have a templates folder with index.html)
if __name__ == "__main__":
    app.run(debug=True)
