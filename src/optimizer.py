import re

def optimize_prompt(prompt: str) -> str:
    """
    Aggressively rephrases a user prompt into short, clear instructions.
    - Removes filler words
    - Shortens verbose phrases
    - Rewrites into imperative style
    """

    # Normalize whitespace
    prompt = prompt.strip()
    prompt = re.sub(r"\s+", " ", prompt)

    # Remove filler words
    filler_words = ["please", "kindly", "actually", "basically", "just", "really", "very", "if you don’t mind"]
    words = [w for w in prompt.split() if w.lower() not in filler_words]
    cleaned = " ".join(words)

    # Replace verbose phrases
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

    # Force imperative style: start with a verb
    # Example: "Could you explain importance..." → "Explain importance..."
    cleaned = re.sub(r"^(could|can|would)\s+you\s+", "Explain ", cleaned, flags=re.IGNORECASE)

    # Limit length
    limited = " ".join(cleaned.split()[:20])

    return limited
