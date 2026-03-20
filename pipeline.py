import subprocess
import os 
from openai import OpenAI
from faster_whisper import WhisperModel

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()
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

# step 5
print("step 5: summarizing the transcript...")

with open("transcript.txt", "r") as f:
    transcript = f.read()

if client: 
    try: 
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You analyze meeting transcripts and return structured outputs."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze the following meeting transcript and return:

1. Summary (short paragraph)
2. Key Points (bullet points)
3. Action Items (clear tasks if mentioned)

Transcript:
{transcript}
"""
                }
            ]   # ✅ THIS BRACKET WAS MISSING
        )

        analysis = response.choices[0].message.content

    except Exception as e: 
        print("Error during summary, using a fallback summary.")
        analysis = None
    
else: 
    print("No OpenAI API key found, using a fallback summary.")
    analysis = None

analysis = None

#fallback 
if analysis is None: 
    analysis = """
Summary: The meeting discusses a Zoom pipeline for processing recordings into transcripts

Key Points:
- Audio is extracted using FFmpeg
- Whisper model is used for transcription
- LLMs can be used for summarization

Action Items: 
- Improve task extraction
- Explore better models
"""

print("Analysis is complete.\n")


#step 6: save analysis 
print("step 6: saving the analysis...")
with open("analysis.txt", "w") as f:
    f.write(analysis)

print("Analysis has been saved successfully.")