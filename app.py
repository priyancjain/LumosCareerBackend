from flask import Flask, request, render_template, jsonify
import PyPDF2
from dotenv import load_dotenv
import os
import google.generativeai as genai 
import json # Assuming you have access

# Load environment variables (assuming you have a `.env` file)
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

# Function to analyze resume using Gemini
def analyze_resume(text, jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    # Prompt template
    prompt = """
Hey, act like a highly skilled and experienced ATS (Application Tracking System) with a deep understanding of the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider that the job market is very competitive, and you should provide the best assistance for improving the resumes. 

For each evaluation, you should:

1. Assign a percentage matching score based on the job description.
2. Identify and list the missing keywords that are important for the job description.
3. Provide a profile summary that highlights the strengths and relevance of the resume to the job description.
4. Assess the ATS friendliness of the resume, considering factors like formatting, use of keywords, and clarity.
5. Suggest things to be removed from the resume to enhance its relevance and readability.
6. Suggest things to be added to the resume to improve its alignment with the job description.
7. Suggestions for improving the resume's overall quality and relevance.

Evaluate the following resume and job description:

Resume: {text}
Description: {jd}

I want the response in one single string with the following structure:
[
    "JD Match": "%",
    "MissingKeywords": [],
    "Profile Summary": "",
    "ATS Friendliness": "",
    "ThingsToBeRemoved": [],
    "ThingsToBeAdded": [],
    "JD Summary": "",
]
"""

    response = model.generate_content(prompt)
    return json.loads(response.text)  # Ensure the response is JSON serializable

# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle resume upload and analysis
@app.route("/analyze", methods=["POST"])
def analyze():
    if request.method == "POST":
        jd = request.form["job_description"]
        uploaded_file = request.files["resume"]

        if uploaded_file:
            text = input_pdf_text(uploaded_file)
            analysis_result = analyze_resume(text, jd)
            return jsonify(analysis_result)  # Return JSON response

        else:
            return jsonify({"error": "No resume uploaded"})

# Run the Flask app (assuming you have a `templates` folder with `index.html`)
if __name__ == "__main__":
    app.run(debug=True)
