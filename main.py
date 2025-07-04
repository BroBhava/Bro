import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel

app = FastAPI()

# Read API key from environment variable
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

last_text = {
    "content": None,
    "source": None
}

class TextIn(BaseModel):
    content: str
    source: str = "undertone"

class TextOut(BaseModel):
    content: str
    source: str

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/stt", response_model=TextOut, dependencies=[Depends(verify_api_key)])
async def receive_undertone(text: TextIn):
    last_text["content"] = text.content
    last_text["source"] = text.source
    print(f"Received STT (undertone): {text.content}")
    return text

@app.get("/tts", response_model=TextOut, dependencies=[Depends(verify_api_key)])
async def get_overtone():
    if last_text["content"]:
        return TextOut(**last_text)
    raise HTTPException(status_code=404, detail="No STT text received yet.")
