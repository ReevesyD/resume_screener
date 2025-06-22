import os
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv

# Set variables
resume_filepath = "resume.txt"
job_listing_filepath = "job_listing.txt"

# Load API key from .env
load_dotenv()

# Function that reads text from a file
def readfile(filepath):
    with open(filepath, "r") as file:
        return file.read()

# Function that writes content to a file
def writefile(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

# Makes the API call to open AI
def get_completion(prompt):
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": prompt}])
    print(response)
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
    if screening_result:
        print("API Call Success")

    output_name = "screening_result_" + datetime.now().strftime("%d-%m_%H-%M-%S") + ".txt"

    writefile(output_name, screening_result)

    print(f"File written to {output_name}")