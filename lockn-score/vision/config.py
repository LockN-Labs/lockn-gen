from dataclasses import dataclass


@dataclass
class DetectorConfig:
    # Model: use YOLOv8n or YOLOv8s for speed
    model_path: str = "yolov8n.pt"

    # Inference settings
    img_size: int = 640  # can raise to 960/1280 for better small-object recall
    conf: float = 0.25
    iou: float = 0.45
    device: str = "0"  # GPU index or "cpu"
    half: bool = True  # FP16 for speed
    max_det: int = 50

    # Performance
    stream: bool = True  # stream mode for real-time
    agnostic_nms: bool = False

    # Optional: class filter for COCO sports ball (class id 32)
    # Set to None to detect all classes
    classes: list[int] | None = None
