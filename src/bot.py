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
import openai

def call_llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
