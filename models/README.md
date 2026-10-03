# Model status

No usable shrimp-trained weights are included. The original aquaeye_best.pt file is a 93-byte placeholder. COCO yolov8n weights are not a shrimp detector. Weight files are excluded from Git.

Install ultralytics and provide actual trained weights with --weights. Class names must contain shrimp to enable the optional model stream. Without such weights AquaEye uses unvalidated image-processing candidates and reports that mode explicitly.
