import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import langchain_core.globals as lc

# Fix LangChain runtime errors
lc.set_llm_cache(None)
lc.set_debug(False)
lc.set_verbose(False)

def evaluate_resume(jd, resume):
    """Evaluate resume vs job description using Gemini 2.5 Flash."""

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",   # ✔ confirmed supported model
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=0.15
    )

    prompt = f"""
You are an ATS-powered professional hiring system.

Analyze the resume against the job description and provide ONLY valid JSON.  
No explanation. No extra text.

---

📌 Job Description:
{jd}

📌 Resume:
{resume}

---

Return JSON in THIS EXACT format:

{{
 "fit_score": <0-100>,
 "match_level": "Poor | Average | Good | Strong | Excellent",
 "summary": "Short recruiter-style summary",
 "years_experience_estimate": "<number> years",
 "tech_match_percentage": <0-100>,
 "missing_skills": ["skill1","skill2"],
 "strengths": ["..."],
 "weaknesses": ["..."],
 "soft_skills_detected": ["communication","leadership","teamwork","adaptability","problem solving"],
 "recommended_role_level": "Intern | Junior | Mid | Senior | Lead",
 "best_fit_role": "Example: Data Analyst, Software Engineer, Cloud Engineer...",
 "skill_gap_severity": "Low | Medium | High",
 "final_recommendation": "Shortlist | Consider | Not suitable"
}}
"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"ERROR: {e}"
