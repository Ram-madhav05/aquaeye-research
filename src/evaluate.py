"""Dependency-free, single-class detection evaluation at a fixed IoU threshold.

Input: {"frames": [{"video_id": "video_020", "frame_index": 0,
                   "boxes": [{"bbox": [x1, y1, x2, y2], "score": 0.8}]}]}
Ground-truth boxes omit score. Include labeled empty frames explicitly.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def iou(a, b):
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    union = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - intersection
    return intersection / union if union else 0.0


def _index(document, predictions=False):
    if not isinstance(document, dict) or not isinstance(document.get("frames"), list):
        raise ValueError("Expected an object with a frames list")
    frames = {}
    for frame in document["frames"]:
        if not isinstance(frame, dict):
            raise ValueError("Frame must be an object")
        video, index = frame.get("video_id"), frame.get("frame_index")
        if not isinstance(video, str) or not video or type(index) is not int or index < 0:
            raise ValueError("Frame needs nonempty video_id and nonnegative integer frame_index")
        key = (video, index)
        if key in frames:
            raise ValueError(f"Duplicate frame: {key}")
        boxes = frame.get("boxes")
        if not isinstance(boxes, list):
            raise ValueError("Each frame requires boxes, including [] for negatives")
        clean = []
        for box in boxes:
            if not isinstance(box, dict):
                raise ValueError("Box must be an object")
            bbox = box.get("bbox")
            if not isinstance(bbox, list) or len(bbox) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in bbox):
                raise ValueError("bbox must contain four finite nonnegative coordinates")
            if bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
                raise ValueError("bbox must have positive width and height")
            score = box.get("score", 1.0)
            if predictions and (type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1):
                raise ValueError("Prediction score must be in [0, 1]")
            clean.append({"bbox": bbox, "score": score})
        frames[key] = clean
    return frames


def evaluate(ground_truth, predictions, iou_threshold=0.5, confidence_threshold=0.0):
    if not 0 < iou_threshold <= 1 or not 0 <= confidence_threshold <= 1:
        raise ValueError("Invalid IoU or confidence threshold")
    truth, predicted = _index(ground_truth), _index(predictions, predictions=True)
    if not truth:
        raise ValueError("Ground truth has no labeled frames")
    unknown = predicted.keys() - truth.keys()
    if unknown:
        raise ValueError(f"Predictions include {len(unknown)} unlabeled frames; explicitly select the evaluation subset")
    tp = fp = fn = 0
    absolute_errors, squared_errors, frame_results = [], [], []
    for key, targets in sorted(truth.items()):
        candidates = sorted((p for p in predicted.get(key, []) if p["score"] >= confidence_threshold), key=lambda p: -p["score"])
        remaining = set(range(len(targets)))
        matched = 0
        for candidate in candidates:
            best = max(sorted(remaining), key=lambda j: iou(candidate["bbox"], targets[j]["bbox"]), default=None)
            if best is not None and iou(candidate["bbox"], targets[best]["bbox"]) >= iou_threshold:
                remaining.remove(best)
                matched += 1
        false_positives, false_negatives = len(candidates)-matched, len(targets)-matched
        tp += matched; fp += false_positives; fn += false_negatives
        error = len(candidates)-len(targets)
        absolute_errors.append(abs(error)); squared_errors.append(error*error)
        frame_results.append({"video_id": key[0], "frame_index": key[1], "tp": matched, "fp": false_positives, "fn": false_negatives, "predicted_count": len(candidates), "true_count": len(targets)})
    precision = tp/(tp+fp) if tp+fp else None
    recall = tp/(tp+fn) if tp+fn else None
    return {"schema_version": 1, "task": "single_class_detection", "iou_threshold": iou_threshold,
            "confidence_threshold": confidence_threshold, "labeled_frames": len(truth),
            "missing_prediction_frames": len(truth.keys()-predicted.keys()),
            "true_positives": tp, "false_positives": fp, "false_negatives": fn,
            "precision": precision, "recall": recall,
            "f1": 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,
            "count_mae": sum(absolute_errors)/len(truth), "count_rmse": math.sqrt(sum(squared_errors)/len(truth)),
            "matching": "confidence-ranked greedy one-to-one IoU; not mAP", "per_frame": frame_results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--confidence", type=float, default=0.0)
    args = parser.parse_args()
    report = evaluate(json.loads(args.ground_truth.read_text(encoding="utf-8")), json.loads(args.predictions.read_text(encoding="utf-8")), args.iou, args.confidence)
    report["input_sha256"] = {"ground_truth": hashlib.sha256(args.ground_truth.read_bytes()).hexdigest(), "predictions": hashlib.sha256(args.predictions.read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "per_frame"}, indent=2))

if __name__ == "__main__":
    main()
