import openai
from dotenv import load_dotenv
import os

# === Load API Key from .env ===
load_dotenv()

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

# === Build your prompt
with open("assets/output/reddit_script.txt", "r", encoding="utf-8") as f:
    original_text = f.read()

prompt = (
    "You're a helpful assistant that edits Reddit-style content for TTS narration.\n"
    "Your task is to:\n"
    "1. Remove all but one comment. Pick the most vivid or emotionally rich one.\n"
    "2. Rewrite that comment as a natural monologue optimized for TTS, (with the title coming first, comment second, separated by two newlines) and removing all references to Reddit.\n"
    "Output ONLY the cleaned and rewritten comment with no extra commentary, no titles, no notes, no explanations.\n\n"
    f"{original_text}\n\n"
    "Final monologue:"
)

# === Chat Completion with new OpenAI API
response = client.chat.completions.create(
    model="llama3-8b-8192", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=512,
    top_p=0.9,
)

edited_text = response.choices[0].message.content.strip()

# Save output to assets/input/tts_input.txt
with open("assets/input/tts_input.txt", "w", encoding="utf-8") as f:
    f.write(edited_text)

print("[INFO] Edited version saved to assets/input/tts_input.txt")
