"""Utilities for working with GenAI responses in the narrative workflow."""

from pathlib import Path
import logging
from typing import Type

from models.data_models import ClipsList


def generate_clips_step(
    *,
    client,
    model_name: str,
    prompt: str,
    start_log: str,
    extract_label: str,
    detail_label: str,
    output_path: Path,
    logger: logging.Logger,
    schema: Type[ClipsList] = ClipsList,
) -> ClipsList:
    """
    Run a GenAI content generation call, log key details, and persist the JSON response.
    """
    logger.info(start_log)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": schema.model_json_schema(),
        },
    )

    result = schema.model_validate_json(response.text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Extracted {len(result.clips)} {extract_label}")
    logger.info(f"{detail_label}: {result.model_dump_json(indent=2)}")
    output_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    logger.info(f"Wrote clip selections to {output_path}")
    return result
