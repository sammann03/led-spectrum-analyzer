# 🔦 LED Bandwidth & Blink Frequency Analysis

This project analyzes the blinking behavior and spectral characteristics of Red, Green, Blue, and Yellow LEDs using video footage and Python-based signal processing. It extracts brightness patterns, detects blinks, generates STFT frequency plots, compares data with theoretical spectra, and outputs a comprehensive report.

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `analyze_brightness.py` | Extract brightness from LED videos |
| `spectrum_brightness.py` | Extract online theoretical LED spectrum |
| `export_brightness_csv.py` | Export brightness data as CSV |
| `brightness_curve.py` | Plot brightness over time |
| `comparison.py` | Compare real vs theoretical data |
| `data_comparison.py` | Generate tabular spectrum comparison |
| `export_frequency_csv.py` | Export blink frequency data |
| `frequency_plot.py` | STFT-based frequency plots |
| `combine.py` | Merge visualizations |
| `generate_led_report.py` | Generate final PDF report |

---

## 🧠 Features

- 🔍 Auto blink detection
- 📊 Brightness + timeline visualization
- 🧠 Frequency analysis using STFT
- 📈 CSV & comparative plots for all LEDs
- 📄 One-click auto PDF report generation

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install opencv-python matplotlib numpy pandas scipy reportlab


▶️ Execution Order
python3 analyze_brightness.py
python3 spectrum_brightness.py
python3 export_brightness_csv.py
python3 brightness_curve.py
python3 comparison.py
python3 data_comparison.py
python3 export_frequency_csv.py
python3 frequency_plot.py
python3 combine.py
python3 generate_led_report.py

