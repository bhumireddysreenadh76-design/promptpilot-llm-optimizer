from fastapi import FastAPI
from pydantic import BaseModel
from src.optimizer import optimize_prompt

app = FastAPI(title="Prompt Optimizer")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/optimize")
async def optimize(request: PromptRequest):
    """
    Return a single concise, rephrased prompt optimized for token efficiency.
    """
    optimized = optimize_prompt(request.prompt)
    return {"optimized_prompt": optimized}
