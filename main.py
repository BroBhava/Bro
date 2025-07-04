from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

main = FastAPI()

# Temporary storage for last received text
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

# STT endpoint - receive text from Unity
@app.post("/stt", response_model=TextOut)
async def receive_undertone(text: TextIn):
    last_text["content"] = text.content
    last_text["source"] = text.source
    print(f"Received STT (undertone): {text.content}")
    return text

# TTS endpoint - send last received text to Unity
@app.get("/tts", response_model=TextOut)
async def get_overtone():
    if last_text["content"]:
        return TextOut(**last_text)
    raise HTTPException(status_code=404, detail="No STT text received yet.")
