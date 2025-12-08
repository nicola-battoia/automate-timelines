#!/usr/bin/env python
#
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the OpenTimelineIO project

"""
Generate a timeline where:
- You provide a list of source media files.
- For each source media, you provide a list of clip in/out times.
- The script creates 1 video track + 1 audio track per source media.
- It then adds all the specified clips for that media to those tracks.
"""

import opentimelineio as otio
from pydantic import BaseModel
from typing import List, Optional


class ClipSpec(BaseModel):
    start: int
    duration: int


class SourceMedia(BaseModel):
    file_path: str
    rate: int
    clips: List[ClipSpec]


# ----------------------------------------------------------------------
# INPUT CONFIGURATION
#
# All time values (start, duration) are in FRAMES at the given "rate".
#
# For each entry:
#   file_path: path to the media file (video with embedded audio, or whatever Resolve sees)
#   rate:      frames per second for that media
#   clips:     list of { "start": <frame>, "duration": <frames> }
#
# Example:
#   - nicola.mp4 with two clips
#   - hwei.mp4 with one clip
# ----------------------------------------------------------------------


class PerMediaTimelineBuilder:
    def __init__(self, timeline_name: str = "Per-media A/V tracks with clip lists"):
        self.timeline_name = timeline_name

    def build_available_range_from_clips(
        self,
        clips: List[ClipSpec],
        rate: int,
    ) -> Optional[otio.opentime.TimeRange]:
        """
        Derive an available_range that covers all specified clips for a media.

        - min_start = earliest clip start
        - max_end   = latest (start + duration)
        """
        if not clips:
            return None

        starts = [c.start for c in clips]
        ends = [c.start + c.duration for c in clips]

        min_start = min(starts)
        max_end = max(ends)

        return otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(min_start, rate),
            duration=otio.opentime.RationalTime(max_end - min_start, rate),
        )

    def build_timeline(
        self, source_media_list: List[SourceMedia]
    ) -> otio.schema.Timeline:
        tl = otio.schema.Timeline(name=self.timeline_name)

        # For each source media, create one video track + one audio track
        for media_index, media_spec in enumerate(source_media_list, start=1):
            file_path = media_spec.file_path
            rate = media_spec.rate
            clip_specs = media_spec.clips

            # Create one V + one A track for this media
            v_track = otio.schema.Track(
                name=f"V{media_index}",
                kind=otio.schema.TrackKind.Video,
            )
            a_track = otio.schema.Track(
                name=f"A{media_index}",
                kind=otio.schema.TrackKind.Audio,
            )

            # Append tracks to the timeline's track stack in the order you want
            tl.tracks.append(v_track)
            tl.tracks.append(a_track)

            # Derive an available_range that covers all requested clips
            available_range = self.build_available_range_from_clips(clip_specs, rate)

            # Shared media reference for all clips on these tracks
            media_ref = otio.schema.ExternalReference(
                target_url=file_path,
                available_range=available_range,
            )

            # ------------------------------------------------------------------
            # For each clip spec, create video + audio clip with same source_range
            # ------------------------------------------------------------------
            for clip_index, clip_def in enumerate(clip_specs, start=1):
                source_range = otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(clip_def.start, rate),
                    duration=otio.opentime.RationalTime(clip_def.duration, rate),
                )

                # Shared id to logically link V + A for this segment
                link_group_id = f"media{media_index}_clip{clip_index}"

                video_clip = otio.schema.Clip(
                    name=f"V{media_index}_Clip{clip_index}",
                    media_reference=media_ref,
                    source_range=source_range,
                    metadata={
                        "linked_group": link_group_id,
                        "role": "video",
                    },
                )

                audio_clip = otio.schema.Clip(
                    name=f"A{media_index}_Clip{clip_index}",
                    media_reference=media_ref,
                    source_range=source_range,
                    metadata={
                        "linked_group": link_group_id,
                        "role": "audio",
                    },
                )

                # Append clips sequentially on their respective tracks
                v_track.append(video_clip)
                a_track.append(audio_clip)

        return tl
