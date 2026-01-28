from cosmoview.app import run

"""
Purpose: Programmatic CosmoView launch

Shows:
- using the viewer without CLI
"""

run(
    width=1200,
    height=800,
    fps_limit=60,
    mode="solar",
)
