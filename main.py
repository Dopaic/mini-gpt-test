import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# 新 SDK 必须使用这种写法
client = OpenAI()  # 从环境变量 OPENAI_API_KEY 自动读取

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def root():
    return {"status": "ok", "message": "GPT backend is running."}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req.message},
        ],
    )

    reply_text = completion.choices[0].message.content
    return ChatResponse(reply=reply_text)
