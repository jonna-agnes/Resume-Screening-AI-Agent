AI Resume Screening Agent

This project is an intelligent resume evaluation system that screens, ranks, and analyzes resumes automatically based on a provided job description. It functions like a lightweight Applicant Tracking System (ATS), using semantic similarity and AI-powered reasoning to determine how well each candidate fits the role.

What the System Does

A user uploads a job description.

One or multiple resumes are uploaded.

The system extracts text from both the job description and resumes.

It generates semantic matching scores using embeddings to understand how closely each resume aligns with the role.

An AI model (Gemini) evaluates each resume and generates:

A fit score

Strengths and weaknesses

Missing skills

Recommended matching role

Final hiring recommendation

Candidates are ranked automatically.

Results are saved into Google Sheets to build a clean, always-updated leaderboard.

The dashboard shows final ranked results, and the user can click a name to view a detailed breakdown — without reprocessing.

Technology Used

AI Model: Gemini API

Frameworks: Streamlit, LangChain

Document processing: PyPDF2

Vector similarity: FAISS / Chroma (depending on configuration)

Backend storage: Google Sheets (via gspread and service account)

State handling and UI: Streamlit session state

This combination provides a fast interface, meaningful evaluation, storage for history, and a structured hiring workflow.

How It Works Internally

The job description and each resume are converted into embeddings—numerical vector representations of meaning.

A similarity score is calculated, not by keyword matching, but by semantic relevance.

The AI model processes the resume and job description together and generates a structured JSON evaluation.

The highest scoring resumes appear at the top.

Results are stored and updated in a shared sheet, acting as a lightweight ATS database.

Setup Instructions

Clone or download the project.

Create a virtual environment and install the required dependencies using the included requirements file.

Generate a Google Service Account, enable Google Sheets and Drive API, and download the credentials file named service_account.json.

Create a new Google Sheet, name it something like Resume_Screening_DB, and share it with the service account email.

Set your Gemini API key as an environment variable.

Run the project using:

streamlit run app.py

Once launched, upload files and the system will take over.

Why This Project Matters

Traditional resume screening is time-consuming and subjective. This system automates the early stages of hiring by giving:

Consistent evaluation

Immediate ranking

Clear insights into strengths, weaknesses, and skill gaps

A record of candidate performance stored for future review

It doesn’t replace human decision-making — it accelerates it.

Future Improvements

Exporting reports as downloadable PDF summaries

Automated emailing for shortlisted candidates

Visual analytics (skill heatmaps, comparative scoring)

Authentication to support teams and multi-user environments
