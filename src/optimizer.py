def optimize_prompt(prompt: str) -> str:
    """
    Cleans and optimizes a user prompt.
    - Strips whitespace
    - Removes filler words
    """
    filler_words = ["please", "kindly", "actually", "basically"]
    words = [w for w in prompt.split() if w.lower() not in filler_words]
    return "Optimized: " + " ".join(words)
