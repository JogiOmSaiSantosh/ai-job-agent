import streamlit as st
import fitz
import requests
import pandas as pd

st.title("AI Job Agent")

uploaded_file = st.file_uploader(
    "Upload Your Resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    document = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

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

    candidate_skills = []

    for skill in skills_database:

        if skill.lower() in resume_text.lower():
            candidate_skills.append(skill)

    st.subheader("Skills Found")

    st.write(candidate_skills)

    url = "https://remotive.com/api/remote-jobs"

    try:

        response = requests.get(url, timeout=10)

        data = response.json()

        jobs = data["jobs"]

    except Exception as e:

        st.error("Internet/API Error")

        st.write(e)

        jobs = []

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

    df = pd.DataFrame(matched_jobs)

    st.subheader("Matching Jobs")

    st.dataframe(df)

    csv = df.to_csv(index=False)

    st.download_button(

        label="Download CSV",

        data=csv,

        file_name="matched_jobs.csv",

        mime="text/csv"

    )