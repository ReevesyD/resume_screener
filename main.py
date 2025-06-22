import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv

# Set variables
resume_filepath = "resume.txt"
job_listing_filepath = "job_listing.txt"

# Load API key from .env
load_dotenv()

# Function that returns the text of a file at a given path
def readfile(filepath):
    with open(filepath, "r") as file:
        return file.read()

# Makes the API call to open AI
def get_completion(prompt):
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": prompt}])
    return response.choices[0].message.content.strip()

# Defines the prompt with the resume and job listing text, calls the function that makes the api call
def make_prompt(resume, job_listing):
    prompt = f"""
        You are a system that extracts skill comparisons between a resume and a job listing.

        Given the resume and job listing below, return ONLY in this structured format:

        Applicant Skills:
        - Skill: <name>, Level: <beginner/intermediate/advanced>

        Job Requirements:
        - Skill: <name>, Required Level: <beginner/intermediate/advanced>

        Skill Gaps:
        - Skill: <name>, Issue: <missing or level too low (e.g., intermediate < required advanced)>

        Resume:
        {resume}

        Job Listing:
        {job_listing}
        """   
    return prompt

# Function runs by default
if __name__ == "__main__":
    resume_text = readfile(resume_filepath)
    job_listing_text = readfile(job_listing_filepath)
    prompt  = make_prompt(resume_text, job_listing_text)
    screening_result = get_completion(prompt)

    print("Resume Screening Result")
    print(screening_result)
