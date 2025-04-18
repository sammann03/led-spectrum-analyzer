import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import csv

# Function to extract LED color from the filename (format "led_colour.mp4")
def extract_color_from_filename(filename):
    color = filename.split('_')[1].replace('.mp4', '')  # Extract color after 'led_' and remove '.mp4'
    return color

# Save blink data (timestamps of detected blinks) to CSV
def save_blink_data(color, timestamps, peaks, filename="blink_data.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([color, *timestamps[peaks]])  # Save color and corresponding blink timestamps

# Load video
video_path = 'led_green.mp4'  # Example for yellow LED video, change dynamically as needed
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Video file could not be opened.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
brightness = []
timestamps = []

# Loop through frames to extract brightness
frame_num = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    brightness.append(avg_brightness)
    timestamps.append(frame_num / fps)
    frame_num += 1

cap.release()

# Check if brightness data is populated
if len(brightness) == 0:
    print("Error: No brightness data was collected. Please check the video.")
    exit()

# Convert to numpy arrays for processing
brightness = np.array(brightness)
timestamps = np.array(timestamps)

# Optional: Smooth brightness data
window_size = 5  # Smoothing window size
brightness_smoothed = np.convolve(brightness, np.ones(window_size) / window_size, mode='same')

# Blink detection (using scipy's find_peaks)
min_distance = max(1, int(fps * 0.2))  # Blink sensitivity
peaks, _ = find_peaks(brightness_smoothed, distance=min_distance, prominence=0.05)  # Detecting blinks
print(f"🔢 Total Blinks Detected: {len(peaks)}")

# Extract LED color from the filename (e.g., "yellow" from "led_yellow.mp4")
led_color = extract_color_from_filename(video_path)

# Save the blink data to CSV
save_blink_data(led_color, timestamps, peaks)

# Generate filename dynamically based on the LED color
output_filename = f"led_{led_color}_blink_detection.png"

# Plot the graph with dynamic title and save it as a PNG file
plt.figure(figsize=(10, 5))
plt.plot(timestamps, brightness, label='Brightness', alpha=0.6)
plt.plot(timestamps, brightness_smoothed, label='Smoothed Brightness', linewidth=2)
plt.plot(timestamps[peaks], brightness[peaks], "ro", label='Detected Blinks')

# Set the plot title dynamically based on the LED color
plt.title(f'{led_color.capitalize()} LED Blink Timeline')
plt.xlabel('Time (s)')
plt.ylabel('Brightness')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the figure with the dynamically generated filename
plt.savefig(output_filename)
print(f"Graph saved as: {output_filename}")
