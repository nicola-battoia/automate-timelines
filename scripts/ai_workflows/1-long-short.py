"""
Long-to-Short Clip Extraction Workflow

This script analyzes a podcast transcript and uses AI to extract interesting clips
for creating a short-form intro video. It converts timestamp-based clips to frame
ranges and builds an OTIO timeline.
"""

# ----------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------

# Standard library
import os
import logging
from pathlib import Path
from typing import List

# Third-party
from openai import OpenAI
import opentimelineio as otio

# Local imports
from models.data_models import ClipSpec, SourceMedia, ClipsList
from create_timelines.otio_builder import PerMediaTimelineBuilder


# ----------------------------------------------------------------------
# LOGGING CONFIGURATION
# ----------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------

# AI Model Configuration
MODEL_NAME = "gpt-5-mini"

# Input Paths
TRANSCRIPT_PATH = Path(
    "/Users/nico/hack/gitHub/automate-timelines/data/transcripts/youtube-subtitles-example.srt"
)

# Video Settings
FPS = 24  # Frames per second

# Media Files
MEDIA_PATHS = [
    "/Users/nico/YT/automation-tests/recording/nicola.mp4",
    "/Users/nico/YT/automation-tests/recording/hwei.mp4",
]

# Output Path
OUTPUT_OTIO_PATH = Path(
    "/Users/nico/hack/gitHub/automate-timelines/data/timelines/per_media_tracks_gpt_5_mini.otio"
)


# ----------------------------------------------------------------------
# AI PROMPT
# ----------------------------------------------------------------------

ORCHESTRATOR_PROMPT = """
Analyze this podcast interview transcript and extract clips from the whole episode to create an interesting intro of roughly two minutes.

Return your response in this format:

# Clips List
List of clip selections in the format of HH:MM:SS,mmm
## Clip 1
- Start: 00:00:00,000
- End: 00:00:00,000
## Clip 2
- Start: 00:00:00,000
- End: 00:00:00,000
## Clip 3
- Start: 00:00:00,000
- End: 00:00:00,000
...

Transcript: {transcript}
"""


# ----------------------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------------------

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Load and process transcript
logger.info(f"Loading transcript from {TRANSCRIPT_PATH}")
lines = TRANSCRIPT_PATH.read_text(encoding="utf-8").splitlines()
spoken = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    spoken.append(line)
transcript = " ".join(spoken)

# Step 2: Call AI model to extract clips
logger.info(f"Calling {MODEL_NAME} to extract clips")
completion = client.beta.chat.completions.parse(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": ORCHESTRATOR_PROMPT.format(transcript=transcript)}
    ],
    response_format=ClipsList,
)

clips_list = completion.choices[0].message.parsed
logger.info(f"Extracted {len(clips_list.clips)} clips from transcript")

# Step 3: Convert timestamp-based clips to frame-based clips
logger.info(f"Converting clips to frame ranges at {FPS} fps")
builder_clips = [clip.to_clip_spec(FPS) for clip in clips_list.clips]

# Step 4: Create source media list with clips for each media file
source_media_list = [
    SourceMedia(
        file_path=path,
        rate=FPS,
        clips=builder_clips,
    )
    for path in MEDIA_PATHS
]

# Step 5: Build OTIO timeline
logger.info("Building OTIO timeline")
builder = PerMediaTimelineBuilder()
timeline = builder.build_timeline(source_media_list)

# Step 6: Write timeline to file
logger.info(f"Writing timeline to {OUTPUT_OTIO_PATH}")
otio.adapters.write_to_file(timeline, OUTPUT_OTIO_PATH)

logger.info("Workflow complete!")
