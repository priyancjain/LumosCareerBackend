from flask import Flask, request, render_template, jsonify
from utils.pdf_extractor import input_pdf_text
from utils.cover_letter import cover_letter
from utils.resume_analyzer import analyze_resume
from utils.summarizer import summarize_job_description
import os
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

if __name__ == "__main__":
    app.run(debug=True)
