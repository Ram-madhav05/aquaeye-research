"""
AquaEye - Shrimp Vision, Detection, and Spatial Awareness System.
"""

from .config import Config
from .tracker import ShrimpGroupTracker, TrackedShrimp, ShrimpGroup

__all__ = [
    "Config",
    "ShrimpGroupTracker",
    "TrackedShrimp",
    "ShrimpGroup",
]

try:
    from .dataset_parser import DatasetParser
    from .image_enhancement import enhance_underwater_frame, CLAHEEnhancer
    __all__.extend(["DatasetParser", "enhance_underwater_frame", "CLAHEEnhancer"])
except ImportError:
    pass
