from __future__ import annotations

"""helioforge.export

Small helpers for exporting helioforge objects to JSON.

This module currently supports SolarSystem serialization via its `to_dict()` method.
"""

import json

from .system import SolarSystem


def load_json(path: str) -> SolarSystem:
    """Load a SolarSystem from a JSON file previously created via `save_json()`.

    Args:
        path: Path to a JSON file created from `SolarSystem.to_dict()`.

    Returns:
        Parsed SolarSystem instance.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return SolarSystem.from_dict(data)

def to_json(system: SolarSystem, *, indent: int = 2) -> str:
    """Serialize a SolarSystem to a JSON string.

    Args:
        system: The SolarSystem instance to serialize.
        indent: Indentation level passed to `json.dumps` for readability.

    Returns:
        A JSON-formatted string representing the SolarSystem.
    """
    return json.dumps(system.to_dict(), indent=indent)


def save_json(system: SolarSystem, path: str, *, indent: int = 2) -> None:
    """Serialize a SolarSystem to JSON and write it to disk.

    Args:
        system: The SolarSystem instance to serialize.
        path: Output file path.
        indent: Indentation level passed to `json.dumps` for readability.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_json(system, indent=indent))
