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
