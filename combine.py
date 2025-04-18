import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

colors = ['red', 'green', 'yellow', 'blue']
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('LED Brightness/Frequency – Real vs Theoretical Comparison', fontsize=16)

for idx, color in enumerate(colors):
    img_path = f'comparison_{color}.png'
    if not os.path.exists(img_path):
        print(f"⚠️ Missing {img_path}, skipping subplot.")
        continue

    img = mpimg.imread(img_path)
    row, col = divmod(idx, 2)
    axs[row][col].imshow(img)
    axs[row][col].axis('off')
    axs[row][col].set_title(color.upper())

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('comparison_grid.png', dpi=300)
print("✅ Saved: comparison_grid.png")
