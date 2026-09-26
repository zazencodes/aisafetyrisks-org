"""aisr_kit: the only module generated scenes may import. Re-exports Manim, NumPy and the kit."""

import numpy as np
from manim import *  # noqa: F403

from aisr_kit.components import *  # noqa: F403
from aisr_kit.narrated import NarratedScene
from aisr_kit.style import *  # noqa: F403

from aisr_kit.editorial import show
