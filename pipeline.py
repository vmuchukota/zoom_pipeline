import subprocess
from faster_whisper import WhisperModel

# extract audio from the zoom recording

print("step 1: extracting audio from the zoom recording...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-i", "zoom_recording.mp4",
    "-vn",
    "-acodec", "mp3",
    "audio.mp3"
])

print("Audio has been extracted successfully.")

print("step 2: loading the whisper model...")

# loading the whisper tool 
model = WhisperModel("base")

print("step 3: transcribing the audio...")

segments, info = model.transcribe("audio.mp3")

print("step 4: saving the transcript...")

# save the transcript 
with open("transcript.txt", "w") as f:
    for segment in segments:
        line = f"{segment.start:.2f} --> {segment.end:.2f}: {segment.text}\n"
        print(line)
        f.write(line)

print("Transcription has been saved")