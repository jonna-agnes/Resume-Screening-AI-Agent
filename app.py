import streamlit as st
import json
from utils.extract import extract_text
from utils.similarity import build_vector_db, similarity_score
from utils.ai_eval import evaluate_resume
from utils.database import save_ranked_results

st.set_page_config(page_title="AI Resume Screening Agent", layout="wide")

st.title("🤖 AI Resume Screening Agent")
st.markdown("Upload a job description and candidate resumes. The system will rank, evaluate, and store results automatically.")

# -------------------- INPUT SECTION -------------------------
jd_file = st.file_uploader("📄 Upload Job Description (PDF)", type=["pdf"])
resume_files = st.file_uploader("👤 Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

# -------------------- RUN BUTTON ----------------------------
if st.button("🚀 Run Screening"):

    if not jd_file or not resume_files:
        st.error("❌ Please upload both job description AND resumes.")
        st.stop()

    st.info("📌 Extracting text... ⏳")
    jd_text = extract_text(jd_file)

    resumes = [{"filename": f.name, "text": extract_text(f)} for f in resume_files]
    st.success("✔ Text extraction complete!")

    st.info("🔍 Matching resumes to job description...")
    vectorstore = build_vector_db(jd_text, resumes)

    st.info("🧠 Evaluating resumes with AI...")

    results = []
    for r in resumes:
        sim = similarity_score(vectorstore, r["text"])
        analysis = evaluate_resume(jd_text, r["text"])
        results.append({
            "filename": r["filename"],
            "similarity": sim,
            "analysis": analysis,
        })

    # ---------------- Sort Results ----------------
    def extract_score(x):
        try:
            clean = x["analysis"].replace("```json", "").replace("```", "").strip()
            return int(json.loads(clean)["fit_score"])
        except:
            return 0

    results = sorted(results, key=extract_score, reverse=True)

    # ---------------- Format for Database ----------------
    formatted_results = []
    for r in results:
        clean = r["analysis"].replace("```json","").replace("```","").strip()
        data = json.loads(clean)
        status = (
            "Shortlist" if data['fit_score'] >= 80
            else "Consider" if data['fit_score'] >= 60
            else "Reject"
        )
        formatted_results.append({
            "filename": r["filename"],
            "fit_score": data["fit_score"],
            "match_level": data["match_level"],
            "best_role": data["best_fit_role"],
            "status": status,
            "similarity": round(r["similarity"],2)
        })

    save_ranked_results(formatted_results)

    # Store once — no repeated API calls later
    st.session_state["results"] = results
    st.success("🎉 Screening Complete!")


# -------------------- UI DISPLAY SECTION ---------------------
if "results" in st.session_state:

    results = st.session_state["results"]

    st.subheader("📊 Candidate Ranking (Auto-Sorted)")
    ranking_table = []

    for idx, r in enumerate(results, start=1):
        clean = r["analysis"].replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

        ranking_table.append([
            idx,
            r["filename"],
            data["fit_score"],
            data["match_level"],
            data["best_fit_role"],
            round(r["similarity"], 2)
        ])

    import pandas as pd
    df = pd.DataFrame(ranking_table, columns=["Rank", "Candidate", "Fit Score", "Match Level", "Role Fit", "Similarity"])
    st.dataframe(df, use_container_width=True)

    st.write("---")

    # ---------------- Candidate Selection ----------------
    st.subheader("📌 View Individual Report")

    selected_name = st.selectbox(
        "Select a candidate:",
        [r["filename"] for r in results]
    )

    selected = next(r for r in results if r["filename"] == selected_name)

    clean = selected["analysis"].replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)

    # ---------------- Candidate Report ----------------
    st.markdown(f"## 🏆 Candidate: **{selected_name}**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Fit Score", f"{data['fit_score']}%")
    c2.metric("Tech Match", f"{data['tech_match_percentage']}%")
    c3.metric("Similarity", round(selected["similarity"],2))

    st.markdown(f"### 📝 Summary\n> {data['summary']}")

    left, right = st.columns(2)

    with left:
        st.markdown("### ✅ Strengths")
        for s in data["strengths"]:
            st.write("•", s)

    with right:
        st.markdown("### ⚠ Weaknesses")
        for w in data["weaknesses"]:
            st.write("•", w)

    st.markdown("### ❌ Missing Skills")
    st.write(", ".join(data["missing_skills"]))

    st.markdown("### 💡 Soft Skills Identified")
    st.write(", ".join(data["soft_skills_detected"]))

    st.markdown(f"### 📌 Final Recommendation\n🎯 **{data['final_recommendation']}**")
