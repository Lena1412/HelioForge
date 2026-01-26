# src/cosmoview/cli.py
from __future__ import annotations

import argparse

from .app import run


def main() -> None:
    parser = argparse.ArgumentParser(prog="cosmoview", description="Visualize helioforge simulations.")
    parser.add_argument("--mode", choices=["solar", "random"], default="solar")
    parser.add_argument("--width", type=int, default=1100)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--fps", type=int, default=60)
    args = parser.parse_args()

    run(width=args.width, height=args.height, fps_limit=args.fps, mode=args.mode)


if __name__ == "__main__":
    main()
