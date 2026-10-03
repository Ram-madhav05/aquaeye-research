"""
Dataset Parser: Connects and merges all 5 environmental calibration datasets:
1. depth_estimation.csv
2. light_reflection.csv
3. multiscale_image_tiling.csv
4. sensory_enhancement.csv
5. spatial_awareness.csv
Extracts dynamic parameters for optical preprocessing, YOLO detection, and DBSCAN clustering.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .config import (
    DEPTH_ESTIMATION_CSV,
    LIGHT_REFLECTION_CSV,
    MULTISCALE_TILING_CSV,
    SENSORY_ENHANCEMENT_CSV,
    SPATIAL_AWARENESS_CSV,
    Config,
)


class DatasetParser:
    """Loads, cleans, merges, and queries metadata across the 5 AquaEye CSV sources."""

    def __init__(
        self,
        depth_path: Path = DEPTH_ESTIMATION_CSV,
        light_path: Path = LIGHT_REFLECTION_CSV,
        tiling_path: Path = MULTISCALE_TILING_CSV,
        sensory_path: Path = SENSORY_ENHANCEMENT_CSV,
        spatial_path: Path = SPATIAL_AWARENESS_CSV,
    ):
        self.depth_path = depth_path
        self.light_path = light_path
        self.tiling_path = tiling_path
        self.sensory_path = sensory_path
        self.spatial_path = spatial_path

        self.df_depth = self._load_and_standardize(self.depth_path)
        self.df_light = self._load_and_standardize(self.light_path)
        self.df_tiling = self._load_and_standardize(self.tiling_path)
        self.df_sensory = self._load_and_standardize(self.sensory_path)
        self.df_spatial = self._load_and_standardize(self.spatial_path)

        self.master_df = self._build_master_dataframe()

    def _load_and_standardize(self, path: Path) -> pd.DataFrame:
        """Safely loads a CSV and standardizes video_id format."""
        if not path.exists():
            print(f"[DatasetParser] Warning: {path} does not exist.")
            return pd.DataFrame()
        try:
            df = pd.read_csv(path)
            if "video_id" in df.columns:
                df["video_id_clean"] = df["video_id"].astype(str).apply(self.normalize_video_id)
            return df
        except Exception as e:
            print(f"[DatasetParser] Error reading {path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def normalize_video_id(raw_name: str) -> str:
        """
        Normalizes any video identifier format to standard 'video_XXX':
        e.g., 'Video_001' -> 'video_001'
              'video_08.mp4' -> 'video_008'
              'sample_01.mp4' -> 'sample_01' (no real-video metadata)
        """
        stem = Path(raw_name).stem.lower().strip()
        # Synthetic samples must not inherit unrelated real-video calibration.
        if stem.startswith("sample_"):
            return stem
        # Handle video_001, video_08, video_8
        if stem.startswith("video_") or stem.startswith("video"):
            clean = stem.replace("video_", "").replace("video", "")
            if clean.isdigit():
                return f"video_{int(clean):03d}"
        
        return stem

    def _build_master_dataframe(self) -> pd.DataFrame:
        """Joins all 5 CSV tables on standardized video_id."""
        dfs = []
        for df, name in [
            (self.df_depth, "depth"),
            (self.df_light, "light"),
            (self.df_sensory, "sensory"),
            (self.df_spatial, "spatial"),
            (self.df_tiling, "tiling"),
        ]:
            if not df.empty and "video_id_clean" in df.columns:
                if df["video_id_clean"].duplicated().any():
                    raise ValueError(f"{name} contains duplicate video IDs. Aggregate or explicitly align frames before joining.")
                dfs.append(df)

        if not dfs:
            return pd.DataFrame()

        master = dfs[0].copy()
        for next_df in dfs[1:]:
            cols_to_use = [c for c in next_df.columns if c not in master.columns or c == "video_id_clean"]
            master = pd.merge(master, next_df[cols_to_use], on="video_id_clean", how="outer")

        return master

    def get_dynamic_parameters(self, video_name: str, frame_width: int = 1280, frame_height: int = 720) -> Dict[str, Any]:
        """
        Extracts dynamically calibrated parameters from the 5 CSVs for a specific video:
        - sensory_enhancement: noise_type, transmission_errors -> filter kernel & YOLO conf
        - depth_estimation: depth_map_mean, disparity_map_mean -> DBSCAN search radius epsilon
        - light_reflection: reflection_mask_sum, mean_intensity -> CLAHE clipLimit & glare dampening
        - spatial_awareness: contrast_level, spatial_complexity_score -> edge sensitivity
        - multiscale_image_tiling: resolution_x, resolution_y, filter_type -> patch scaling
        """
        video_key = self.normalize_video_id(video_name)

        # Baseline fallback defaults
        params: Dict[str, Any] = {
            "video_id": video_key,
            "raw_name": video_name,
            "metadata_matched": False,
            # Sensory Enhancement defaults
            "noise_type": "Gaussian",
            "transmission_errors": 0,
            "bandwidth_Hz": 250.0,
            # Depth Estimation defaults
            "depth_map_mean": 15.0,
            "disparity_map_mean": 5.0,
            "depth_confidence_score": 0.90,
            # Light Reflection defaults
            "mean_intensity": 100.0,
            "max_intensity": 255.0,
            "reflection_mask_sum": 2000,
            "contrast_enhancement_factor": 1.5,
            # Spatial Awareness defaults
            "mean_brightness": 85.0,
            "contrast_level": 30.0,
            "keypoint_density": 1.5,
            "spatial_complexity_score": 0.60,
            # Multiscale Tiling defaults
            "scale_level": 1,
            "resolution_x": 1280,
            "resolution_y": 720,
            "filter_type": "CLAHE",
            # Calculated dynamic parameters
            "clahe_clip_limit": Config.clahe_clip_limit,
            "clahe_tile_grid_size": Config.clahe_tile_grid_size,
            "denoise_h": Config.denoise_h,
            "dbscan_eps": Config.dbscan_eps,
            "dbscan_min_samples": Config.dbscan_min_samples,
            "conf_threshold": Config.conf_threshold,
        }

        # Query CSV data
        if not self.master_df.empty and "video_id_clean" in self.master_df.columns:
            match = self.master_df[self.master_df["video_id_clean"] == video_key]
            if not match.empty:
                row = match.iloc[0]
                params["metadata_matched"] = True
                
                # 1. Sensory Enhancement CSV
                if "noise_type" in row and pd.notna(row["noise_type"]):
                    params["noise_type"] = str(row["noise_type"]).strip()
                if "transmission_errors" in row and pd.notna(row["transmission_errors"]):
                    params["transmission_errors"] = int(row["transmission_errors"])
                if "bandwidth_Hz" in row and pd.notna(row["bandwidth_Hz"]):
                    params["bandwidth_Hz"] = float(row["bandwidth_Hz"])

                # 2. Depth Estimation CSV
                if "depth_map_mean" in row and pd.notna(row["depth_map_mean"]):
                    params["depth_map_mean"] = float(row["depth_map_mean"])
                if "disparity_map_mean" in row and pd.notna(row["disparity_map_mean"]):
                    params["disparity_map_mean"] = float(row["disparity_map_mean"])
                if "depth_confidence_score" in row and pd.notna(row["depth_confidence_score"]):
                    params["depth_confidence_score"] = float(row["depth_confidence_score"])

                # 3. Light Reflection CSV
                if "mean_intensity" in row and pd.notna(row["mean_intensity"]):
                    params["mean_intensity"] = float(row["mean_intensity"])
                if "reflection_mask_sum" in row and pd.notna(row["reflection_mask_sum"]):
                    params["reflection_mask_sum"] = float(row["reflection_mask_sum"])
                if "contrast_enhancement_factor" in row and pd.notna(row["contrast_enhancement_factor"]):
                    params["contrast_enhancement_factor"] = float(row["contrast_enhancement_factor"])

                # 4. Spatial Awareness CSV
                if "mean_brightness" in row and pd.notna(row["mean_brightness"]):
                    params["mean_brightness"] = float(row["mean_brightness"])
                if "contrast_level" in row and pd.notna(row["contrast_level"]):
                    params["contrast_level"] = float(row["contrast_level"])
                if "spatial_complexity_score" in row and pd.notna(row["spatial_complexity_score"]):
                    params["spatial_complexity_score"] = float(row["spatial_complexity_score"])

                # 5. Multiscale Tiling CSV
                if "resolution_x" in row and pd.notna(row["resolution_x"]):
                    params["resolution_x"] = int(row["resolution_x"])
                if "resolution_y" in row and pd.notna(row["resolution_y"]):
                    params["resolution_y"] = int(row["resolution_y"])
                if "filter_type" in row and pd.notna(row["filter_type"]):
                    params["filter_type"] = str(row["filter_type"]).strip()
                if "scale_level" in row and pd.notna(row["scale_level"]):
                    params["scale_level"] = int(row["scale_level"])

        # =====================================================================
        # FORMULAS CONNECTING CSVs TO PIPELINE
        # =====================================================================

        # A. Light Reflection -> CLAHE clipLimit
        # High reflection / intense mean brightness requires dampened clipLimit to avoid amplifying glare
        reflection_attenuation = max(0.5, 1.0 - (params["reflection_mask_sum"] / 10000.0))
        base_clip = 2.4 * params["contrast_enhancement_factor"] * reflection_attenuation
        params["clahe_clip_limit"] = float(np.clip(base_clip, 1.2, 4.5))

        # B. Sensory Enhancement -> YOLO Confidence Threshold
        # Scale confidence threshold upward if transmission error counts are high to suppress packet loss artifacts
        trans_err = params["transmission_errors"]
        params["conf_threshold"] = float(np.clip(Config.conf_threshold + (trans_err * 0.015), 0.20, 0.45))

        # C. Depth Estimation -> DBSCAN Epsilon (Search Radius)
        # Deeper water columns compress 2D perspective (shrimp appear smaller and closer together)
        # Therefore, search radius epsilon scales inversely with mean depth and scales with frame resolution
        depth_m = max(params["depth_map_mean"], 2.0)
        res_scale = frame_width / 1280.0
        depth_scaling = 18.0 / depth_m
        calibrated_eps = Config.dbscan_eps * depth_scaling * res_scale
        params["dbscan_eps"] = float(np.clip(calibrated_eps, 35.0, 160.0))

        # D. Spatial Awareness -> Denoising Strength & Min Samples
        if params["spatial_complexity_score"] > 0.70:
            params["denoise_h"] = 6.0
            params["dbscan_min_samples"] = 4
        else:
            params["denoise_h"] = 4.0
            params["dbscan_min_samples"] = 3

        return params
