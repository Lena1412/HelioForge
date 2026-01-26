from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# 1. Remove repo root from sys.path if present
sys.path = [p for p in sys.path if p not in ("", str(ROOT))]

# 2. Force src/ to be first
sys.path.insert(0, str(SRC))
