import fitz
import requests
import pandas as pd

# -----------------------------
# READ RESUME PDF
# -----------------------------

pdf_path = "resumes/santosh_resume.pdf"

document = fitz.open(pdf_path)

resume_text = ""

for page in document:
    resume_text += page.get_text()

# -----------------------------
# SKILLS DATABASE
# -----------------------------

skills_database = [

    "Python",
    "SQL",
    "AWS",
    "Power BI",
    "Excel",
    "Machine Learning",
    "Pandas",
    "NumPy",
    "Java",
    "HTML",
    "CSS"

]

# -----------------------------
# EXTRACT SKILLS
# -----------------------------

candidate_skills = []

for skill in skills_database:

    if skill.lower() in resume_text.lower():
        candidate_skills.append(skill)

print("\nCandidate Skills:\n")

for skill in candidate_skills:
    print(skill)

# -----------------------------
# FETCH REAL JOBS
# -----------------------------

url = "https://remotive.com/api/remote-jobs"

try:

    response = requests.get(url, timeout=10)

    data = response.json()

    jobs = data["jobs"]

except Exception as e:

    print("\nInternet/API Error")
    print(e)

    jobs = []

# -----------------------------
# MATCH JOBS
# -----------------------------

matched_jobs = []

for job in jobs[:100]:

    title = job["title"]

    description = job["description"]

    matched_skills = 0

    for skill in candidate_skills:

        if (
            skill.lower() in title.lower()
            or skill.lower() in description.lower()
        ):

            matched_skills += 1

    if len(candidate_skills) > 0:

        match_percentage = (
            matched_skills / len(candidate_skills)
        ) * 100

    else:
        match_percentage = 0

    if match_percentage > 0:

        matched_jobs.append({

            "Job Title": title,
            "Company": job["company_name"],
            "Location": job["candidate_required_location"],
            "Match Percentage": round(match_percentage, 2),
            "Job URL": job["url"]

        })

# -----------------------------
# SAVE CSV
# -----------------------------

df = pd.DataFrame(matched_jobs)

df.to_csv("matched_jobs.csv", index=False)

# -----------------------------
# SHOW RESULTS
# -----------------------------

print("\nMATCHING JOBS:\n")

print(df)

print("\nAI Job Agent Completed Successfully")