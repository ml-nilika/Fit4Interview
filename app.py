import streamlit as st
# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🎯 Fit4Interview", layout="centered")

from DATA.questions import ROLE_QUESTIONS
from analysis.text_analyzer import analyze_answer
from voice_input import get_voice_text
from analysis.voice_analyzer import analyze_voice
from analysis.final_scorer import calculate_final_score
from analysis.ai_feedback import generate_feedback
from analysis.performance_level import get_performance_label
from config import RECRUITER_PASSWORDS
from resume_module.parser import extract_text
from resume_module.question_generator import generate_questions
from database.db import create_table
from database.db import save_interview
from database.user_db import create_user_table, register_user, login_user
create_table()
create_user_table()
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# ================= LOGIN SYSTEM =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    load_css("styles/login.css")
else:
    load_css("styles/main.css")
if not st.session_state.logged_in:

    with st.container():
        st.markdown('<div class="login-title">Fit4Interview</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">AI Interview & Job Readiness Analyzer</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            username = st.text_input("Username", key="USer_login")
            password = st.text_input("Password", type="password",key="login_pass")

            if st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_name = username
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            st.markdown("Don't have an account?")
            if st.button("Create one"):
                st.session_state.auth_tab = "Register"
                st.rerun()

        with tab2:
            username = st.text_input("Username",key="reg_user")
            name = st.text_input("Full Name",key="reg_name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            new_password = st.text_input("Password", type="password", key="reg_pass")
            confirm = st.text_input("Confirm Password", type="password",key="reg_confirm")
            if st.button("Create Account"):
                if new_password!= confirm:
                    st.error("Passwords do not match")
                else:
                    success=register_user(username,name, gender, new_password)
                    if success:
                        st.success("Account created! Please login.")
                    else:
                        st.error("Username already exists")
            st.markdown("Already have an account?")
            if st.button("Login here"):
                st.session_state.auth_tab = "Login"
                st.rerun()

    st.stop()
st.sidebar.success(f"Logged in as {st.session_state.user_name}")
# ================= MAIN APP STARTS HERE =================
st.title("🎯Fit4Interview")
st.caption("AI-powered interview & job readiness analyzer")
st.markdown("---")

st.markdown("## 👤 Candidate Information")
candidate_name = st.session_state.user_name
st.write(f"Welcome, {candidate_name}")
st.markdown("---")
st.header("🎯 Setup Your Interview")
# Resume + JD
resume_file = st.file_uploader(
    "Upload Resume (Optional)",
    type=["pdf", "docx"]
)

jd_text = st.text_area("Paste Job Description (Optional)")
    
st.markdown("## 🎯 Select Job Role")
selected_role = st.selectbox(
    "Choose the role you are preparing for",
    list(ROLE_QUESTIONS.keys())
)
mode = st.radio(
    "Choose Interview Mode",
    ["Practice Mode", "Screening Mode"],
    horizontal=True
)
generate_btn = st.button("🚀 Generate Interview")
# ------------------ SESSION STATE ------------------


if "recruiter_dashboard" not in st.session_state:
    st.session_state.recruiter_dashboard = False

if "current_role" not in st.session_state:
    st.session_state.current_role = selected_role

if st.session_state.current_role != selected_role:
    st.session_state.current_role = selected_role
    st.session_state.q_index = 0
    st.session_state.answers = {}
    st.session_state.scores = {}
    st.session_state.voice_scores = {}
    st.session_state.voice_duration = {}
if generate_btn:

    # Personalized Interview
    if resume_file and jd_text:
        resume_text = extract_text(resume_file)

        with st.spinner("Generating personalized interview..."):
            questions = generate_questions(resume_text, jd_text)

        if questions:
            st.session_state.generated_questions = [
                {"question": q, "ideal": ""}
                for q in questions
            ]
            st.session_state.q_index = 0
            st.success("✅ Personalized Interview Ready!")

    # Role-based Interview
    else:
        st.session_state.generated_questions = ROLE_QUESTIONS[selected_role]
        st.session_state.q_index = 0
        st.success(f"✅ {selected_role} Interview Ready!")

if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "generated_questions" not in st.session_state:
    st.info("Configure your interview above and click Generate.")
    st.stop()

QUESTIONS = st.session_state.generated_questions
TOTAL_Q = len(QUESTIONS)

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "voice_duration" not in st.session_state:
    st.session_state.voice_duration = {}

if "voice_scores" not in st.session_state:
    st.session_state.voice_scores = {}

if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False


if "review_mode" not in st.session_state:
    st.session_state.review_mode = False

if "final_eval_mode" not in st.session_state:
    st.session_state.final_eval_mode = False

if "recruiter_dashboard" not in st.session_state:
    st.session_state.recruiter_dashboard = False

# ------------------ CURRENT QUESTION ------------------
if "generated_questions" in st.session_state and not st.session_state.interview_completed:
    idx = st.session_state.q_index
    current = QUESTIONS[idx]

# ------------------ PROGRESS INDICATOR ------------------
    st.caption(f"Question {idx + 1} of {TOTAL_Q}")
    st.progress((idx + 1) / TOTAL_Q)

    st.subheader("Mock Interview Question")
    st.write(f"**{current['question']}**")


    # ------------------ VOICE INPUT ------------------
    if st.button("🎤 Speak Answer"):
        with st.spinner("🎧 Listening... Please speak now"):
            spoken_text, duration = get_voice_text()

        if spoken_text:
            st.session_state[f"answer_{idx}"] = spoken_text
            st.session_state.voice_duration[idx] = duration
            st.success("✅ Voice captured successfully")
            st.rerun()
        else:
            st.warning("❌ Could not understand speech. Please try again.")
    # ------------------ ANSWER INPUT ------------------
    st.markdown("## ✍️ Answer Content (What you say)")
    st.caption("Type or speak your answer, then click Analyze for content evaluation.")

    answer = st.text_area(
        "Your Answer",
        height=180,
        placeholder="Type your answer here...",
        key=f"answer_{idx}"
    )


    # ------------------ ANALYZE BUTTON ------------------
    if mode == "Practice Mode":
        if st.button("🔍 Analyze Answer (Content + Final Score)"):
            if answer.strip() == "":
                st.warning("Please write an answer before analyzing.")
            else:
                score = analyze_answer(answer, current["ideal"])
                st.session_state.scores[st.session_state.q_index] = score
                st.session_state.answers[st.session_state.q_index] = answer
                st.session_state.score = score

    # ------------------ SMART RESULT SECTION ------------------

    if mode == "Practice Mode" and idx in st.session_state.scores:

        content_score = st.session_state.scores[idx]

        # Check if voice was used
        voice_score = None
        if idx in st.session_state.voice_duration:
            voice_score, voice_feedback = analyze_voice(
                st.session_state.answers.get(idx, ""),
                st.session_state.voice_duration[idx]
            )
            st.session_state.voice_scores[idx] = voice_score

        # Calculate final score
        if voice_score is not None:
            final_score = calculate_final_score(content_score, voice_score)
        else:
            final_score = content_score

        st.markdown("## 📊 Overall Interview Score")
        st.metric("Score", final_score)
        # ----------------Performance level------------------
        level=get_performance_label(final_score)
        st.markdown(f"### 🏷 Level: **{level}**")

        # AI Summary
        st.markdown("### 🤖 AI Performance Summary")

        with st.spinner("Analyzing performance..."):
            summary = generate_feedback(
                current["question"],
                st.session_state.answers[idx],
                current["ideal"],
                content_score,
                voice_score if voice_score is not None else 0
            )

        st.info(summary)

        # Show voice insight only if voice used
        if voice_score is not None:
            st.markdown("### 🎤 Delivery Insight")
            st.write(f"Voice Score: {voice_score}")
            if voice_score < 50:
                st.warning("Your speaking pace may need improvement.")
            else:
                st.success("Your speaking delivery was confident.")

    # ------------------ NAVIGATION ------------------

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Previous") and idx > 0:
            st.session_state.q_index -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡"):
        # 🔥 ALWAYS SAVE ANSWER (Practice + Screening)
            current_answer = st.session_state.get(f"answer_{idx}", "")

            if current_answer.strip() != "":
                st.session_state.answers[idx] = current_answer
                # ================= SAVE TO DATABASE =================
                content_score = st.session_state.scores.get(idx, 0)
                voice_score = st.session_state.voice_scores.get(idx, 0)

                if voice_score:
                    final_score = calculate_final_score(content_score, voice_score)
                else:
                    final_score = content_score

                data = {
                    "name": candidate_name,
                    "role": selected_role,
                    "question": current["question"],
                    "answer": current_answer,
                    "content": content_score if mode == "Practice Mode" else None,
                    "voice": voice_score if mode == "Practice Mode" else None,
                    "final": final_score if mode == "Practice Mode" else None,
                    "mode": mode
                }
                if f"saved_{idx}" not in st.session_state:
                    save_interview(data)
                    st.session_state[f"saved_{idx}"] = True
            # Move to next question
            if idx < TOTAL_Q - 1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.session_state.interview_completed = True
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
if st.session_state.interview_completed:

    st.markdown("## 🎉 Interview Completed")
    st.markdown("---")

    total = TOTAL_Q
    answered = len(st.session_state.answers)
    skipped = total - answered

    # ---------------- PRACTICE MODE ----------------
    if mode == "Practice Mode":

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📘 Review My Answers"):
                st.session_state.review_mode = True
                st.session_state.final_eval_mode = False

        with col2:
            if st.button("📊 Final Evaluation"):
                st.session_state.final_eval_mode = True
                st.session_state.review_mode = False
    if mode == "Screening Mode" and st.session_state.interview_completed:

        st.markdown("### 🧾 Screening Summary")

        answered = len(st.session_state.answers)
        skipped = TOTAL_Q - answered

        col1, col2 = st.columns(2)
        col1.metric("Questions Answered", answered)
        col2.metric("Questions Skipped", skipped)

        st.info("Thank you for completing the screening process.")


# ------------------ Review Mode ------------------
if st.session_state.review_mode:

    st.markdown("---")
    st.header("📘 Interview Review")

    for i, q in enumerate(QUESTIONS):
        st.subheader(f"Q{i+1}. {q['question']}")

        user_ans = st.session_state.answers.get(i, "No answer")
        score = st.session_state.scores.get(i, 0)

        st.markdown("**Your Answer:**")
        st.write(user_ans)

        st.markdown("**Ideal Answer:**")
        st.info(q["ideal"])

        st.markdown(f"**Score:** {score}")

        if score < 40:
            st.warning("Needs improvement")
        elif score < 70:
            st.info("Decent answer")
        else:
            st.success("Strong answer")

        st.markdown("---")

if st.session_state.final_eval_mode:

    st.markdown("---")
    st.header("📊 Final Performance Evaluation")

    avg_content = sum(st.session_state.scores.values()) / len(st.session_state.scores) if st.session_state.scores else 0
    avg_voice = sum(st.session_state.voice_scores.values()) / len(st.session_state.voice_scores) if st.session_state.voice_scores else 0

    overall = int(0.7 * avg_content + 0.3 * avg_voice)

    col1, col2, col3 = st.columns(3)
    col1.metric("Answered", len(st.session_state.answers))
    col2.metric("Skipped", TOTAL_Q - len(st.session_state.answers))
    col3.metric("Final Score", overall)

    st.markdown("---")

    level = get_performance_label(overall)
    st.markdown(f"### 🏷 Performance Level: **{level}**")

    if overall >= 75:
        st.success("✅ Eligible for Interview Round")
    elif overall >= 55:
        st.info("⚠ Borderline — Improve Before Real Interview")
    else:
        st.error("❌ Not Ready Yet")

    st.markdown("---")

    if st.session_state.scores:
        st.markdown("### 📈 Question-wise Performance")
        st.bar_chart(list(st.session_state.scores.values()))



# ---------------- Recruiter Login ----------------





# ---------------- Recruiter Dashboard ----------------
if st.session_state.recruiter_dashboard:

    st.markdown("---")
    st.header("👔 Recruiter Evaluation Dashboard")

    avg_content = (
        sum(st.session_state.scores.values()) / len(st.session_state.scores)
        if st.session_state.scores else 0
    )

    avg_voice = (
        sum(st.session_state.voice_scores.values()) / len(st.session_state.voice_scores)
        if st.session_state.voice_scores else 0
    )

    overall = int(0.7 * avg_content + 0.3 * avg_voice)

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Content", int(avg_content))
    col2.metric("Avg Voice", int(avg_voice))
    col3.metric("Overall Score", overall)

    st.markdown("---")

    level = get_performance_label(overall)
    st.markdown(f"### Candidate Level: **{level}**")

    if overall >= 75:
        st.success("Recommended for Interview")
    elif overall >= 55:
        st.info("Consider with caution")
    else:
        st.error("Not recommended")

    if st.session_state.scores:
        st.markdown("### 📊 Score Distribution")
        st.bar_chart(list(st.session_state.scores.values()))
    if st.button("Logout Recruiter"):
        st.session_state.recruiter_dashboard = False
        st.rerun()
