from fastapi import FastAPI
from pydantic import BaseModel
from src.optimizer import optimize_prompt

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/optimize")
async def optimize(request: PromptRequest):
    optimized = optimize_prompt(request.prompt)
    return {"optimized_prompt": optimized}
import re

def optimize_prompt(prompt: str) -> str:
    """
    Cleans and optimizes a user prompt for token efficiency.
    - Strips whitespace
    - Removes filler words
    - Shortens long phrases
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
