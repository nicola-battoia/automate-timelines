"""
Pydantic data models for timeline automation workflows.

This module contains all the data classes used for:
- Defining clip specifications and source media
- Processing timestamps and frame ranges
- Validating clip selections
"""

from typing import List
from pydantic import BaseModel, Field, RootModel, field_validator, model_validator

from utils.utils import timestamp_to_seconds


class ClipSpec(BaseModel):
    """Represents a single clip segment in frames."""

    start: int
    duration: int


class SourceMedia(BaseModel):
    """
    Represents a single source media item:
    - file_path: path to the media file
    - rate: frames per second (fps)
    - clips: list of clip specs for this media
    """

    file_path: str
    rate: int
    clips: List[ClipSpec]


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
    transcript_text: str = Field(
        description="Exact transcript text from the transcript",
    )
    notes: str = Field(
        description="Brief note about why you choose this segment",
    )

    @field_validator("start", "end")
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        # Will raise if invalid; we don't store the parsed value here,
        # just validate and keep the original string.
        timestamp_to_seconds(v)
        return v

    @model_validator(mode="after")
    def check_order(self) -> "ClipSelection":
        if timestamp_to_seconds(self.end) <= timestamp_to_seconds(self.start):
            raise ValueError("end must be strictly after start")
        return self

    def to_clip_spec(self, fps: int) -> ClipSpec:
        """Convert timestamp-based selection to frame-based clip spec.

        Args:
            fps: Frame rate (frames per second)

        Returns:
            ClipSpec with start frame and duration in frames
        """
        start_seconds = timestamp_to_seconds(self.start)
        end_seconds = timestamp_to_seconds(self.end)

        start_frame = int(round(start_seconds * fps))
        end_frame = int(round(end_seconds * fps))
        duration_frames = end_frame - start_frame

        return ClipSpec(start=start_frame, duration=duration_frames)


class ClipsList(BaseModel):
    """List of clip selections"""

    clips: List[ClipSelection] = Field(description="List of clip selections")
