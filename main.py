import sys
import subprocess

scripts = [
    "scrape_reddit.py",
    "story_cleanup.py",
    "tts.py",
    "create_video.py", 
    "publish.py"
]

python_executable = sys.executable

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run([python_executable, script])  # <-- no capture_output, interactive mode
    if result.returncode != 0:
        print(f"Error running {script}")
        break
