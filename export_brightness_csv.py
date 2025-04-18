import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import find_peaks

video_map = {
    'red': 'led_red.mp4',
    'green': 'led_green.mp4',
    'yellow': 'led_yellow.mp4',
    'blue': 'led_blue.mp4'
}

for color, filename in video_map.items():
    if not os.path.exists(filename):
        print(f"⚠️ Skipping {filename} (not found)")
        continue

    print(f"📦 Processing {color.upper()} from {filename}")
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    brightness = []
    times = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        brightness.append(mean_brightness)
        times.append(frame_count / fps)
        frame_count += 1

    cap.release()

    # Increase the smoothing window size (e.g., 20 frames for moving average)
    brightness_smooth = np.convolve(brightness, np.ones(20)/20, mode='same')

    # Save brightness timeline CSV
    df = pd.DataFrame({'Time': times, 'Brightness': brightness_smooth})
    df.to_csv(f'{color}_real.csv', index=False)
    print(f"✅ Saved {color}_real.csv")

    # Plot regular brightness timeline
    plt.plot(times, brightness_smooth)
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.title(f'Brightness vs Time - {color.upper()}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'brightness_timeline_{color}.png', dpi=300)
    plt.clf()

    # Debug plot to visualize raw and smoothed signal
    plt.plot(times, brightness, label='Raw')
    plt.plot(times, brightness_smooth, label='Smoothed', linestyle='--')
    plt.title(f'[DEBUG] Brightness Timeline - {color.upper()}')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'debug_brightness_{color}.png', dpi=300)
    plt.clf()

    # Blink detection using further reduced prominence
    brightness_np = np.array(brightness_smooth)
    adaptive_prominence = max(1.0, np.std(brightness_np) * 0.3)  # Further reduced prominence
    peaks, _ = find_peaks(brightness_np, prominence=adaptive_prominence, distance=fps * 0.1)
    blink_times = [times[p] for p in peaks]

    # Plot detected blinks on the brightness graph
    plt.plot(times, brightness_smooth, label='Brightness')
    plt.scatter([times[p] for p in peaks], [brightness_smooth[p] for p in peaks], color='red', label='Detected Blinks')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.title(f'Blink Detection - {color.upper()}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'blink_detection_{color}.png', dpi=300)
    plt.clf()

    # Save blink timestamps
    pd.DataFrame({'Blink Time (s)': blink_times}).to_csv(f'blinks_{color}.csv', index=False)
    print(f"🔁 {color.upper()}: {len(peaks)} blinks detected with adaptive prominence = {adaptive_prominence:.2f}")
