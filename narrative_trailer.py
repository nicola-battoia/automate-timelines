"""
Narrative 90 seconds trailer. multi step process
"""

# ----------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------

# Standard library
import os
import logging
from pathlib import Path


# Third-party
from dotenv import load_dotenv
import opentimelineio as otio
from google import genai

# Local imports
from config import (
    CONTEXT,
    FPS,
    GOOGLE_MODEL_NAME,
    MEDIA_PATHS,
    TRANSCRIPT_PATH,
)
from models.data_models import SourceMedia, ClipsList
from create_timelines.otio_builder import PerMediaTimelineBuilder
from ai_prompts.cleanup_1 import CLEANUP_TRANSCRIPT
from utils.genai import generate_clips_step


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
# GOOGLE GEMINI EXECUTION
# ----------------------------------------------------------------------

logger.info("Initializing Google GenAI client")
google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

CLEANED_TRANSCRIPT_PATH = Path("data/processing/cleaned_transcript.json")
HOOK_CANDIDATES_PATH = Path("data/processing/hook_candidates.json")
LIFE_LESSONS_PATH = Path("data/processing/life_lessons.json")
EMOTIONS_PATH = Path("data/processing/emotions.json")
CLIFFHANGER_PATH = Path("data/processing/cliffhanger_candidates.json")
NARRATIVE_TRAILER_PATH = Path("data/processing/narrative_trailer.json")

# Step 1: clean up the transcript to only the meaningful parts
cleaned_transcript = generate_clips_step(
    client=google_client,
    model_name=GOOGLE_MODEL_NAME,
    prompt=CLEANUP_TRANSCRIPT.format(transcript=transcript, context=CONTEXT),
    start_log=f"Cleaning up the transcript with {GOOGLE_MODEL_NAME}",
    extract_label="clips from transcript",
    detail_label="Clips selected",
    output_path=CLEANED_TRANSCRIPT_PATH,
    logger=logger,
)

from ai_prompts.hook_finder_2 import HOOK_FINDER

hook_candidates = generate_clips_step(
    client=google_client,
    model_name=GOOGLE_MODEL_NAME,
    prompt=HOOK_FINDER.format(transcript=cleaned_transcript.clips),
    start_log="Selecting hooks",
    extract_label="potential hooks",
    detail_label="Hook candidates",
    output_path=HOOK_CANDIDATES_PATH,
    logger=logger,
)

from ai_prompts.life_lesson_finder_3 import LIFE_LESSON_FINDER

life_lessons = generate_clips_step(
    client=google_client,
    model_name=GOOGLE_MODEL_NAME,
    prompt=LIFE_LESSON_FINDER.format(transcript=cleaned_transcript.clips),
    start_log="Selecting life lessons",
    extract_label="life lessons",
    detail_label="Life lessons",
    output_path=LIFE_LESSONS_PATH,
    logger=logger,
)

# Step 4: emotions
from ai_prompts.emotions_finder_4 import EMOTIONS_FINDER

emotions = generate_clips_step(
    client=google_client,
    model_name=GOOGLE_MODEL_NAME,
    prompt=EMOTIONS_FINDER.format(transcript=transcript),
    start_log="Analyzing emotional moments",
    extract_label="emotion clips",
    detail_label="Emotion candidates",
    output_path=EMOTIONS_PATH,
    logger=logger,
)

# Step 5: cliffhanger
from ai_prompts.cliffhanger_finder_5 import CLIFFHANGER_FINDER

cliffhanger_candidates = generate_clips_step(
    client=google_client,
    model_name=GOOGLE_MODEL_NAME,
    prompt=CLIFFHANGER_FINDER.format(transcript=transcript),
    start_log="Finding cliffhangers",
    extract_label="cliffhanger candidates",
    detail_label="Cliffhanger candidates",
    output_path=CLIFFHANGER_PATH,
    logger=logger,
)

# Step 6: narrative trailer
from ai_prompts.narrative_together_6 import NARRATIVE_TOGETHER

narrative_trailer = generate_clips_step(
    client=google_client,
    model_name=GOOGLE_MODEL_NAME,
    prompt=NARRATIVE_TOGETHER.format(
        hooks=hook_candidates,
        lessons=life_lessons,
        emotional_moments=emotions,
        cliffhangers=cliffhanger_candidates,
    ),
    start_log="Building narrative trailer",
    extract_label="clips for the trailer",
    detail_label="Narrative trailer",
    output_path=NARRATIVE_TRAILER_PATH,
    logger=logger,
)

# ----------------------------------------------------------------------
# TIMELINE BUILDING
# ----------------------------------------------------------------------

logger.info(f"Converting clips to frame ranges at {FPS} fps")
builder_clips = [clip.to_clip_spec(FPS) for clip in narrative_trailer.clips]

# Create source media list with clips for each media file
source_media_list = [
    SourceMedia(
        file_path=path,
        rate=FPS,
        clips=builder_clips,
    )
    for path in MEDIA_PATHS
]

# Build OTIO timeline
logger.info("Building OTIO timeline")
builder = PerMediaTimelineBuilder()
timeline = builder.build_timeline(source_media_list)

NARRATIVE_TRAILER_OTIO_PATH = Path("data/processing/narrative_trailer.otio")


# Write timeline to file
logger.info(f"Writing timeline to {NARRATIVE_TRAILER_OTIO_PATH}")
otio.adapters.write_to_file(timeline, NARRATIVE_TRAILER_OTIO_PATH)

logger.info("Workflow complete!")
