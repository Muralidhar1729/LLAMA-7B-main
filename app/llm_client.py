from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def chat(messages, temperature=0.1, max_tokens=512, model=None):
    model = model or OPENAI_MODEL
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content
