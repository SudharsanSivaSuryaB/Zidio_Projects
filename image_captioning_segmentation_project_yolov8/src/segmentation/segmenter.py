"""Object detection using YOLOv8 (Ultralytics).

- Requires: pip install ultralytics
- Supports >600 classes (includes tiger, deer, etc.)
"""
from typing import List, Tuple
import numpy as np
from PIL import Image
import cv2
from ultralytics import YOLO

# Load YOLOv8 model once (large for accuracy, but can use yolov8m.pt for medium)
_model = None

def load_detector(model_name: str = "yolov8x.pt"):
    global _model
    if _model is None:
        _model = YOLO(model_name)
    return _model

def predict_boxes(image: Image.Image, conf: float = 0.25) -> List[Tuple[int,int,int,int,float,str]]:
    """Run YOLOv8 detection on an image.

    Returns list of (x,y,w,h,score,label).
    """
    model = load_detector()
    results = model.predict(image, conf=conf, verbose=False)
    boxes = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            score = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            boxes.append((x1, y1, x2-x1, y2-y1, score, label))
    return boxes

def draw_boxes(image: np.ndarray, boxes, thickness: int = 2) -> np.ndarray:
    """Draw YOLOv8 boxes with labels."""
    output = image.copy()
    for (x,y,w,h,score,label) in boxes:
        color = (0,255,0)
        cv2.rectangle(output, (x,y), (x+w,y+h), color, thickness)
        text = f"{label}:{score:.2f}"
        ty = y - 6 if y - 6 > 6 else y + 12
        cv2.putText(output, text, (x, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)
    return output
