#!/usr/bin/env python
#
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the OpenTimelineIO project

"""
Generate a timeline with video and audio tracks from a JSON configuration.
Each source file gets a video track and a corresponding audio track.
Multiple clips can be defined per source, and they will be placed sequentially.
Each A/V pair is logically "linked" via shared metadata.
"""

import argparse
import json

import opentimelineio as otio


def parse_args():
    """Parse arguments out of sys.argv"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "config",
        type=str,
        help="Path to JSON configuration file with source files and clip ranges",
    )
    parser.add_argument(
        "filepath",
        type=str,
        help=(
            "Path to write timeline file to. Example: /var/tmp/example.otio "
            "or c:\\example.otio"
        ),
    )
    return parser.parse_args()


def load_config(config_path):
    """Load and validate JSON configuration file."""
    with open(config_path, 'r') as f:
        config = json.load(f)

    if 'sources' not in config:
        raise ValueError("JSON config must contain 'sources' array")

    for i, source in enumerate(config['sources']):
        if 'file' not in source:
            raise ValueError(f"Source {i} missing 'file' field")
        if 'clips' not in source:
            raise ValueError(f"Source {i} missing 'clips' array")

        for j, clip in enumerate(source['clips']):
            if 'start' not in clip:
                raise ValueError(f"Source {i}, clip {j} missing 'start' field")
            if 'duration' not in clip:
                raise ValueError(f"Source {i}, clip {j} missing 'duration' field")
            if 'rate' not in clip:
                raise ValueError(f"Source {i}, clip {j} missing 'rate' field")

    return config


def main():
    args = parse_args()

    # ------------------------------------------------------------------
    # Load configuration
    # ------------------------------------------------------------------
    config = load_config(args.config)
    sources = config['sources']

    # ------------------------------------------------------------------
    # Build the timeline & tracks
    # ------------------------------------------------------------------
    tl = otio.schema.Timeline(name="Multi-source A/V linked timeline")

    # Create video and audio tracks dynamically for each source
    video_tracks = []
    audio_tracks = []

    for i in range(len(sources)):
        v_track = otio.schema.Track(
            name=f"V{i + 1}",
            kind=otio.schema.TrackKind.Video,
        )
        a_track = otio.schema.Track(
            name=f"A{i + 1}",
            kind=otio.schema.TrackKind.Audio,
        )
        video_tracks.append(v_track)
        audio_tracks.append(a_track)

        # Append to timeline
        tl.tracks.append(v_track)
        tl.tracks.append(a_track)

    # ------------------------------------------------------------------
    # Build clip pairs: for each source, create multiple clips based
    # on the time ranges specified in the config. Clips are placed
    # sequentially in their respective tracks.
    # ------------------------------------------------------------------
    clip_counter = 0

    for source_idx, source in enumerate(sources):
        fname = source['file']
        clip_specs = source['clips']

        for clip_idx, clip_spec in enumerate(clip_specs):
            # Create time range from clip spec
            source_range = otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(
                    clip_spec['start'],
                    clip_spec['rate'],
                ),
                duration=otio.opentime.RationalTime(
                    clip_spec['duration'],
                    clip_spec['rate'],
                ),
            )

            # Shared media reference for video + audio
            media_ref = otio.schema.ExternalReference(
                target_url=fname,
            )

            # Use a shared id to mark this A/V pair as belonging together.
            clip_counter += 1
            link_group_id = f"pair_{clip_counter}"

            video_clip = otio.schema.Clip(
                name=f"V{source_idx + 1}_Clip{clip_idx + 1}",
                media_reference=media_ref,
                source_range=source_range,
                metadata={
                    "linked_group": link_group_id,
                    "role": "video",
                },
            )

            audio_clip = otio.schema.Clip(
                name=f"A{source_idx + 1}_Clip{clip_idx + 1}",
                media_reference=media_ref,
                source_range=source_range,
                metadata={
                    "linked_group": link_group_id,
                    "role": "audio",
                },
            )

            # Append clips sequentially to their respective tracks
            video_tracks[source_idx].append(video_clip)
            audio_tracks[source_idx].append(audio_clip)

    # ------------------------------------------------------------------
    # Write the file to disk
    # ------------------------------------------------------------------
    otio.adapters.write_to_file(tl, args.filepath)
    print(f"Timeline written to: {args.filepath}")
    print(f"Created {len(sources)} track pairs with {clip_counter} total clip pairs")


if __name__ == "__main__":
    main()
