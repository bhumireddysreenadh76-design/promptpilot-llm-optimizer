from fastapi import FastAPI
from pydantic import BaseModel
from src.optimizer import optimize_prompt, optimize_suggestions

app = FastAPI(title="Prompt Optimizer")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/optimize")
async def optimize(request: PromptRequest):
    optimized = optimize_prompt(request.prompt)
    return {"optimized_prompt": optimized}

@app.post("/optimize_options")
async def optimize_options(request: PromptRequest):
    """
    Returns multiple rewrite options (short, balanced, formal) for UI suggestions.
    """
    options = optimize_suggestions(request.prompt)
    return {"options": options}
