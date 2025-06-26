
"""
Image to PDF Converter
Improvements:
1. Filters only image files (jpg, jpeg, png, bmp, gif).
2. Maintains aspect ratio and centers images on A4.
3. Adds error handling for file issues.
4. Allows user to specify input directory and output filename via command-line arguments.
5. Uses natural sorting for filenames.
"""

import os
import argparse
from fpdf import FPDF
from PIL import Image
import re

# Natural sort helper
def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif"))

def main():
    parser = argparse.ArgumentParser(description="Convert images in a folder to a single PDF.")
    parser.add_argument('-i', '--input', type=str, default='convert/', help='Input directory with images')
    parser.add_argument('-o', '--output', type=str, default='output.pdf', help='Output PDF filename')
    args = parser.parse_args()

    path = args.input
    output_pdf = args.output

    try:
        img_list = [f for f in os.listdir(path) if is_image(f)]
    except Exception as e:
        print(f"Error reading directory: {e}")
        return

    if not img_list:
        print("No image files found in the specified directory.")
        return

    img_list.sort(key=natural_key)

    pdf = FPDF("P", "mm", "A4")
    page_w, page_h = 210, 297

    for img_name in img_list:
        img_path = os.path.join(path, img_name)
        try:
            with Image.open(img_path) as img:
                img_w, img_h = img.size
                # Calculate new size to fit A4 while maintaining aspect ratio
                ratio = min(page_w / img_w, page_h / img_h)
                new_w = img_w * ratio
                new_h = img_h * ratio
                x = (page_w - new_w) / 2
                y = (page_h - new_h) / 2
        except Exception as e:
            print(f"Skipping {img_name}: {e}")
            continue

        pdf.add_page()
        try:
            pdf.image(img_path, x, y, new_w, new_h)
        except Exception as e:
            print(f"Error adding {img_name} to PDF: {e}")

    try:
        pdf.output(output_pdf, "F")
        print(f"PDF created successfully: {output_pdf}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

if __name__ == "__main__":
    main()   

