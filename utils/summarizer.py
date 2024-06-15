import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def summarize_job_description(jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    prompt = f"""Summarize the following job description in 3-4 sentences, highlighting the key requirements and responsibilities:

Description: {jd}

Additional Notes:
Do not add any additional information from your side instead use the {jd} to summarize the job description.
"""
    response = model.generate_content(prompt)
    return response.text.strip()  # Get summarized text
