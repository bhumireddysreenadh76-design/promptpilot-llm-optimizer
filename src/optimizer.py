import re

def optimize_prompt(prompt: str) -> str:
    """
    Cleans and optimizes a user prompt for token efficiency.
    - Strips whitespace
    - Removes filler words
    - Shortens verbose phrases
    - Collapses multiple spaces
    - Limits token count (e.g., 30 words max)
    """

    # Step 1: Trim whitespace
    prompt = prompt.strip()

    # Step 2: Remove filler words
    filler_words = ["please", "kindly", "actually", "basically", "just", "really", "very"]
    words = [w for w in prompt.split() if w.lower() not in filler_words]

    # Step 3: Collapse multiple spaces
    cleaned = re.sub(r"\s+", " ", " ".join(words))

    # Step 4: Shorten common verbose phrases
    replacements = {
        "in order to": "to",
        "as soon as possible": "quickly",
        "a large number of": "many",
        "due to the fact that": "because"
    }
    for long, short in replacements.items():
        cleaned = cleaned.replace(long, short)

    # Step 5: Limit token count (example: 30 words max)
    limited = " ".join(cleaned.split()[:30])

    return limited

import re

def optimize_prompt(prompt: str) -> str:
    """
    Rephrases a user prompt into a short, clear, token-efficient version.
    - Removes filler words
    - Shortens verbose phrases
    - Rewrites into direct, simple language
    """

    # Step 1: Normalize whitespace
    prompt = prompt.strip()
    prompt = re.sub(r"\s+", " ", prompt)

    # Step 2: Remove filler words
    filler_words = ["please", "kindly", "actually", "basically", "just", "really", "very", "if you don’t mind"]
    words = [w for w in prompt.split() if w.lower() not in filler_words]
    cleaned = " ".join(words)

    # Step 3: Replace verbose phrases with concise ones
    replacements = {
        "in order to": "to",
        "as soon as possible": "quickly",
        "a large number of": "many",
        "due to the fact that": "because",
        "provide me with": "give",
        "could you": "explain",
        "help me understand": "explain"
    }
    for long, short in replacements.items():
        cleaned = cleaned.replace(long, short)

    # Step 4: Rephrase into imperative style (remove politeness, keep action)
    # Example: "Could you explain importance of incident management" → "Explain importance of incident management"
    cleaned = re.sub(r"^(could|can|would)\s+you\s+", "Explain ", cleaned, flags=re.IGNORECASE)

    # Step 5: Limit to ~25 words
    limited = " ".join(cleaned.split()[:25])

    return limited

