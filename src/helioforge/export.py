from __future__ import annotations

import json

from .system import SolarSystem


def to_json(system: SolarSystem, *, indent: int = 2) -> str:
    """Serialize a SolarSystem to JSON."""
    return json.dumps(system.to_dict(), indent=indent)


def save_json(system: SolarSystem, path: str, *, indent: int = 2) -> None:
    """Save SolarSystem JSON to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_json(system, indent=indent))
