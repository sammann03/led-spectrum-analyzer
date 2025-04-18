import os
import csv
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Function to load blink data from CSV
def load_blink_data(filename="blink_data.csv"):
    blink_data = {}
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                color = row[0]
                timestamps = np.array([float(ts) for ts in row[1:]])
                blink_data[color] = timestamps
    else:
        print(f"❌ {filename} not found.")
    return blink_data

# Function to create audio based on blink timestamps
def create_audio(blink_timestamps, output_filename="blinks_audio.wav", beep_duration=0.1, beep_freq=1000, sample_rate=44100):
    if len(blink_timestamps) == 0:
        print("❌ No blinks detected. No audio will be generated.")
        return

    # Calculate the total duration of the audio
    max_time = blink_timestamps[-1] + beep_duration  # Last blink time plus beep duration
    audio = np.zeros(int(max_time * sample_rate))  # Create an empty audio array

    # For each blink timestamp, generate a beep and place it in the audio array
    for blink_time in blink_timestamps:
        start_sample = int(blink_time * sample_rate)
        end_sample = start_sample + int(beep_duration * sample_rate)
        t = np.linspace(0, beep_duration, int(beep_duration * sample_rate), endpoint=False)
        beep = np.sin(2 * np.pi * beep_freq * t)  # Sine wave for the beep
        audio[start_sample:end_sample] = beep

    # Save the audio to a WAV file
    wav.write(output_filename, sample_rate, (audio * 32767).astype(np.int16))  # Convert to 16-bit PCM
    print(f"🔊 Audio saved as: {output_filename}")

# Function to plot the blink data
def plot_blink_data(blink_timestamps, color):
    plt.figure(figsize=(10, 5))
    plt.plot(blink_timestamps, np.ones_like(blink_timestamps), 'ro', label=f'{color.capitalize()} Blinks')
    plt.title(f'{color.capitalize()} LED Blink Detection')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    output_filename = f"led_{color}_blink_detection.png"
    plt.savefig(output_filename)
    print(f"Graph saved as: {output_filename}")

# Main function to generate audio from graph
def main():
    blink_data = load_blink_data()

    for color, timestamps in blink_data.items():
        if len(timestamps) > 0:
            print(f"🔢 Total Blinks Detected for {color}: {len(timestamps)}")

            # Plot the blink data for visualization
            plot_blink_data(timestamps, color)

            # Create audio from blink timestamps
            create_audio(timestamps, output_filename=f"led_{color}_blinks_audio.wav")

        else:
            print(f"❌ No blink data found for {color}. Skipping audio generation.")

if __name__ == "__main__":
    main()
