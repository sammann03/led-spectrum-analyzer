import pandas as pd
import matplotlib.pyplot as plt
import os

colors = ['red', 'green', 'yellow', 'blue']

for color in colors:
    real_brightness_file = f'{color}_real.csv'
    theoretical_file = f'spec_{color}.csv'

    if not os.path.exists(real_brightness_file):
        print(f"⚠️ Skipping {color.upper()} (real CSV missing)")
        continue

    if not os.path.exists(theoretical_file):
        print(f"⚠️ Skipping {color.upper()} (theoretical CSV missing)")
        continue

    # Load data
    real_df = pd.read_csv(real_brightness_file)
    theo_df = pd.read_csv(theoretical_file)

    # Align data length
    min_len = min(len(real_df), len(theo_df))
    real_df = real_df.iloc[:min_len]
    theo_df = theo_df.iloc[:min_len]

    # Extract and normalize
    time = real_df['Time']
    real_vals = real_df.iloc[:, 1].values  # Brightness or Frequency
    theo_vals = theo_df.iloc[:, 1].values  # Brightness or Frequency

    # Overlay Graph
    plt.plot(time, theo_vals, label='Theoretical', linestyle='--', color='black')
    plt.plot(time, real_vals, label='Real', alpha=0.7)
    plt.title(f'{color.upper()} – Real vs Theoretical')
    plt.xlabel('Time (s)')
    plt.ylabel('Brightness / Frequency')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'comparison_{color}.png', dpi=300)
    plt.clf()

    # Delta Graph
    delta = real_vals - theo_vals
    plt.plot(time, delta, label='Δ Real - Theoretical', color='purple')
    plt.title(f'{color.upper()} – Difference Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Difference')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'difference_{color}.png', dpi=300)
    plt.clf()

    # Combined CSV export
    comp_df = pd.DataFrame({
        'Time': time,
        'Theoretical': theo_vals,
        'Real': real_vals,
        'Delta': delta
    })
    comp_df.to_csv(f'comparison_table_{color}.csv', index=False)
    print(f"✅ Comparison complete for {color.upper()}")
