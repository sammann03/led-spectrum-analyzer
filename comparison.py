import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

# Function to extract color from filename (like 'led_blue.mp4' -> 'blue')
def extract_color_from_filename(filename):
    color = filename.split('_')[1].replace('.mp4', '')
    return color

# Function to compute and plot STFT for a video
def compute_stft_for_video(video_path):
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
        avg_brightness = np.mean(gray)
        brightness.append(avg_brightness)
        timestamps.append(frame_num / fps)
        frame_num += 1
    
    cap.release()
    
    brightness = np.array(brightness)
    timestamps = np.array(timestamps)
    
    # Compute STFT (Short-Time Fourier Transform)
    f, t, Zxx = stft(brightness, fs=fps, nperseg=100)
    
    return f, t, np.abs(Zxx)  # Return frequency, time, and magnitude of STFT

# Load and compute STFT for multiple LED videos
led_videos = ['led_blue.mp4', 'led_red.mp4', 'led_green.mp4', 'led_yellow.mp4']  # Replace with your actual video filenames

plt.figure(figsize=(15, 10))

for idx, video_path in enumerate(led_videos):
    # Get color from filename
    led_color = extract_color_from_filename(video_path)
    
    # Compute STFT for this video
    f, t, Zxx = compute_stft_for_video(video_path)
    
    # Plot STFT for each LED
    plt.subplot(2, 2, idx + 1)
    plt.pcolormesh(t, f, Zxx)
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.title(f'{led_color.capitalize()} LED STFT')
    plt.colorbar(label='Magnitude')
    
# Save the figure as a PNG file instead of showing it interactively
plt.tight_layout()
plt.savefig('stft_comparison.png')  # Save the figure as a PNG file
print("STFT comparison saved as 'stft_comparison.png'")
