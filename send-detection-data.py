# Library Imports
import requests
from datetime import datetime
import os
from ultralytics import YOLO
import cv2
import time

# Send Data to Website
def sendDataToWebsite(image_path, object_count):
    """ Sends detection data and the image to the server. """
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "secret": "VTS_Meowlynna-2312",
        "date_and_time": formatted_datetime,
        "number": object_count,
    }

    with open(image_path, "rb") as img_file:
        files = {
            "image": img_file
        }
        response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            print("Request successful!")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)


# Configurations
model_path = './models/datasetv1_200epoch.pt'
url = "https://thesis.esage.site/public/api/send-detection-data"
threshold = 0.5
send_interval = 60
output_dir = 'detected-frames'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Model and Camera Load
model = YOLO(model_path)
cap = cv2.VideoCapture(0)

# Frame reading
ret, frame = cap.read()
H, W, _ = frame.shape

last_send_time = time.time()

# Main program loop
while ret:
    # Get current frame and predict
    results = model(frame)[0]

    # Count objects
    object_count = sum(1 for result in results.boxes.data.tolist() if result[4] > threshold)

    # Draw bounding boxes on the frame
    for idx, result in enumerate(results.boxes.data.tolist()):
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{results.names[int(class_id)]} {score * 100:.2f}%",
                (int(x1), int(y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )


    # Send frame every 5 seconds
    current_time = time.time()
    if current_time - last_send_time >= send_interval:
        last_send_time = current_time
        output_path = os.path.join(output_dir, f"frame_{int(time.time())}.jpg")
        cv2.imwrite(output_path, frame)

        sendDataToWebsite(output_path, object_count)


    # Show Window Preview
    cv2.imshow("Detection Result", frame)

    # Wait for Esc key
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    # Read next frame
    ret, frame = cap.read()


# On program stop
cap.release()
cv2.destroyAllWindows()
