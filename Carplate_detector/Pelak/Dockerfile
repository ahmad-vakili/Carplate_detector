FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# ابزارهای پایه
RUN pip install --no-cache-dir --retries 10 --timeout 300 \
    Django==4.2.24 Pillow==10.4.0

# OpenCV فقط نسخه headless
RUN pip install --no-cache-dir --retries 10 --timeout 300 \
    opencv-python-headless==4.10.0.84

# PyTorch نسخه CPU-only
RUN pip install --no-cache-dir --retries 10 --timeout 300 \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# Ultralytics
RUN pip install --no-cache-dir --retries 10 --timeout 300 \
    ultralytics==8.3.28

# EasyOCR
RUN pip install --no-cache-dir --retries 10 --timeout 300 \
    easyocr==1.7.2

COPY . .

# دانلود مدل YOLO
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]