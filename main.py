import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field

app = FastAPI()

# Read API key from environment variable
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

last_text = {
    "content": None,
    "source": None
}

# Input model with alias for "text-to-translate"
class TextIn(BaseModel):
    content: str = Field(..., alias="text-to-translate")
    source: str = "undertone"

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True  # Optional: lets FastAPI display alias in docs

# Output model remains the same
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
    return TextOut(content=text.content, source=text.source)

@app.get("/tts", response_model=TextOut, dependencies=[Depends(verify_api_key)])
async def get_overtone():
    if last_text["content"]:
        return TextOut(**last_text)
    raise HTTPException(status_code=404, detail="No STT text received yet.")
