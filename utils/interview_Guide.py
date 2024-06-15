import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

def generate_interview_guide(text, jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    prompt = f"""
Generate an interview guide based on the following job description and resume highlights:

Job Description:
{jd}

Resume Highlights:
{text}

Consider the following aspects when generating the guide:
- Tailor questions to assess candidate's experience, skills, and alignment with the job requirements.
- Provide suggested answers or points to look for in responses.
- Offer suggestions about topics and things to keep in mind during the interview.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
