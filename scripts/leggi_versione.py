#!/usr/bin/env python3
"""Stampa la versione di FotoFacile: la pipeline la passa a Inno Setup (/DVersione=…)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fotofacile  # noqa: E402

print(fotofacile.__version__)
