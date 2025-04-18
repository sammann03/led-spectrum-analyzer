import numpy as np
import matplotlib.pyplot as plt

def gaussian(wavelengths, peak, fwhm):
    sigma = fwhm / 2.355
    return np.exp(-0.5 * ((wavelengths - peak) / sigma) ** 2)

# -------- LED SPECTRUM DATA --------
leds = {
    "Red":    (630, 20),
    "Green":  (525, 35),
    "Yellow": (590, 30),
    "White":  (550, 150),  # Broad white spectrum approximation
}

wavelengths = np.linspace(400, 700, 1000)

# -------- PLOT --------
for name, (peak, fwhm) in leds.items():
    intensity = gaussian(wavelengths, peak, fwhm)
    plt.plot(wavelengths, intensity, label=f"{name} LED")

plt.xlabel("Wavelength (nm)")
plt.ylabel("Relative Intensity")
plt.title("Simulated LED Emission Spectra")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("led_spectra_simulation.png")

