"""Entry program for news-image-20261124 (standard library only).

The image is drawn at build time by build_image.py and shipped in this
repository as entry.png; this program copies it to the grader's output
directory, mirroring the kit starter's main.ts.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
