# LockN Score — YOLOv8 Ping Pong Ball Detection

This project sets up YOLOv8 for real-time ping pong ball detection on an RTX 6000-class GPU. It uses a COCO-pretrained YOLOv8 model initially and is structured for later fine-tuning on ping pong–specific data.

## Structure
```
lockn-score/
  vision/
    config.py
    detector.py
  requirements.txt
  README.md
```

## Setup
```bash
cd ~/.openclaw/workspace/lockn-score
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Model Choices (Pretrained)
- **YOLOv8n** (`yolov8n.pt`) — fastest, best for 120+ FPS
- **YOLOv8s** (`yolov8s.pt`) — slightly heavier, better accuracy

COCO includes class **sports ball (id 32)**, which is a reasonable starting point. For best ping pong performance, fine-tune on ping pong–specific data.

## Usage
### Single-frame inference
```python
from vision.config import DetectorConfig
from vision.detector import PingPongDetector

cfg = DetectorConfig(model_path="yolov8n.pt", img_size=640)
# Optional: focus on sports ball class only
# cfg.classes = [32]

detector = PingPongDetector(cfg)
frame = ...  # numpy BGR image
print(detector.detect(frame))
```

### Real-time webcam demo
```bash
python -m vision.detector
```

## Performance Tips (120+ FPS target)
- Use **YOLOv8n** + **FP16** (`half=True`)
- Keep `img_size` at **640** for speed; increase if ball is too small
- Set `classes=[32]` to reduce NMS overhead
- Pre-warm the model (`detector.warmup()`)
- Use a high-FPS camera; reduce exposure to limit motion blur

## Handling Motion Blur
- Lower exposure/shorter shutter time if possible
- Consider higher `img_size` or `yolov8s.pt` if recall is too low
- Plan a fine-tune step with blurred ball samples for robustness

## Fine-Tuning (Later)
Collect ping pong ball images/videos and train a custom model:
```bash
yolo detect train data=pingpong.yaml model=yolov8n.pt imgsz=640
```

## Notes
- COCO sports ball detection may miss tiny or blurred ping pong balls.
- A custom dataset will significantly improve accuracy.
