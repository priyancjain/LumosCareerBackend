import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def analyze_resume(text, jd):
    api_key = os.getenv('GENAI_API_KEY')
    if not api_key:
        return {"error": "API key not found. Please set GENAI_API_KEY in your environment variables."}
    
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel('gemini-pro')  # Assuming Gemini Pro model
    except Exception as e:
        return {"error": f"Failed to configure model: {e}"}

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
    {{
        "JD Match": "%",
        "MissingKeywords": [],
        "Profile Summary": "",
        "ATS Friendliness": "",
        "ThingsToBeRemoved": [],
        "ThingsToBeAdded": [],
        "JD Summary": ""
    }}
    """

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        return {"error": f"Failed to generate content: {e}"}
    
    response_text = response.text.strip()

    # Debug: Print the raw response text
    print("Response text:", response_text)
    
    # Attempt to parse the JSON response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return {"error": "Failed to decode JSON response from API"}

# Example usage
# if __name__ == "__main__":
#     # Example text and job description
#     resume_text = "John Doe's resume..."
#     job_description = "Software Engineer job description..."
#     result = analyze_resume(resume_text, job_description)
#     print(result)
