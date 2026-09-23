import os
from fastapi import FastAPI
from pydantic import BaseModel
from strands import Agent
from strands.models import BedrockModel
app = FastAPI(title="support-agent")
class ChatIn(BaseModel):
 message: str
@app.get("/health")
def health():
 return {"status": "ok"}
@app.post("/chat")
def chat(body: ChatIn):
 # A new Agent per request. A shared Agent keeps conversation history,
 # so different users would see each other's messages.
 agent = Agent(model=BedrockModel(model_id=os.environ["MODEL_ID"]),
 system_prompt="You are a helpful support agent.",
 callback_handler=None)
 return {"answer": str(agent(body.message))}
