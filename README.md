# AquaEye

An underwater computer-vision research prototype for image enhancement, shrimp **candidate** detection, temporal association, and spatial clustering. The Next.js observatory lets reviewers inspect historical experiments and download their underlying data.

## Research status

The supplied batch summary contains **10 excerpts of 50 frames each**. One is a synthetic sample. Its counts are historical detector outputs, not ground truth. No labeled test set, measured accuracy, usable shrimp-trained weights, or reproducible historical throughput benchmark is supplied. The 93-byte `aquaeye_best.pt` file is a placeholder. General COCO weights do not contain a shrimp class.

The previous browser simulation and hard-coded benchmark/count claims have been replaced by a CSV-backed results explorer. Stored frame overlays have incomplete run provenance and may not correspond to the summary run. They are illustrations, not validation evidence. The legacy `ui/` directory is an archived, unvalidated demonstration and is not deployed.

## Start the dashboard

Requires Node.js 22+ and npm. From the repository root:

```sh
cd web
npm ci
npm run dev
```

Open http://localhost:3000. The predev/prebuild exporter reads `data/processed_videos/batch_processing_summary.csv`, checks the required images, and generates the dashboard JSON and portable CSV. The JSON includes the source file SHA-256. No database, API key, camera access, or inference service is needed for the hosted dashboard.

```sh
npm run lint
npm run build
```

## Run the research pipeline

Requires Python 3.10+:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-core.txt
python -m unittest discover -s tests -v
python -m src.main --video_dir data/raw_videos --output_dir runs/enhanced --limit 50
python -m src.main --video_dir data/raw_videos --output_dir runs/raw --limit 50 --no_enhance
```

Provide your own footage in `data/raw_videos`. Large videos and weights are excluded from Git. Missing input fails explicitly; synthetic footage is generated only with `python -m src.main --generate_samples`. Synthetic samples use distinct metadata IDs and fallback parameters.

The core install uses OpenCV heuristics without PyTorch or automatic weight downloads. For a shrimp-trained model, install `ultralytics` and supply `--weights path/to/best.pt`. Only classes containing `shrimp` in their names are used. Other class labels require an explicit code mapping. `--device cpu` is the default. For an interactive camera session, use the fuller `requirements.txt` environment with GUI OpenCV and `python -m src.live_tracker --source 0`.

Each batch video produces an annotated MP4, zero-based per-frame predictions JSON, and a manifest recording parameters, detector mode, model hash when applicable, environment versions, and measured end-to-end processing time. The batch summary CSV is also saved. Heuristic scores are ranking scores, not calibrated probabilities. A custom-model inference error fails visibly instead of silently changing the detector.

## Evaluate detections

```sh
python -m src.evaluate --ground-truth annotations.json --predictions runs/enhanced/video_020_predictions.json --output evaluation.json --iou 0.5
```

Both inputs use `{"frames": [{"video_id": "video_020", "frame_index": 0, "boxes": [{"bbox": [10, 20, 40, 60]}]}]}`. Predictions can include a `score` per box. Boxes are `[x1,y1,x2,y2]` in processed-frame pixel coordinates. Explicitly include negative frames with `boxes: []`. Predictions for unlabeled frames are rejected; select the same labeled evaluation subset first. Missing prediction frames count as empty detections.

The evaluator reports one-to-one, confidence-ranked IoU precision, recall, F1, count MAE/RMSE and per-frame matches. Undefined rates are `null`. This is **not mAP, identity-tracking accuracy, species verification, or evidence of feeding/stress behavior**. See [the research protocol](docs/RESEARCH_PROTOCOL.md).

## Deployment

Import this GitHub repository into Vercel, select **Next.js**, set **Root Directory = web**, enable inclusion of source files outside the root directory, and use npm with `npm ci` / `npm run build`. The exporter requires the parent `data/` directory. Deployments host the static research dashboard; Python/OpenCV inference runs separately on a workstation or suitable compute service.

GitHub Actions checks Python regressions, dashboard lint, and the production build. No secrets are needed. No license is assigned to the original footage, weights, or dataset by this repository.
