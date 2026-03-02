from resume_module.llm_engine import call_llm
import re


def generate_questions(resume_text, jd_text):

    prompt = f"""
You are an expert interviewer.

Generate 20 professional interview questions based on the candidate resume and job description.

Resume:
{resume_text[:800]}

Job Description:
{jd_text[:800]}

Return ONLY numbered questions.
"""

    text = call_llm(prompt)

    print("LLM TEXT:", text)

    questions = []

    # -------- Extract numbered questions --------
    matches = re.findall(r"\d+\.\s*(.+)", text)

    for q in matches:
        q = q.strip()
        if len(q) > 20:
            questions.append(q)

    return questions[:20]