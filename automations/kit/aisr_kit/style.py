"""Visual identity shared by every explainer. Colors mirror the website's dark palette."""

from pathlib import Path

import manimpango
from manim import NORMAL, Text, config

for font_file in (Path(__file__).resolve().parents[1] / "fonts").glob("*.ttf"):
    if not manimpango.register_font(str(font_file)):
        raise RuntimeError(f"could not register font {font_file}")

BG = "#111418"
PANEL = "#1A1E24"
INK = "#E9E7E1"
SOFT = "#C9C6BF"
MUTED = "#8E949C"
FAINT = "#3A3F47"

BLUE = "#7FA7D6"
TEAL = "#5FB3A1"
AMBER = "#D9A647"
ROSE = "#D9826A"
VIOLET = "#A98BD4"
SAND = "#B89A8E"
GRAY = "#9FA3AA"

SANS = "IBM Plex Sans"
SERIF = "Charter"
MONO = "IBM Plex Mono"

MIN_FONT_SIZE = 20

KIND_COLORS = {
    "observed_result": TEAL,
    "theoretical_result": BLUE,
    "author_interpretation": AMBER,
    "hypothesis": VIOLET,
    "threat_model": ROSE,
    "future_scenario": SAND,
    "speculation": GRAY,
    "limitation": ROSE,
    "method": MUTED,
    "definition": MUTED,
    "background": MUTED,
}

KIND_LABELS = {
    "observed_result": "Observed result",
    "theoretical_result": "Theoretical result",
    "author_interpretation": "Authors' interpretation",
    "hypothesis": "Hypothesis",
    "threat_model": "Threat model",
    "future_scenario": "Future scenario",
    "speculation": "Speculation",
    "limitation": "Stated limitation",
    "method": "Method",
    "definition": "Definition",
    "background": "Background",
}

config.background_color = BG
Text.set_default(font=SANS, color=INK, weight=NORMAL)
