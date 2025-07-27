# import library
from ultralytics import YOLO

# Pilih dan load model (sesuaikan sama versi YOLO yang mau dipake)
model = YOLO("yolov8n.pt")

# Training
results = model.train(data='./config.yaml', epochs=200)