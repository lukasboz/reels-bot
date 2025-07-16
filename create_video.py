from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, vfx
from moviepy.video.fx import Resize, Crop
from moviepy.video.tools.subtitles import SubtitlesClip, file_to_subtitles
from moviepy.audio.fx import *
from moviepy.audio.AudioClip import *
from datetime import datetime
import os, random, pysrt


# === Paths ===
VIDEO_PATH = r"assets\input\gameplay.mp4"
OUTPUT_PATH = r"assets\output\gameplay_portrait.mp4"
AUDIO_PATH = r"assets\input\audio.mp3"
SUBTITLE_PATH = r"assets\input\subtitles.srt"
OUTPUT_DIR = r"assets\output"
MUSIC_DIR = r"assets\input\music"

def get_random_music_path():
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith('.mp3')]
    if not music_files:
        raise FileNotFoundError(f"No .mp3 files found in {MUSIC_DIR}")
    return os.path.join(MUSIC_DIR, random.choice(music_files))

def generate_subtitle_clips(sub_path, video_size):
    subs = pysrt.open(sub_path)
    clips = []
    for sub in subs:
        txt = sub.text.replace('\n', ' ')  # Flatten multiline subtitles
        start = sub.start.ordinal / 1000  # Convert ms to sec
        end = sub.end.ordinal / 1000

        txt_clip = TextClip(
            text=txt,
            font_size=50,
            color='white',
            method='label'
        ).with_position(('center', 'bottom')).with_start(start).with_end(end)

        clips.append(txt_clip)
    return clips

def convert_to_portrait(input_path, output_path):
    print("[INFO] Loading video and audio...")
    
    # Load and validate audio
    audio = AudioFileClip(AUDIO_PATH).subclipped(0)  # Force reload
    
    background_music_path = get_random_music_path()
    background_music = AudioFileClip(background_music_path).subclipped(0, audio.duration)
    print(f"[INFO] Using background music: {background_music_path}")

    background_music = background_music.with_effects([MultiplyVolume(0.05)])

    final_audio = CompositeAudioClip([audio, background_music])

    if audio.duration <= 0:
        raise ValueError("Audio file has no duration (corrupted or silent?)")

    video = VideoFileClip(input_path)

    # Validate video length vs trim range
    if video.duration < 2 + audio.duration:
        raise ValueError(f"Video is {video.duration:.2f}s long, but need {2 + audio.duration:.2f}s")

    # Trim and attach audio
    video = video.subclipped(2, 2 + final_audio.duration)
    video = video.with_audio(final_audio)

    # Resize and crop
    video = video.with_effects([vfx.Resize(height=1920)])
    video = Crop(x1=1166.6, y1=0, x2=2246.6, y2=1920).apply(video)

    #SUBTITLING
    # Generate subtitle clips
    subtitle_clip = SubtitlesClip(
        subtitles=file_to_subtitles(SUBTITLE_PATH),
        make_textclip=lambda txt: TextClip(
            text=txt,
            font_size=72,
            color='white',
            stroke_color='black',
            stroke_width=2,
            text_align='center',
            method='caption',  # Handles multi-line subtitles
            size=(video.size[0] - 100, 200)  # Wrap text within video width
        )
    )

    # Compose final video
    video = CompositeVideoClip([video, subtitle_clip.with_position(('center','center'))])


    print(f"[INFO] Exporting cropped video to {output_path}...")

    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="libmp3lame",
        preset="ultrafast",
        fps=video.fps,
        audio=True,
        logger='bar'
    )

    print("[SUCCESS] Portrait video saved successfully!")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    convert_to_portrait(VIDEO_PATH, OUTPUT_PATH)