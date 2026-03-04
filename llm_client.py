import os
from groq import Groq
from prompts import build_prompt
from tenacity import retry, wait_random_exponential, stop_after_attempt

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable not set")
        _client = Groq(api_key=api_key, timeout=30.0)
    return _client

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
def analyze_text_with_groq(text: str) -> str:
    client = get_client()

    prompt = build_prompt(text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500
    )

    return response.choices[0].message.content
    