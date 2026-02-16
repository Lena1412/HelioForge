# commandline usage
# one of the last things besides docs and examples to be added
# it was something I wanted to try even before starting this project in my work

# src/cosmoview/cli.py
from __future__ import annotations

"""cosmoview.cli

Command-line entry point for the CosmoView pygame viewer.

This module parses CLI arguments and forwards them to `cosmoview.app.run`.
"""

import argparse

from .app import run


def main() -> None:
    """Parse CLI arguments and run the viewer."""
    parser = argparse.ArgumentParser(
        prog="cosmoview", description="Visualize helioforge simulations."
    )
    parser.add_argument("--mode", choices=["solar", "random"], default="solar")
    parser.add_argument("--width", type=int, default=1100)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument(
        "--json", type=str, default=None, help="Load SolarSystem from JSON export."
    )
    args = parser.parse_args()

    if args.json:
        from helioforge.export import load_json

        system = load_json(args.json)
        run(
            width=args.width,
            height=args.height,
            fps_limit=args.fps,
            mode=args.mode,
            system=system,
        )
    else:
        run(width=args.width, height=args.height, fps_limit=args.fps, mode=args.mode)


if __name__ == "__main__":
    main()
