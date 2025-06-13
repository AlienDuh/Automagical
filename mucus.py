import mss
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from pix2tex.cli import LatexOCR

def extract_text_and_latex(img):
    # Step 1: Convert to grayscale
    gray = ImageOps.grayscale(img)

    # Step 2: Threshold for detecting math regions
    binary = gray.point(lambda p: 255 if p > 180 else 0)
    np_img = np.array(binary)

    # Step 3: Find bounding box of non-white pixels (math area)
    coords = np.column_stack(np.where(np_img < 255))

    if coords.size == 0:
        print("❌ No LaTeX detected.")
        return pytesseract.image_to_string(img), ""  # fallback

    # Bounding box of LaTeX region
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    latex_box = (x_min, y_min, x_max + 1, y_max + 1)

    # Crop LaTeX area
    latex_img = img.crop(latex_box)

    # Create mask for LaTeX area, then extract regular text
    mask_img = Image.new("L", img.size, 255)
    mask_img.paste(0, latex_box)
    text_only_img = Image.composite(img, Image.new("RGB", img.size, (255, 255, 255)), mask_img)

    # Step 4: OCR
    regular_text = pytesseract.image_to_string(text_only_img)
    model = LatexOCR()
    latex_text = model(latex_img)

    return regular_text.strip(), latex_text.strip()

# Define region of interest
x1, y1, x2, y2 = 587, 417, 1554, 948

# Capture screen region
with mss.mss() as sct:
    monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
    screenshot = sct.grab(monitor)
    img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)

# Extract
regular_text, latex_text = extract_text_and_latex(img)

# Output
print("📝 Problem Text:")
print(regular_text)
print("\n🧮 LaTeX Expression:")
print(latex_text)
