import os
import google.generativeai as genai
import json
from .summarizer import summarize_job_description

# def analyze_resume(text, jd):
#     # Summarize the job description first
#     summary = summarize_job_description(jd)

#     api_key = os.getenv('GENAI_API_KEY')
#     genai.configure(api_key=api_key)

#     model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

#     prompt = f"""
#     Act like a highly skilled and experienced ATS (Application Tracking System) with a deep understanding of the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the following resume and job description:

#     Resume:

#     {text}

#     Job Description Summary:  
#     {summary}

#       Original Job Description (For your reference only, not used for evaluation):  

#     {jd}

#       Original Resume (For your reference only, not used for evaluation):  
# #
#     {text}

#     For each evaluation, you should provide the following:

#     1.   JD Match (Percentage):   Assign a percentage matching score between the resume and the job description summary. This score should reflect the relevance of the resume's content to the job requirements.
#     2.   Missing Keywords:   Identify and list any keywords from the job description summary that are missing from the resume.
#     3.   Profile Summary:   Briefly summarize the strengths and relevance of the candidate's profile based on the resume and job description summary.
#     4.   ATS Friendliness:   Assess the resume's suitability for Applicant Tracking Systems (ATS) considering formatting, keyword usage, clarity, file type, contact information, data presentation consistency, structure, and headers/footers. Indicate "Highly ATS-friendly," "Moderately ATS-friendly," or "Not ATS-friendly."
#     5.   Things to Remove:   Suggest any elements in the resume that could be removed to enhance its relevance and readability.
#     6.   Things to Add:   Suggest any information the candidate could add to the resume to improve its alignment with the job description summary.

#       Please note:  

#     * Do not access or use any information beyond the provided resume and job description summary.
#     * Base all scores and suggestions solely on the provided content.
#     * If there is insufficient information to determine a specific value (e.g., missing keywords), indicate "I don't have enough information to determine this."

#       Output format:  
#     {{
#       "JD Match": "",
#       "MissingKeywords": [],
#       "Profile Summary": "",
#       "ATS Friendliness": "",
#       "ThingsToBeRemoved": [],
#       "ThingsToBeAdded": []
#     }}
#     """

#     response = model.generate_content(prompt)
#     return response.text.strip()
def analyze_resume(text, jd):
    api_key = os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model

    # Prompt template
    prompt = f"""
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
    "JD Summary": ""
]
"""

    response = model.generate_content(prompt)
    return json.loads(response.text) 