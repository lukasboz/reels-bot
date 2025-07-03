import whisper

# Load model (first time will download ~70MB)
model = whisper.load_model("base")

# Transcribe audio
result = model.transcribe("Recording.m4a")
print(result["text"])