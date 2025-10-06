# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# Initialize FastAPI app
app = FastAPI(title="AI Dictionary Backend")

# Allow frontend (GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your site if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up OpenAI
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")
client = OpenAI(api_key=OPENAI_KEY)

@app.get("/")
async def root():
    return {"message": "✅ AI Dictionary Backend Running Successfully!"}

@app.get("/define")
async def define(word: str = Query(..., description="Word to define")):
    """
    Fetch a concise meaning and example sentence for a word using OpenAI.
    """
    try:
        prompt = f"Define the word '{word}' in a simple and short way, and give one example sentence."

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        text = response.output[0].content[0].text.strip()

        # Try to split the AI response into meaning and example
        meaning = ""
        example = ""
        parts = text.split("Example:")
        if len(parts) == 2:
            meaning = parts[0].strip()
            example = parts[1].strip()
        else:
            meaning = text

        return {
            "word": word,
            "meaning": meaning,
            "example": example,
        }

    except Exception as e:
        return {"error": str(e)}
