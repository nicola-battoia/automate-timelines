"""Example configuration for the clip extraction workflow.

Copy this file to `config.py` and update the path values for your environment.
Specifically, replace the placeholder strings with absolute paths to your media
files. Relative paths (e.g., transcripts and outputs under `data/`) can stay as-is
or be changed if your layout differs.
"""

from pathlib import Path

# AI Model Configuration
OPENAI_MODEL_NAME = "gpt-5.1"
GOOGLE_MODEL_NAME = "gemini-2.5-flash"
# gemini-2.5-flash
# gemini-3-pro-preview

# Input Paths
# Change to the transcript filename you placed in data/transcripts
TRANSCRIPT_FILE_NAME = "example_transcript.txt"
TRANSCRIPT_PATH = Path(f"data/transcripts/{TRANSCRIPT_FILE_NAME}")

# Context for prompt
# Replace with context relevant to your transcript and video
example_context = "This is a podcast interview between Nicola (the host) and Hwei (the guest). Hwei is a data scientist, AI engineer, and freelance coach. In the interview, she shares her approach to building with AI, reflecting both on her professional experience and her personal journey of growth as she struggled to find the right path for herself. Hwei explains how she now helps others navigate the challenges of starting out as freelancers, sharing the tools and strategies she uses to coach people. The interview has an informal, conversational style between two friends."

CONTEXT = example_context


# Video Settings
FPS = 24  # Frames per second; adjust to match your footage

# Media Files (replace these placeholders with your absolute video paths)
MEDIA_PATHS = [
    "insert here the path to your video file #1.mp4",
    "insert here the path to your video file #2.mp4",
]

# Output Paths
# Change to the timeline name you want to create
TIMELINE_FILENAME = "example_timeline"
OUTPUT_OTIO_PATH = Path(f"data/timelines/{TIMELINE_FILENAME}.otio")
AI_CLIPS_PATH = Path(f"data/ai_selected_clips/{TIMELINE_FILENAME}.json")
