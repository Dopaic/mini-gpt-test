import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# 从环境变量读取 OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# 允许任何前端域名访问
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
    """
    接收前端发来的 message，调用 GPT，返回回复。
    """
    completion = client.chat.completions.create(
        # 可以换参 gpt-4o / gpt-4.1 / gpt-5.1 
        model="gpt-5.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req.message},
        ],
    )

    reply_text = completion.choices[0].message.content
    return ChatResponse(reply=reply_text)
