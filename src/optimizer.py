import re

def optimize_prompt(prompt: str) -> str:
    prompt = prompt.strip()
    prompt = re.sub(r"\s+", " ", prompt)

    filler_words = ["please", "kindly", "actually", "basically", "just", "really", "very", "if you don’t mind"]
    words = [w for w in prompt.split() if w.lower() not in filler_words]
    cleaned = " ".join(words)

    replacements = {
        "in order to": "to",
        "as soon as possible": "quickly",
        "a large number of": "many",
        "due to the fact that": "because",
        "provide me with": "give",
        "could you": "explain",
        "help me understand": "explain",
        "i need it urgently": "urgent"
    }
    for long, short in replacements.items():
        cleaned = cleaned.replace(long, short)

    cleaned = re.sub(r"^(could|can|would)\s+you\s+", "Explain ", cleaned, flags=re.IGNORECASE)

    limited = " ".join(cleaned.split()[:20])
    return limited
