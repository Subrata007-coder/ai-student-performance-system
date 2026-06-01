import os
from fastapi import FastAPI, Body
import google.generativeai as genai

# 1. Initialize the Web Server
app = FastAPI()

# 2. Setup Gemini (The AI Brain)
# We will provide the API Key during deployment for security
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def home():
    return {"message": "Agent is online!"}

@app.post("/process")
async def run_agent(payload: dict = Body(...)):
    # This captures the text you send to the agent
    user_text = payload.get("text", "No text provided")

    # The Task: A simple text summarizer
    prompt = f"Summarize this briefly: {user_text}"
    
    response = model.generate_content(prompt)
    
    return {
        "input": user_text,
        "summary": response.text
    }