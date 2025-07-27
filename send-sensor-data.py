# Library imports
import serial
import requests
import time

# Configurations
COM_PORT = 'COM4'
BAUD_RATE = 9600
URL = "https://thesis.esage.site/public/api/send-sensor-data"
send_interval = 60  # seconds

# Start serial connection
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
    print(f"Connected to {COM_PORT} at {BAUD_RATE} baud.")
except Exception as e:
    print("Failed to connect to serial port:", e)
    exit()

# Track time of last POST
last_send_time = 0

# Main program loop
while True:
    # Normal flow
    try:
        # Read data from serial monitor
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        print("Received:", line)

        # Parse string into JSON format
        data = {}
        for part in line.split(','):
            key, value = part.split(':')
            data[key.strip()] = float(value.strip())


        data["secret"] = "VTS_Meowlynna-2312"

        # Send to website every 5 seconds
        current_time = time.time()
        if current_time - last_send_time >= send_interval:
            last_send_time = current_time
            print("Sending:", data)
            response = requests.post(URL, json=data)
            print("POST Status:", response.status_code)

    # Exception handling
    except KeyboardInterrupt:
        print("Stopped by user.")
        break
    except Exception as e:
        print("Error:", e)


# On program stop
ser.close()