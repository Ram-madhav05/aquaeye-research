"""
AquaEye Live Stream Shrimp Tracker.
Processes real-time underwater video feeds from:
- USB / Underwater Camera Index (e.g. --source 0)
- RTSP / HTTP IP Camera URL (e.g. --source rtsp://admin:pass@192.168.1.50/stream)
- Local Video File Stream (e.g. --source data/raw_videos/video_016.mp4)

Features:
- Real-time 40-50+ FPS tracking with multiscale resolution pyramid
- Live HUD overlay with depth, noise filter, verified shrimp count, and active schools
- Live feeder target reticle pointing to the highest biomass centroid
- Keyboard shortcuts:
  [Q / ESC] Quit stream
  [Space]   Pause / Resume
  [S]       Save high-resolution annotated snapshot
  [E]       Toggle optical enhancement (CIELAB + CLAHE + Denoise) on/off
  [F]       Simulate precision feeder trigger
  [+] / [-] Increase / Decrease DBSCAN swarm grouping radius
"""

import sys
import time
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

import cv2
import numpy as np

# Ensure parent directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.tracker import ShrimpGroupTracker
from src.image_enhancement import enhance_underwater_frame, CLAHEEnhancer


def parse_args():
    parser = argparse.ArgumentParser(description="AquaEye Live Stream Shrimp Vision & Swarm Tracker")
    parser.add_argument(
        "--source",
        type=str,
        default="data/raw_videos/video_013.mp4",
        help="Camera device index (0, 1), RTSP/HTTP URL, or path to local .mp4 video file (default: data/raw_videos/video_013.mp4)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/yolov8n.pt",
        help="Path to YOLO weights",
    )
    parser.add_argument(
        "--depth",
        type=float,
        default=2.99,
        help="Estimated optical depth in meters (default: 2.99)",
    )
    parser.add_argument(
        "--noise",
        type=str,
        default="Impulse",
        choices=["Impulse", "SaltPepper", "Poisson", "Speckle", "Gaussian"],
        help="Noise classification for adaptive filtering (default: Impulse)",
    )
    parser.add_argument(
        "--clahe-clip",
        type=float,
        default=2.44,
        help="CLAHE clip limit for optical contrast boost (default: 2.44)",
    )
    parser.add_argument(
        "--eps",
        type=float,
        default=160.0,
        help="DBSCAN grouping radius in pixels (default: 160.0)",
    )
    parser.add_argument(
        "--min-samples",
        type=int,
        default=2,
        help="DBSCAN min points to form a schooling cluster (default: 2)",
    )
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Disable CIELAB enhancement pipeline for maximum raw FPS",
    )
    parser.add_argument(
        "--record",
        type=str,
        default=None,
        help="Optional output path to record processed live stream (e.g. data/processed_videos/live_output.mp4)",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        default=True,
        help="Loop video file when end is reached (default: True for continuous live simulation)",
    )
    return parser.parse_args()


