"""
Utility functions for timeline automation workflows.
"""


def timestamp_to_seconds(ts: str) -> float:
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
