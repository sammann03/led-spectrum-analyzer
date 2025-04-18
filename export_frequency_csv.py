import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
import pandas as pd
import os

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

    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    brightness = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness.append(np.mean(gray))

    cap.release()

    brightness = np.array(brightness)
    f, t, Zxx = stft(brightness, fs=fps, nperseg=64)
    dominant_freqs = np.abs(Zxx).max(axis=0)

    df = pd.DataFrame({'Time': t, 'Frequency': dominant_freqs})
    df.to_csv(f'{color}_real.csv', index=False)
    print(f"✅ Saved {color}_real.csv")

    plt.plot(t, dominant_freqs)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title(f'Dominant Frequency vs Time - {color.upper()}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'frequency_timeline_{color}.png', dpi=300)
    plt.clf()
