from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)
import os

# === CONSTANTS ===
VIDEO_PATH = r"C:\Users\lukas\Github Projects\reels-bot\assets\input\gameplay.mp4"
AUDIO_PATH = r"C:\Users\lukas\Github Projects\reels-bot\assets\output\output.mp3"
SUBTITLE_PATH = r"C:\Users\lukas\Github Projects\reels-bot\assets\output\subtitles.txt"
OUTPUT_VIDEO_PATH = r"C:\Users\lukas\Github Projects\reels-bot\assets\output\final_video.mp4"

# Video output size (portrait 9:16)
OUTPUT_RESOLUTION = (1080, 1920)

def parse_subtitles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    subtitles = []
    i = 0
    while i < len(lines):
        if "-->" in lines[i]:
            times = lines[i].split("-->")
            start = float(times[0].strip())
            end = float(times[1].strip())
            text = lines[i+1].strip()
            subtitles.append((start, end, text))
            i += 2
        else:
            i += 1
    return subtitles

def assemble_video():
    print("[INFO] Loading video and audio...")
    video_clip = VideoFileClip(VIDEO_PATH)
    audio_clip = AudioFileClip(AUDIO_PATH)

    print("[INFO] Converting video to portrait format...")
    # Resize & crop to 9:16 portrait
    video_clip = video_clip.resize(width=OUTPUT_RESOLUTION[0])
    video_clip = video_clip.crop(
        y_center=video_clip.h / 2,
        width=OUTPUT_RESOLUTION[0],
        height=OUTPUT_RESOLUTION[1]
    )

    print("[INFO] Adding subtitles...")
    subtitles = parse_subtitles(SUBTITLE_PATH)

    subtitle_clips = []
    for start, end, text in subtitles:
        txt_clip = TextClip(
            text,
            fontsize=60,
            font="Arial-Bold",
            color="white",
            stroke_color="black",
            stroke_width=3,
            size=(OUTPUT_RESOLUTION[0] - 100, None),
            method="caption"
        ).set_position(("center", OUTPUT_RESOLUTION[1] - 250)).set_start(start).set_end(end)
        subtitle_clips.append(txt_clip)

    print("[INFO] Combining everything...")
    final_clip = CompositeVideoClip(
        [video_clip] + subtitle_clips
    ).set_audio(audio_clip)

    final_clip = final_clip.set_duration(audio_clip.duration)

    print("[INFO] Exporting final video...")
    final_clip.write_videofile(
        OUTPUT_VIDEO_PATH,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )

    print(f"[SUCCESS] Video exported to {OUTPUT_VIDEO_PATH}")

if __name__ == "__main__":
    assemble_video()
