#!/usr/bin/env python
#
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the OpenTimelineIO project

"""
Generate a simple timeline with 2 video tracks and 2 audio tracks.
Each video track has a corresponding audio track, and each A/V pair
is logically "linked" via shared metadata and ranges.
"""

import argparse

import opentimelineio as otio

# For simplicity, use two clips so we get 2 A/V pairs:
#   pair 1 -> V1 + A1
#   pair 2 -> V2 + A2
FILE_LIST = [
    (
        "/Users/nico/YT/automation-tests/recording/nicola.mp4",
        otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, 24),
            duration=otio.opentime.RationalTime(800, 24),
        ),
    ),
    (
        "/Users/nico/YT/automation-tests/recording/hwei.mp4",
        otio.opentime.TimeRange(
            # 1 hour in @ 24 fps
            start_time=otio.opentime.RationalTime(0, 24),
            duration=otio.opentime.RationalTime(800, 24),
        ),
    ),
]


def parse_args():
    """Parse arguments out of sys.argv"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "filepath",
        type=str,
        help=(
            "Path to write example file to. Example: /var/tmp/example.otio "
            "or c:\\example.otio"
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # ------------------------------------------------------------------
    # Build the timeline & tracks
    # ------------------------------------------------------------------
    tl = otio.schema.Timeline(name="Example A/V linked timeline")

    # Create 2 video tracks and 2 audio tracks
    v1 = otio.schema.Track(
        name="V1",
        kind=otio.schema.TrackKind.Video,
    )
    v2 = otio.schema.Track(
        name="V2",
        kind=otio.schema.TrackKind.Video,
    )
    a1 = otio.schema.Track(
        name="A1",
        kind=otio.schema.TrackKind.Audio,
    )
    a2 = otio.schema.Track(
        name="A2",
        kind=otio.schema.TrackKind.Audio,
    )

    # The Timeline.tracks is a Stack; append tracks in the order you want
    tl.tracks.append(v1)
    tl.tracks.append(v2)
    tl.tracks.append(a1)
    tl.tracks.append(a2)

    video_tracks = [v1, v2]
    audio_tracks = [a1, a2]

    # ------------------------------------------------------------------
    # Build clip pairs: for each media entry, create a video clip and
    # a matching audio clip with the same media reference and source_range.
    # ------------------------------------------------------------------
    for i, (fname, available_range) in enumerate(FILE_LIST):
        # Safety: only as many FILE_LIST items as we have track pairs
        if i >= len(video_tracks):
            break

        # Shared media reference for video + audio
        media_ref = otio.schema.ExternalReference(
            target_url=fname,
            available_range=available_range,
        )

        # Trim the source a bit, like in the original example
        source_range = otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(
                available_range.start_time.value + 10,
                available_range.start_time.rate,
            ),
            duration=otio.opentime.RationalTime(
                available_range.duration.value - 20,
                available_range.duration.rate,
            ),
        )

        # Use a shared id to mark this A/V pair as belonging together.
        # OTIO itself does not interpret this; it's for your tools or
        # any NLE adapter that chooses to use it.
        link_group_id = f"pair_{i + 1}"

        video_clip = otio.schema.Clip(
            name=f"VClip{i + 1}",
            media_reference=media_ref,
            source_range=source_range,
            metadata={
                "linked_group": link_group_id,
                "role": "video",
            },
        )

        audio_clip = otio.schema.Clip(
            name=f"AClip{i + 1}",
            media_reference=media_ref,
            source_range=source_range,
            metadata={
                "linked_group": link_group_id,
                "role": "audio",
            },
        )

        # Append to corresponding video/audio tracks
        video_tracks[i].append(video_clip)
        audio_tracks[i].append(audio_clip)

    # ------------------------------------------------------------------
    # Write the file to disk
    # ------------------------------------------------------------------
    otio.adapters.write_to_file(tl, args.filepath)


if __name__ == "__main__":
    main()
