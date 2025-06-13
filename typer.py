from PIL import ImageGrab,Image
import pytesseract
import pyautogui
import keyboard
import time
import easyocr
import cv2
import sys
#configs and setup for monkeytype
x1=168
y1=430
x2=1750
y2=600

#humanbenchmark typing test
# x1=168
# y1=430
# x2=1750
# y2=650
time.sleep(1)

while True:
    pyautogui.leftClick(951, 592)
    time.sleep(1)
    screenshot = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    screenshot.save("region_capture.png")
    #sys.exit()
    img = Image.open("region_capture.png")
    sys.exit()
    #gray = img.convert('L')
    #bw = gray.point(lambda x: 0 if x < 200 else 255, '1')
    text = pytesseract.image_to_string(img).replace('\n', ' ').strip()
    print(text)
    keyboard.write(text, delay=0.1)

    time.sleep(1)
    pyautogui.leftClick(704,674)
    time.sleep(1)


