from fpdf import FPDF
import os

# Define the LED colors
colors = ['red', 'green', 'blue', 'yellow']

# Define the specific image paths
paths = {
    'timeline': {
        'red': 'brightness_timeline_red.png',
        'green': 'brightness_timeline_green.png',
        'blue': 'brightness_timeline_blue.png',
        'yellow': 'brightness_timeline_yellow.png'
    },
    'comparison': {
        'red': 'comparison_red.png',
        'green': 'comparison_green.png',
        'blue': 'comparison_blue.png',
        'yellow': 'comparison_yellow.png'
    },
    'intensity': {
        'red': 'led_red_brightness_curve.png',
        'green': 'led_green_brightness_curve.png',
        'blue': 'led_blue_brightness_curve.png',
        'yellow': 'led_yellow_brightness_curve.png'
    },
    'audio': {
        'red': 'led_red_blink_detection.png',
        'green': 'led_green_blink_detection.png',
        'blue': 'led_blue_blink_detection.png',
        'yellow': 'led_yellow_blink_detection.png'
    }
}

# Create the PDF report
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for color in colors:
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"{color.upper()} LED REPORT", ln=True, align='C')

    for section, imgs in paths.items():
        image_path = imgs.get(color)
        if image_path and os.path.exists(image_path):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, f"{section.capitalize()} Analysis", ln=True)
            pdf.image(image_path, w=180)
        else:
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(200, 10, f"{section.capitalize()} image not found for {color}.", ln=True)

# Save the PDF
pdf.output("LED_Report_All_Colors.pdf")
print("✅ PDF generated: LED_Report_All_Colors.pdf")
