def optimize_prompt(prompt: str) -> str:
    """
    Cleans and optimizes a user prompt.
    - Strips whitespace
    - Removes filler words
    - Keeps it concise
    """
    filler_words = ["please", "kindly", "actually", "basically", "just"]
    words = [w for w in prompt.split() if w.lower() not in filler_words]
    return " ".join(words)
