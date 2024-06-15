import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def cover_letter(text, jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model
    
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
