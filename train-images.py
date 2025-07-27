# Library import
from ultralytics import YOLO

# Model load
model = YOLO("yolov8n.pt")

# Training
results = model.train(data='./config.yaml', epochs=200)