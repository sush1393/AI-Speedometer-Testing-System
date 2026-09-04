
import easyocr
import re

# Initialize OCR
reader = easyocr.Reader(['en'])

# Image Path
img_path = input("Enter image path: ")

# Read text from image
result = reader.readtext(img_path, detail=0)

print("OCR Raw Output:", result)

# Extract numbers
numbers = []

for text in result:
    found = re.findall(r'\d+', text)
    numbers.extend(found)

print("Detected Numbers:", numbers)

if len(numbers) == 0:
    print("No numbers detected!")
    exit()

# Select largest detected number as speed
detected_speed = int(max(numbers, key=len))

# Reference speed input
reference_speed = int(input("Enter reference speed: "))

# Error calculation
error = abs(reference_speed - detected_speed)
error_percent = (error / reference_speed) * 100

status = "PASS" if error_percent < 5 else "FAIL"

print("\n----------------------------")
print("SPEEDOMETER TEST REPORT")
print("----------------------------")
print("Detected Speed :", detected_speed)
print("Reference Speed:", reference_speed)
print("Error %        :", round(error_percent, 2))
print("Status         :", status)
print("----------------------------")
