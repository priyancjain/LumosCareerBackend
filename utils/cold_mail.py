import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def cold_mail(text, jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model
    
    prompt = f"""
Job Description:
{{jd}}

Resume:
{{text}}

Write an email to the company using the following format:

Subject: Unique Application for [Position] - [Your Name]

Dear [Recipient Name],

I saw that [Company] is advertising to fill the role of [Position]. I'm very interested in this opportunity, as it aligns perfectly with my passion for [relevant field/industry].

Rather than simply sending my resume and cover letter, I decided to [unique action or project you've done related to the job]. This [action/project] demonstrates my [relevant skills] and showcases why I would be an excellent candidate for the [Position] role.

Key highlights of my experience:
- [Relevant achievement or skill 1]
- [Relevant achievement or skill 2]
- [Relevant achievement or skill 3]

In my current role as [Current Role] at [Current Company], I've gained valuable experience in [relevant area], which I believe would translate well to the [Position] at [Company].

I'd love to schedule a time to discuss my suitability for the role within the next two weeks. If I haven't heard back from you by [specific date, about 10 days from now], I'll follow up to ensure you received my application.

Thank you for your time and consideration. I look forward to the opportunity to speak with you about how I can contribute to [Company]'s success.

Sincerely,
[Your Name]
[Your Phone Number]
[Your Email Address]

Instructions:
- [Position], [Company], and [Recipient Name] should be taken from {{jd}}
- [Current Role] and [Current Company] should be taken from {{text}}
- [Your Name], [Your Phone Number], and [Your Email Address] should be filled with the applicant's details from {text}and {jd}
- [unique action or project] should be something specific and relevant to the job that sets the applicant apart
- Fill in [relevant field/industry], [relevant skills], [Relevant achievement or skill 1/2/3], and [relevant area] based on information from {{text}} and {{jd}}
- Set [specific date] to be about 10 days from the current date
- Ensure the email is tailored to the specific job and company, highlighting the applicant's unique approach
- Maintain a professional yet engaging tone throughout the email

Important thing
ALL THE INFORMATION SHOULD BE TAKEN RESUME {text} and JOB DESCRIPTION {jd}
EMail sholud be short and concise miniumum 100 words..
"""
    
    # Generate content using the prompt
    # response = model.generate_content(prompt)
    
    # # Check if response is valid
    # if response and 'generated_text' in response:
    #     generated_text = response.generated_text.strip()  # Access 'generated_text' property
    #     return generated_text
    # else:
    #     raise RuntimeError("Failed to generate content")
    response = model.generate_content(prompt)
    return response.text.strip()

