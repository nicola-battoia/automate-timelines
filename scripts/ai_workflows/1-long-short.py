import os
import logging
from typing import Dict, List
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel, Field, RootModel, field_validator, model_validator


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

# --------------------------------------------------------------
# Step 1: Define the data models
# --------------------------------------------------------------


def _timestamp_to_seconds(ts: str) -> float:
    """
    Convert 'HH:MM:SS,mmm' to total seconds as float.
    Example: '01:23:48,320' -> 5028.320
    """
    try:
        hh, mm, rest = ts.split(":")
        ss, ms = rest.split(",")
        return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0
    except Exception as exc:
        raise ValueError(f"Invalid timestamp format: {ts!r}") from exc


class ClipSelection(BaseModel):
    """Clip segment to extract from a source media file"""

    start: str = Field(
        description="Start time of the clip in 'HH:MM:SS,mmm' format "
        "(YouTube transcript style)",
        examples=["01:23:48,320"],
    )
    end: str = Field(
        description="End time of the clip in 'HH:MM:SS,mmm' format "
        "(YouTube transcript style)",
        examples=["01:23:53,639"],
    )

    @field_validator("start", "end")
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        # Will raise if invalid; we don't store the parsed value here,
        # just validate and keep the original string.
        _timestamp_to_seconds(v)
        return v

    @model_validator(mode="after")
    def check_order(self) -> "ClipSelection":
        if _timestamp_to_seconds(self.end) <= _timestamp_to_seconds(self.start):
            raise ValueError("end must be strictly after start")
        return self


class ClipsList(BaseModel):
    """List of clip selections"""

    clips: List[ClipSelection] = Field(description="List of clip selections")


class SourceMedia(BaseModel):
    """Source media file definition with its clip selections"""

    file_path: str = Field(description="Absolute path to the source media file")
    rate: int = Field(description="Frame rate (fps) of the source media")
    clips: List[ClipSelection] = Field(
        description="Clip segments to pull from this source media"
    )


class SourceMediaList(RootModel[List[SourceMedia]]):
    """Collection of source media entries to process"""

    root: List[SourceMedia]


# --------------------------------------------------------------
# Step 2: Define prompts
# --------------------------------------------------------------

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

srt_path = Path(
    "/Users/nico/hack/gitHub/automate-timelines/data/transcripts/youtube-subtitles-example.srt"
)

# Flatten SRT entries into a single transcript string
lines = srt_path.read_text(encoding="utf-8").splitlines()
spoken = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    spoken.append(line)
transcript = " ".join(spoken)

print(transcript)


# --------------------------------------------------------------
# Step 2: Call the model
# --------------------------------------------------------------

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "system", "content": ORCHESTRATOR_PROMPT}],
    response_format=ClipsList,
)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------
