"""Un pays qui s’enrichit enrichit-il ses actionnaires ?"""

__version__ = "1.0.0"

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".cache" / "matplotlib"))
