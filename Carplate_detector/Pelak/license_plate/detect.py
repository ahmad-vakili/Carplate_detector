import cv2
import easyocr
import re
from ultralytics import YOLO

_model = YOLO("yolov8n.pt")
_reader = easyocr.Reader(['fa', 'en'], gpu=False)

PLATE_PATTERN = re.compile(r'^\d{2}[آ-ی]\d{3}\d{2}$')

CONFIDENCE_THRESHOLD = 0.4
OCR_CONFIDENCE_THRESHOLD = 0.5
FRAME_SKIP = 5


def _clean_plate_text(text: str) -> str:
    return text.strip().replace(" ", "")


def detect_license_plate_yolo(video_path: str) -> str:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("[DEBUG] cv2 could not open the video file at all")
        return "نامشخص"

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[DEBUG] video opened OK, total_frames={total_frames}")

    best_text = "نامشخص"
    best_score = 0.0
    frame_idx = 0
    processed_frames = 0
    total_boxes_seen = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        if frame_idx % FRAME_SKIP != 0:
            continue

        processed_frames += 1
        results = _model(frame, verbose=False)[0]
        total_boxes_seen += len(results.boxes)

        for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
            class_name = _model.names[int(cls)]
            print(f"[DEBUG] frame {frame_idx}: detected class='{class_name}' conf={float(conf):.2f}")

            if float(conf) < CONFIDENCE_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box)
            if x2 <= x1 or y2 <= y1:
                continue

            plate_roi = frame[y1:y2, x1:x2]
            if plate_roi.size == 0:
                continue

            text_results = _reader.readtext(plate_roi)
            for (bbox, text, prob) in text_results:
                cleaned = _clean_plate_text(text)
                print(f"[DEBUG]   OCR read text='{cleaned}' prob={prob:.2f}")

                if len(cleaned) < 5 or prob < OCR_CONFIDENCE_THRESHOLD:
                    continue

                score = prob + (0.5 if PLATE_PATTERN.match(cleaned) else 0)
                if score > best_score:
                    best_score = score
                    best_text = cleaned

    cap.release()
    print(f"[DEBUG] processed_frames={processed_frames}, total_boxes_seen={total_boxes_seen}, final_result='{best_text}'")
    return best_text