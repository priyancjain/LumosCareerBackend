from flask import Flask, request, render_template, jsonify,send_file
from utils.pdf_extractor import input_pdf_text
from utils.cover_letter import cover_letter
from utils.resume_analyzer import analyze_resume
from utils.summarizer import summarize_job_description
from utils.interview_Guide import generate_interview_guide
from utils.resume_generator import create_new_resume
from werkzeug.utils import secure_filename
from utils.cold_mail import cold_mail
import io
import os
import PyPDF2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    jd = data.get("job_description")

    if jd:
        summary = summarize_job_description(jd)
        return jsonify({"summary": summary})
    else:
        return jsonify({"error": "No job description provided"})

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
    
@app.route("/interviewguide", methods=["POST"])
def interviewguide():
    jd = request.form["job_description"]
    uploaded_file = request.files["resume"]

    if uploaded_file and jd:
        text = input_pdf_text(uploaded_file)
        interview_guide_text = generate_interview_guide(text, jd)
        return jsonify({"interview_guide": interview_guide_text})
    else:
        return jsonify({"error": "No resume or job description provided"})
    
@app.route("/generate", methods=["POST"])
def generate():
    jd = request.form["job_description"]
    uploaded_file = request.files["resume"]

    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part"})

    resume_file = request.files['resume']

    # If the user does not select a file, browser also submit an empty part without filename
    if resume_file.filename == '':
        return jsonify({"error": "No selected file"})

    # Ensure the filename is secure
    filename = secure_filename(resume_file.filename)

    # Save the uploaded resume to a temporary location
    resume_path = '/Users/priyanshijain/Data_Science/project/job_buddy/' + filename
    resume_file.save(resume_path)

    # Example job description (you can get this from the frontend as needed)
    jd = "Your job description here"

    # Analyze the uploaded resume
    text = resume_file.read().decode('utf-8')  # Read and decode the resume content
    analysis_result = analyze_resume(text, jd)

    # Generate the modified resume HTML
    html_resume = create_new_resume(resume_path, analysis_result)

    # Return the HTML as a string to the frontend
    return jsonify({"html_resume": html_resume})

@app.route("/extra", methods=["POST"])
def extra():
    jd = request.form["job_description"]
    uploaded_file = request.files["resume"]

    if uploaded_file and jd:
        text = input_pdf_text(uploaded_file)
        cover_letter_text = cold_mail(text, jd)
        return jsonify({"cold_mail": cover_letter_text})
    


if __name__ == "__main__":
    app.run(debug=True)