def run_live_tracker():
    args = parse_args()

    # Determine capture source
    source: Any = args.source
    if str(source).isdigit():
        source = int(source)
        source_label = f"Camera #{source}"
    else:
        source_label = Path(source).name if Path(source).exists() else str(source)

    print("=" * 65)
    print(" AQUAEYE VISION | Precision Live Stream Shrimp Tracker")
    print("=" * 65)
    print(f" Source Stream    : {source_label}")
    print(f" Optical Depth    : {args.depth:.2f} m")
    print(f" Noise Filter     : {args.noise}")
    print(f" CLAHE Clip Limit : {args.clahe_clip:.2f}")
    print(f" DBSCAN Radius    : {args.eps:.1f} px | MinPts: {args.min_samples}")
    print(f" Optical Enhance  : {'Disabled' if args.no_enhance else 'Active (CIELAB CLAHE + Denoise)'}")
    print("-" * 65)
    print(" Interactive Controls:")
    print("  [Q / ESC] Quit stream")
    print("  [Space]   Pause / Resume")
    print("  [S]       Save annotated snapshot")
    print("  [E]       Toggle optical enhancement on/off")
    print("  [F]       Simulate precision feeder drop")
    print("  [+] / [-] Increase / Decrease DBSCAN grouping radius")
    print("=" * 65)

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERROR] Unable to open video source: {source}")
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_in = cap.get(cv2.CAP_PROP_FPS) or 30.0

    print(f"[INFO] Stream connected successfully ({width}x{height} @ {fps_in:.1f} FPS)")

    # Video Writer if recording requested
    writer = None
    if args.record:
        out_path = Path(args.record)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(out_path), fourcc, fps_in, (width, height))
        print(f"[INFO] Recording live stream to: {out_path}")

    # Initialize Tracker
    tracker = ShrimpGroupTracker(
        model_path=args.model,
        dbscan_eps=args.eps,
        dbscan_min_samples=args.min_samples,
    )

    enhancer = CLAHEEnhancer(clip_limit=args.clahe_clip)
    enhance_enabled = not args.no_enhance
    current_eps = args.eps
    feeder_active_frames = 0

    enhancement_params = {
        "clahe_clip_limit": args.clahe_clip,
        "noise_type": args.noise,
        "reflection_mask_sum": 2000.0,
        "lab_l_boost": 1.05,
        "gamma_correction": 0.98,
    }

    fps_history = []
    frame_idx = 0
    paused = False

    cv2.namedWindow("AquaEye Vision - Live Stream Tracker", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AquaEye Vision - Live Stream Tracker", min(width, 1280), min(height, 720))

    try:
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    if args.loop and not isinstance(source, int):
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    else:
                        print("[INFO] End of stream reached.")
                        break

                t_start = time.perf_counter()

                # 1. Optical Enhancement
                if enhance_enabled:
                    processed_frame = enhance_underwater_frame(
                        frame, params=enhancement_params, enhancer_cache=enhancer
                    )
                else:
                    processed_frame = frame

                # 2. Multi-Stream Detection & Tracking
                shrimps, groups = tracker.update(
                    processed_frame,
                    custom_eps=current_eps,
                    custom_min_samples=args.min_samples,
                )

                t_latency = (time.perf_counter() - t_start) * 1000
                current_fps = 1000.0 / max(t_latency, 1.0)
                fps_history.append(current_fps)
                if len(fps_history) > 30:
                    fps_history.pop(0)
                avg_fps = sum(fps_history) / len(fps_history)

                # 3. Telemetry Metadata for HUD
                telemetry = {
                    "video_id": f"LIVE: {source_label}",
                    "depth_m": args.depth,
                    "noise_type": args.noise if enhance_enabled else "Raw (No Enhance)",
                    "clahe_clip_limit": args.clahe_clip if enhance_enabled else 1.0,
                    "dbscan_eps": current_eps,
                    "dbscan_min_samples": args.min_samples,
                }

                # 4. Render HUD & Visual Overlays
                annotated = tracker.annotate(
                    frame if not enhance_enabled else processed_frame,
                    shrimps,
                    groups,
                    metadata=telemetry,
                    show_trajectories=True,
                    show_hulls=True,
                    show_hud=True,
                )

                # 5. Live Performance Badge
                perf_text = f"Throughput: {avg_fps:.1f} FPS | Latency: {t_latency:.1f} ms"
                cv2.putText(
                    annotated,
                    perf_text,
                    (width - 340, 32),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0, 242, 254),
                    1,
                    cv2.LINE_AA,
                )

                # 6. Feeder Dispensing Visual Feedback
                if feeder_active_frames > 0:
                    feeder_active_frames -= 1
                    target_pt = (
                        shrimps[0].centroid
                        if shrimps
                        else (width // 2, height // 2)
                    )
                    radius = int(30 + (30 - feeder_active_frames) * 2.5)
                    cv2.circle(annotated, target_pt, radius, (0, 215, 255), 2, lineType=cv2.LINE_AA)
                    cv2.circle(annotated, target_pt, 6, (0, 255, 0), -1)
                    cv2.putText(
                        annotated,
                        "FEED DISPENSED [ACTIVE]",
                        (target_pt[0] - 80, target_pt[1] - radius - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.48,
                        (0, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )

                if writer is not None:
                    writer.write(annotated)

                cv2.imshow("AquaEye Vision - Live Stream Tracker", annotated)
                frame_idx += 1

            # Keyboard Interactions
            key = cv2.waitKey(1 if not paused else 50) & 0xFF
            if key in [ord("q"), 27]:  # Q or ESC
                break
            elif key == ord(" "):  # Space: Pause/Resume
                paused = not paused
                print(f"[INFO] Stream {'PAUSED' if paused else 'RESUMED'}")
            elif key in [ord("s"), ord("S")]:  # S: Save Snapshot
                snap_path = BASE_DIR / "data" / "processed_videos" / f"live_snapshot_{int(time.time())}.jpg"
                cv2.imwrite(str(snap_path), annotated)
                print(f"[INFO] Saved snapshot to: {snap_path}")
            elif key in [ord("e"), ord("E")]:  # E: Toggle Enhancement
                enhance_enabled = not enhance_enabled
                print(f"[INFO] Optical Enhancement: {'ENABLED' if enhance_enabled else 'DISABLED'}")
            elif key in [ord("f"), ord("F")]:  # F: Trigger Feeder
                feeder_active_frames = 25
                shrimp_count = len(shrimps)
                dose = shrimp_count * 3.8
                print(f"[FEEDER TRIGGERED] Target biomass: {shrimp_count} shrimp | Dose: {dose:.1f}g Pellets")
            elif key in [ord("+"), ord("=")]:  # Increase DBSCAN eps
                current_eps = min(current_eps + 10.0, 300.0)
                print(f"[INFO] DBSCAN Radius increased to: {current_eps:.1f}px")
            elif key in [ord("-"), ord("_")]:  # Decrease DBSCAN eps
                current_eps = max(current_eps - 10.0, 20.0)
                print(f"[INFO] DBSCAN Radius decreased to: {current_eps:.1f}px")

    finally:
        cap.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()
        print("\n[INFO] Live stream tracker stopped cleanly.")


if __name__ == "__main__":
    run_live_tracker()
