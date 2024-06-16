import os
import google.generativeai as genai
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
from dotenv import load_dotenv
import json

load_dotenv()

def generate_altered_resume(original_text, analysis):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    prompt = f"""
Act like a highly skilled resume editor. Your task is to take the original resume and the analysis results and generate an improved resume. 

Original Resume:
{original_text}

Analysis Results:
{json.dumps(analysis, indent=2)}

Based on the analysis results, update the resume to improve its JD Match, add missing keywords, remove irrelevant content, and enhance ATS friendliness.

Generate the new resume in plain text format.
"""

    response = model.generate_content(prompt)
    new_resume_text = response.text.strip()

    return new_resume_text

def save_as_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)

def create_new_resume(original_pdf, analysis):
    reader = PdfReader(original_pdf)
    original_text = ''
    for page in reader.pages:
        original_text += page.extract_text()

    new_resume_text = generate_altered_resume(original_text, analysis)
    new_pdf_filename = 'altered_resume.pdf'
    save_as_pdf(new_resume_text, new_pdf_filename)

    with open(new_pdf_filename, 'rb') as file:
        pdf_data = file.read()

    return pdf_data, new_resume_text

if __name__ == "__main__":
    # Sample usage
    sample_analysis = {
        "JD Match": "75%",
        "MissingKeywords": ["Python", "Machine Learning"],
        "Profile Summary": "Experienced software engineer with a background in data science.",
        "ATS Friendliness": "Moderately ATS-friendly",
        "ThingsToBeRemoved": ["Objective statement"],
        "ThingsToBeAdded": ["Technical skills section", "Projects section"]
    }

    with open("sample_resume.pdf", "rb") as original_pdf:
        pdf_data, new_resume_text = create_new_resume(original_pdf, sample_analysis)
        print(new_resume_text)
