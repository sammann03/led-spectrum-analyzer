import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# === Extract colour name from filename ===
def extract_colour(filename):
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]  # "led_red"
    parts = name.split("_")
    return parts[1] if len(parts) >= 2 else "unknown"

# === Process video and generate brightness plot ===
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    brightness = []
    timestamps = []

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness.append(np.mean(gray))
        timestamps.append(frame_num / fps)
        frame_num += 1

    cap.release()

    brightness = np.array(brightness)
    timestamps = np.array(timestamps)
    colour = extract_colour(video_path)

    # === Plot Brightness Curve ===
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, brightness, label=f'{colour} LED Brightness')
    plt.title(f'{colour.capitalize()} LED Brightness Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.grid(True)
    plt.tight_layout()

    filename = f'led_{colour}_brightness_curve.png'
    plt.savefig(filename)
    print(f"📊 Saved: {filename}")
    plt.close()

# === Run for your 4 LED videos ===
video_files = [
    'led_red.mp4',
    'led_blue.mp4',
    'led_green.mp4',
    'led_yellow.mp4'
]

for video in video_files:
    process_video(video)
