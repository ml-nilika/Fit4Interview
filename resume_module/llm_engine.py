import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}


def call_llm(prompt):

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 700,
        "temperature": 0.7
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    print("RAW:", response.text[:500])

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception:
        return ""