import os
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment. Set it in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

def complete(messages: list[Dict[str, str]], **kwargs: Any) -> str:
    """
    Thin wrapper around OpenAI chat completions.
    Returns the assistant's message content as a string.
    """
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=kwargs.get("temperature", 0.5),
        max_tokens=kwargs.get("max_tokens", 300),
    )
    return resp.choices[0].message.content.strip()