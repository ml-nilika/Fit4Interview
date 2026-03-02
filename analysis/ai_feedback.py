
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)


def generate_feedback(question, user_answer, ideal_answer, content_score, voice_score):
    messages = [
        {
            "role": "system",
            "content": "You are a professional AI interview evaluator."
        },
        {
            "role": "user",
            "content": f"""
Content Score: {content_score}
Voice Score: {voice_score}

Question: {question}
Candidate Answer: {user_answer}
Ideal Answer: {ideal_answer}

Give professional interview feedback in 4-5 concise sentences.
Mention strengths and improvement areas.
"""
        }
    ]

    result = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=messages,
        max_tokens=200,
        temperature=0.3,
    )

    return result.choices[0].message["content"]