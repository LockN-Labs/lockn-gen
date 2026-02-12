from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Iterator

import cv2
import numpy as np
from ultralytics import YOLO

from .config import DetectorConfig


class PingPongDetector:
    def __init__(self, config: DetectorConfig | None = None) -> None:
        self.config = config or DetectorConfig()
        self.model = YOLO(self.config.model_path)

    def warmup(self) -> None:
        dummy = np.zeros((self.config.img_size, self.config.img_size, 3), dtype=np.uint8)
        _ = self.model.predict(
            source=dummy,
            imgsz=self.config.img_size,
            conf=self.config.conf,
            iou=self.config.iou,
            device=self.config.device,
            half=self.config.half,
            max_det=self.config.max_det,
            stream=False,
            agnostic_nms=self.config.agnostic_nms,
            classes=self.config.classes,
            verbose=False,
        )

    def detect(self, frame: np.ndarray) -> list[dict]:
        """
        Run inference on a single frame.
        Returns list of detections: {xyxy, conf, cls, name}
        """
        results = self.model.predict(
            source=frame,
            imgsz=self.config.img_size,
            conf=self.config.conf,
            iou=self.config.iou,
            device=self.config.device,
            half=self.config.half,
            max_det=self.config.max_det,
            stream=False,
            agnostic_nms=self.config.agnostic_nms,
            classes=self.config.classes,
            verbose=False,
        )

        detections: list[dict] = []
        for r in results:
            if r.boxes is None:
                continue
            for b in r.boxes:
                xyxy = b.xyxy[0].tolist()
                conf = float(b.conf[0])
                cls_id = int(b.cls[0])
                name = self.model.names.get(cls_id, str(cls_id))
                detections.append({"xyxy": xyxy, "conf": conf, "cls": cls_id, "name": name})
        return detections

    def detect_stream(self, frames: Iterable[np.ndarray]) -> Iterator[list[dict]]:
        """Stream inference over frames (generator)."""
        results = self.model.predict(
            source=frames,
            imgsz=self.config.img_size,
            conf=self.config.conf,
            iou=self.config.iou,
            device=self.config.device,
            half=self.config.half,
            max_det=self.config.max_det,
            stream=True,
            agnostic_nms=self.config.agnostic_nms,
            classes=self.config.classes,
            verbose=False,
        )
        for r in results:
            detections: list[dict] = []
            if r.boxes is not None:
                for b in r.boxes:
                    xyxy = b.xyxy[0].tolist()
                    conf = float(b.conf[0])
                    cls_id = int(b.cls[0])
                    name = self.model.names.get(cls_id, str(cls_id))
                    detections.append({"xyxy": xyxy, "conf": conf, "cls": cls_id, "name": name})
            yield detections


if __name__ == "__main__":
    # Example real-time webcam inference
    config = DetectorConfig()
    # For COCO sports ball class only (class id 32), uncomment:
    # config.classes = [32]

    detector = PingPongDetector(config)
    detector.warmup()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)
        for det in detections:
            x1, y1, x2, y2 = map(int, det["xyxy"])
            conf = det["conf"]
            label = f"{det['name']} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow("PingPong Detector", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
