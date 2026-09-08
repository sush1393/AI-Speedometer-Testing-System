import cv2
import easyocr
import torch
import numpy as np
import re
from ultralytics import YOLO

# Load your trained model (best.pt)
model = YOLO("best.pt")

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

def detect_speedometer(img):
    """Detect digital speedometer region"""
    results = model(img)
    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()
        for box in boxes:
            x1, y1, x2, y2 = map(int, box[:4])
            cropped = img[y1:y2, x1:x2]
            return cropped
    return None

print("🚗 AI-Based Vehicle Speedometer Testing System (Digital Only)")
print("Enter image path: ")

img_path = input("Image path: ").strip()

if not img_path:
    print("No image path provided!")
    exit()

img = cv2.imread(img_path)
if img is None:
    print("❌ Could not read image!")
    exit()

# Detect speedometer
cropped_img = detect_speedometer(img)

if cropped_img is None:
    print("❌ Speedometer not detected!")
    exit()

# OCR on cropped image
result = reader.readtext(cropped_img, detail=0)

# Extract numbers
numbers = []
for text in result:
    found = re.findall(r'\d+', text)
    numbers.extend(found)

print("📸 Detected Numbers:", numbers)

if len(numbers) == 0:
    print("No numbers detected!")
    exit()

detected_speed = int(max(numbers, key=len))
print(f"✅ Detected Speed: {detected_speed}")

reference_speed = int(input("Reference speed (e.g. 80): "))

error = abs(detected_speed - reference_speed)
error_percent = (error / reference_speed) * 100 if reference_speed != 0 else 0

status = "PASS" if error_percent < 5 else "FAIL"

print("\n" + "="*40)
print("🎯 SPEEDOMETER TESTING REPORT")
print("="*40)
print(f"Detected Speed   : {detected_speed}")
print(f"Reference Speed  : {reference_speed}")
print(f"Error %          : {round(error_percent, 2)}%")
print(f"Status           : {status}")
print("="*40)
