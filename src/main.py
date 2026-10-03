"""
Main Execution Script for AquaEye Video Processing Pipeline.
Iterates through raw video files, loads dynamic environmental parameters from CSVs,
applies underwater CIELAB/CLAHE enhancement, runs YOLO detection + DBSCAN clustering,
and exports annotated videos with spatial cluster visualizations and telemetry.
"""

import sys
import json
import time
import hashlib
import platform
from datetime import datetime, timezone
import argparse
from pathlib import Path
from typing import List, Dict, Any
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from .config import Config, RAW_VIDEOS_DIR, PROCESSED_VIDEOS_DIR
from .dataset_parser import DatasetParser
from .image_enhancement import enhance_underwater_frame, CLAHEEnhancer
from .tracker import ShrimpGroupTracker


def generate_synthetic_shrimp_video(output_path: Path, num_frames: int = 150, width: int = 640, height: int = 480):
    """
    Creates a synthetic aquatic video with moving shrimp-like entities
    to allow immediate pipeline testing when raw footage is not yet placed in data/raw_videos.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_path), fourcc, 25.0, (width, height))

    # Initialize shrimp particles (x, y, vx, vy, size)
    np.random.seed(42)
    num_particles = 45
    particles = []
    for _ in range(num_particles):
        x = np.random.uniform(50, width - 50)
        y = np.random.uniform(50, height - 50)
        vx = np.random.uniform(-1.5, 1.5)
        vy = np.random.uniform(-1.0, 1.0)
        size = np.random.randint(12, 28)
        particles.append([x, y, vx, vy, size])

    for f in range(num_frames):
        # Aquatic background gradient (greenish-blue underwater murk)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :, 0] = np.linspace(80, 50, height)[:, None]   # B
        frame[:, :, 1] = np.linspace(110, 80, height)[:, None]  # G
        frame[:, :, 2] = np.linspace(50, 30, height)[:, None]   # R

        # Add water turbidity / particulate noise
        noise = np.random.normal(0, 10, (height, width, 3)).astype(np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Draw shrimp entities
        for p in particles:
            p[0] = (p[0] + p[2] - 20) % (width - 40) + 20
            p[1] = (p[1] + p[3] - 20) % (height - 40) + 20
            cx, cy = int(p[0]), int(p[1])
            s = p[4]
            # Translucent shrimp body ellipse
            angle = int(np.degrees(np.arctan2(p[3], p[2])))
            cv2.ellipse(frame, (cx, cy), (s, max(s // 3, 3)), angle, 0, 360, (180, 210, 230), -1)
            # Antennae line
            ant_end = (int(cx + np.cos(np.radians(angle)) * (s + 8)), int(cy + np.sin(np.radians(angle)) * (s + 8)))
            cv2.line(frame, (cx, cy), ant_end, (140, 180, 200), 1)

        out.write(frame)

    out.release()
    print(f"[AquaEye] Generated test synthetic video at: {output_path}")


def process_single_video(
    video_path: Path,
    output_dir: Path,
    parser: DatasetParser,
    tracker: ShrimpGroupTracker,
    config: Config,
    max_frames: int = -1,
) -> Dict[str, Any]:
    """Processes a single underwater video file."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"[Error] Unable to open video: {video_path}")
        return {}

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not np.isfinite(fps) or fps <= 0:
        fps = config.export_fps
    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 1. Fetch dynamic metadata connecting all 5 calibration CSVs
    dyn_params = parser.get_dynamic_parameters(video_path.name, frame_width=orig_w, frame_height=orig_h)

    # Use target resolution from multiscale_image_tiling.csv for ultra-high-resolution inputs
    target_w = dyn_params.get("resolution_x", orig_w)
    target_h = dyn_params.get("resolution_y", orig_h)
    if orig_w > 1920 and target_w > 0:
        width, height = target_w, target_h
    else:
        width, height = orig_w, orig_h

    if width <= 0 or height <= 0:
        cap.release()
        raise ValueError(f"Invalid video dimensions for {video_path.name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Recompute pixel-space parameters after any resize.
    dyn_params = parser.get_dynamic_parameters(video_path.name, frame_width=width, frame_height=height)
    tracker.conf_threshold = dyn_params["conf_threshold"]
    output_filename = f"{video_path.stem}_processed.mp4"
    output_path = output_dir / output_filename
    fourcc = cv2.VideoWriter_fourcc(*config.output_codec)
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    if not writer.isOpened():
        cap.release()
        writer.release()
        raise RuntimeError(f"Cannot open video writer: {output_path}")
    enhancer = CLAHEEnhancer(
        clip_limit=config.clahe_clip_limit,
        tile_grid_size=config.clahe_tile_grid_size,
    )

    # Reset tracker background model and tracks for clean video stream
    tracker.reset()

    frame_idx = 0
    prediction_frames = []
    started = time.perf_counter()
    shrimp_counts: List[int] = []
    cluster_counts: List[int] = []

    print(f"\nProcessing: {video_path.name} ({total_frames} frames @ {fps:.1f} FPS, scale: {width}x{height})...")
    progress_bar = tqdm(total=total_frames if max_frames <= 0 else min(total_frames, max_frames))

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))

            # 2. Image Enhancement
            if config.enable_enhancement:
                enhanced_frame = enhance_underwater_frame(frame, params=dyn_params, enhancer_cache=enhancer)
            else:
                enhanced_frame = frame

            # 3. Shrimp Detection & Group Tracking
            shrimps, groups = tracker.update(
                enhanced_frame,
                custom_eps=dyn_params.get("dbscan_eps", config.dbscan_eps),
                custom_min_samples=dyn_params.get("dbscan_min_samples", config.dbscan_min_samples),
            )

            # 4. Overlay Visualizations with 5-CSV Telemetry HUD
            annotated_frame = tracker.annotate(
                frame=enhanced_frame,
                shrimps=shrimps,
                groups=groups,
                metadata=dyn_params,
                show_trajectories=True,
                show_hulls=config.draw_cluster_hulls,
                show_hud=config.overlay_stats,
            )

            writer.write(annotated_frame)
            prediction_frames.append({
                "video_id": video_path.stem, "frame_index": frame_idx,
                "boxes": [{"bbox": list(shrimp.bbox), "score": float(shrimp.confidence)} for shrimp in shrimps],
            })

            shrimp_counts.append(len(shrimps))
            cluster_counts.append(len(groups))

            frame_idx += 1
            progress_bar.update(1)

            if max_frames > 0 and frame_idx >= max_frames:
                break

    finally:
        progress_bar.close()
        cap.release()
        writer.release()
    elapsed = time.perf_counter() - started
    (output_dir / f"{video_path.stem}_predictions.json").write_text(
        json.dumps({"frames": prediction_frames}, indent=2), encoding="utf-8")
    manifest = {
        "schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(),
        "video": video_path.name, "frames": frame_idx, "resolution": [width, height],
        "enhancement": config.enable_enhancement, "parameters": dyn_params,
        "detector": "hybrid_shrimp_yolo_and_heuristics" if tracker.is_custom_model else "heuristic",
        "weights_sha256": hashlib.sha256(Path(config.model_weights).read_bytes()).hexdigest() if tracker.is_custom_model else None,
        "elapsed_seconds": elapsed, "throughput_fps": frame_idx / elapsed if elapsed else 0,
        "timing_scope": "decode, enhancement, detection, tracking, annotation, encoding; excludes model initialization and JSON exports",
        "python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__,
        "device": config.device, "platform": platform.platform(), "validation": "unvalidated",
    }
    (output_dir / f"{video_path.stem}_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    avg_shrimp = float(np.mean(shrimp_counts)) if shrimp_counts else 0.0
    max_clusters = int(np.max(cluster_counts)) if cluster_counts else 0

    print(f"-> Saved: {output_path} | Avg Shrimp: {avg_shrimp:.1f} | Peak Clusters: {max_clusters}")

    return {
        "video_name": video_path.name,
        "video_id": dyn_params.get("video_id", "N/A"),
        "resolution": f"{width}x{height}",
        "depth_m": dyn_params.get("depth_map_mean", "N/A"),
        "noise_type": dyn_params.get("noise_type", "N/A"),
        "clahe_clip": round(dyn_params.get("clahe_clip_limit", 2.5), 2),
        "dbscan_eps": round(dyn_params.get("dbscan_eps", 65.0), 1),
        "total_frames": frame_idx,
        "average_shrimp_count": round(avg_shrimp, 2),
        "max_clusters_detected": max_clusters,
        "processed_path": str(output_path),
    }


def run_pipeline(
    video_dir: Path = RAW_VIDEOS_DIR,
    output_dir: Path = PROCESSED_VIDEOS_DIR,
    weights_path: Path = Config.model_weights,
    device: str = "cpu",
    limit_frames: int = -1,
    enable_enhancement: bool = True,
):
    """Executes the full video analysis batch loop."""
    Config.ensure_directories()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Scan for input videos
    video_extensions = {".mp4", ".avi", ".mov", ".mkv"}
    video_files = sorted(p for p in video_dir.iterdir() if p.is_file() and p.suffix.lower() in video_extensions) if video_dir.is_dir() else []

    if not video_files:
        raise FileNotFoundError(f"No input videos in {video_dir}. Add footage or explicitly use --generate_samples.")

    print(f"[AquaEye] Discovered {len(video_files)} video file(s) for processing.")

    # Initialize components
    parser = DatasetParser()
    tracker = ShrimpGroupTracker(
        weights_path=weights_path,
        conf_threshold=Config.conf_threshold,
        iou_threshold=Config.iou_threshold,
        device=device,
    )

    config = Config(
        device=device,
        model_weights=weights_path,
        enable_enhancement=enable_enhancement,
    )

    summary_records = []
    for v_file in video_files:
        rec = process_single_video(
            video_path=v_file,
            output_dir=output_dir,
            parser=parser,
            tracker=tracker,
            config=config,
            max_frames=limit_frames,
        )
        if rec:
            summary_records.append(rec)

    # Save summary report
    if summary_records:
        df_summary = pd.DataFrame(summary_records)
        summary_csv = output_dir / "batch_processing_summary.csv"
        df_summary.to_csv(summary_csv, index=False)
        print(f"\n[AquaEye] Batch processing complete! Summary saved to {summary_csv}")


def main():
    parser = argparse.ArgumentParser(description="AquaEye Shrimp Detection and Group Tracker")
    parser.add_argument("--video_dir", type=Path, default=RAW_VIDEOS_DIR, help="Path to raw videos")
    parser.add_argument("--output_dir", type=Path, default=PROCESSED_VIDEOS_DIR, help="Path to output videos")
    parser.add_argument("--weights", type=Path, default=Config.model_weights, help="Path to model weights (.pt)")
    parser.add_argument("--device", type=str, default="cpu", help="Device to use ('cpu' or 'cuda')")
    parser.add_argument("--limit", type=int, default=-1, help="Max frames to process per video (-1 for full)")
    parser.add_argument("--no_enhance", action="store_true", help="Disable CIELAB/CLAHE enhancement")
    parser.add_argument("--generate_samples", action="store_true", help="Generate 10 synthetic sample videos")

    args = parser.parse_args()

    if args.generate_samples:
        Config.ensure_directories()
        print("Generating 10 synthetic sample videos in data/raw_videos/...")
        for i in range(1, 11):
            vid_path = RAW_VIDEOS_DIR / f"sample_{i:02d}.mp4"
            if not vid_path.exists():
                generate_synthetic_shrimp_video(vid_path, num_frames=100)
        print("All 10 sample videos generated successfully.")
        return

    run_pipeline(
        video_dir=args.video_dir,
        output_dir=args.output_dir,
        weights_path=args.weights,
        device=args.device,
        limit_frames=args.limit,
        enable_enhancement=not args.no_enhance,
    )


if __name__ == "__main__":
    main()
