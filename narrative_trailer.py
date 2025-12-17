"""
Narrative 90 seconds trailer. multi step process
"""

# ----------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------

# Standard library
import os
import logging

# Third-party
from dotenv import load_dotenv
from openai import OpenAI
import opentimelineio as otio
from google import genai
from google.genai import types

# Local imports
from config import (
    AI_CLIPS_PATH,
    CONTEXT,
    FPS,
    GOOGLE_MODEL_NAME,
    MEDIA_PATHS,
    OPENAI_MODEL_NAME,
    OUTPUT_OTIO_PATH,
    TRANSCRIPT_PATH,
)
from models.data_models import SourceMedia, ClipsList
from create_timelines.otio_builder import PerMediaTimelineBuilder
from ai_prompts.cleanup_1 import CLEANUP_TRANCRIPT


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
# MAIN EXECUTION
# ----------------------------------------------------------------------

# Step 1: Load environment and transcript
logger.info("Loading environment variables")
load_dotenv()
logger.info(f"Loading transcript from {TRANSCRIPT_PATH}")
transcript = TRANSCRIPT_PATH.read_text(encoding="utf-8")
logger.info(f"Transcript loaded ({len(transcript)} characters)")

# ----------------------------------------------------------------------
# OPENAI EXECUTION
# ----------------------------------------------------------------------

# Initialize OpenAI openai_client
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Call AI model to extract clips
# logger.info(f"Calling {OPENAI_MODEL_NAME} to extract clips")
# completion = openai_client.beta.chat.completions.parse(
#     model=OPENAI_MODEL_NAME,
#     messages=[
#         {
#             "role": "system",
#             "content": ORCHESTRATOR_PROMPT.format(
#                 transcript=transcript, context=CONTEXT
#             ),
#         }
#     ],
#     response_format=ClipsList,
# )

# cleaned_transcript = completion.choices[0].message.parsed
# logger.info(f"Extracted {len(cleaned_transcript.clips)} clips from transcript")
# print(cleaned_transcript)


# ----------------------------------------------------------------------
# GOOGLE GEMINI EXECUTION
# ----------------------------------------------------------------------

logger.info("Initializing Google GenAI client")
google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Log before processing transcript with the Google client generate call
logger.info(f"Cleaning up the transcript with {GOOGLE_MODEL_NAME}")

# use this with thinking models like gemini 3-pro
# response = google_client.models.generate_content(
#     model=GOOGLE_MODEL_NAME,
#     contents=ORCHESTRATOR_PROMPT.format(transcript=transcript, context=CONTEXT),
#     config=types.GenerateContentConfig(
#         thinking_config=types.ThinkingConfig(thinking_level="low"),
#         response_mime_type="application/json",
#         response_json_schema=ClipsList.model_json_schema(),
#     ),
# )

# clean up the transcript to only the meaningful parts

response_cleaned_transcript = google_client.models.generate_content(
    model=GOOGLE_MODEL_NAME,
    contents=CLEANUP_TRANCRIPT.format(transcript=transcript, context=CONTEXT),
    config={
        "response_mime_type": "application/json",
        "response_json_schema": ClipsList.model_json_schema(),
    },
)


cleaned_transcript = ClipsList.model_validate_json(response_cleaned_transcript.text)

logger.info(f"Extracted {len(cleaned_transcript.clips)} clips from transcript")

logger.info(f"Clips Selected: {cleaned_transcript.model_dump_json(indent=2)}")

# Persist selected clips to file for downstream use
AI_CLIPS_PATH.parent.mkdir(parents=True, exist_ok=True)
AI_CLIPS_PATH.write_text(cleaned_transcript.model_dump_json(indent=2), encoding="utf-8")
logger.info(f"Wrote clip selections to {AI_CLIPS_PATH}")


# Step 3: Convert timestamp-based clips to frame-based clips
logger.info(f"Converting clips to frame ranges at {FPS} fps")
builder_clips = [clip.to_clip_spec(FPS) for clip in cleaned_transcript.clips]

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
