"""
Configuration and parameter defaults for AquaEye pipeline.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple, List

# Base project root (one level up from src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_VIDEOS_DIR = DATA_DIR / "raw_videos"
PROCESSED_VIDEOS_DIR = DATA_DIR / "processed_videos"
METADATA_DIR = DATA_DIR / "metadata"

# Models paths
MODELS_DIR = BASE_DIR / "models"
YOLO_BASELINE_WEIGHTS = MODELS_DIR / "yolov8n.pt"
AQUAEYE_BEST_WEIGHTS = MODELS_DIR / "aquaeye_best.pt"

# Metadata CSV paths
DEPTH_ESTIMATION_CSV = METADATA_DIR / "depth_estimation.csv"
LIGHT_REFLECTION_CSV = METADATA_DIR / "light_reflection.csv"
MULTISCALE_TILING_CSV = METADATA_DIR / "multiscale_image_tiling.csv"
SENSORY_ENHANCEMENT_CSV = METADATA_DIR / "sensory_enhancement.csv"
SPATIAL_AWARENESS_CSV = METADATA_DIR / "spatial_awareness.csv"


@dataclass
class Config:
    """Global configuration settings for video processing and clustering."""
    
    # Execution & Device
    device: str = "cpu"  # "cpu", "cuda", or "0"
    num_workers: int = 4
    
    # Model configuration
    model_weights: Path = AQUAEYE_BEST_WEIGHTS
    conf_threshold: float = 0.25
    iou_threshold: float = 0.45
    target_class_ids: List[int] = field(default_factory=lambda: [0])  # Shrimp class or generic object class
    
    # Image enhancement defaults (fallback when dynamic metadata is unavailable)
    clahe_clip_limit: float = 2.5
    clahe_tile_grid_size: Tuple[int, int] = (8, 8)
    denoise_h: float = 4.0
    lab_l_boost: float = 1.10
    gamma_correction: float = 0.95
    enable_enhancement: bool = True
    
    # Clustering defaults (DBSCAN)
    dbscan_eps: float = 65.0           # Spatial distance threshold in pixels
    dbscan_min_samples: int = 4        # Minimum shrimp to constitute a cluster/swarm
    
    # Video export properties
    output_codec: str = "mp4v"
    export_fps: float = 30.0
    overlay_stats: bool = True
    draw_cluster_hulls: bool = True
    
    # Color palette for distinct cluster visualization (BGR format)
    cluster_colors: List[Tuple[int, int, int]] = field(default_factory=lambda: [
        (255, 99, 71),    # Tomato / Orange-Red
        (50, 205, 50),    # Lime Green
        (30, 144, 255),   # Dodger Blue
        (238, 130, 238),  # Violet
        (255, 215, 0),    # Gold
        (0, 255, 255),    # Cyan
        (255, 105, 180),  # Hot Pink
        (138, 43, 226),   # Blue Violet
        (0, 250, 154),    # Medium Spring Green
        (255, 140, 0),    # Dark Orange
    ])
    
    # Noise/outlier color (unclustered shrimp)
    unclustered_color: Tuple[int, int, int] = (169, 169, 169)  # Gray
    bbox_color: Tuple[int, int, int] = (0, 215, 255)            # Bright Yellow-Orange

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they do not exist."""
        for path in [DATA_DIR, RAW_VIDEOS_DIR, PROCESSED_VIDEOS_DIR, METADATA_DIR, MODELS_DIR]:
            path.mkdir(parents=True, exist_ok=True)
