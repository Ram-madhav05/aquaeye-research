# AquaEye research protocol

## Question

Does metadata-guided enhancement improve single-class shrimp detection and frame-level count accuracy compared with raw-image processing on held-out underwater recordings?

## Existing evidence

The supplied CSV contains 500 analyzed frames across ten video excerpts; the raw videos and stored images are not an annotated benchmark. Source metadata are per-video rows in the actual supplied schema, not synchronized measurements for every frame. Depth and environmental values have no verified calibration/provenance. The depth-to-DBSCAN-radius formula is a heuristic in image pixels, not a physical distance estimate. DBSCAN clusters do not establish biological social, feeding, or stress behavior.

The existing synthetic sample was historically mapped to video_001 metadata. This has been fixed for future runs. The dashboard deliberately retains the historical CSV unchanged, labels it as legacy, and does not imply the new tracker reproduces those numbers.

## Dataset and annotation

1. Document footage source, collection date, camera, pond, species if independently known, image size, lighting, and data permissions.
2. Define a visible-shrimp annotation policy, including occlusions and truncated bodies. Use two annotators on a subset and adjudicate disagreements.
3. Split by pond/video/session before selecting frames. Adjacent frames from one recording must not leak across train, validation, and test.
4. Include negative frames with bubbles, substrate, feed, reflections, and camera motion. Stratify by turbidity and illumination where verified labels exist.
5. Freeze the test set and annotation version. Save input hashes and the exact Git commit with published experiments.

## Controlled experiments

Compare the same held-out frames with raw processing, fixed CLAHE, and metadata-adaptive enhancement. Compare heuristic-only and trained-shrimp-model variants separately. The current optional YOLO path fuses with heuristic candidates; isolate streams before claiming a pure YOLO ablation. Hold detection and clustering thresholds fixed for an enhancement ablation, or explicitly report threshold differences. Tune only on validation data.

Repeat clustering over a preregistered epsilon/min-samples range. Report sensitivity; do not choose settings using the test labels. Physical swarm density needs camera calibration and scene scale, which the present code does not establish.

## Metrics

Use the supplied evaluator for fixed-threshold precision, recall, F1 and count MAE/RMSE. It sorts predictions by score and matches each at most once to the highest-IoU unmatched target in the same video/frame. Report IoU and score thresholds. It does not compute AP/mAP. Report video-level uncertainty (for example bootstrap videos, not correlated frames), sample sizes, and failure cases.

To evaluate identity continuity, collect track-ID ground truth and use established MOT metrics separately. Synthetic smoke tests verify software execution, not biological accuracy. Scores assigned to heuristic contours are not calibrated confidence probabilities.

## Reproducibility and timing

Use unique output directories for each run to preserve previous results. Record commit, command, dependency lock, source-file hashes, model hash, hardware, device, enhancement settings, and metadata version. Current manifests capture per-video settings, model hash, versions, device, OS, and processing duration; capture hardware and repository commit alongside them.

Reported pipeline FPS covers decoding, enhancement, detection, association, annotation and encoding, including cold-frame effects. It excludes model initialization and JSON exports. Do not compare it to browser animation FPS or to inference-only GPU benchmarks. Use full clips, repeated runs, warm-up policy and hardware reporting for publication.

## Before scientific claims

The project currently lacks a usable trained shrimp model and a labeled held-out benchmark. Neither false-positive elimination nor detection accuracy has been demonstrated. Annotated legacy images are not ground truth. Publish quantitative findings only after the protocol is executed; retain null/unavailable values for unmeasured results.
