from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import Quartz
import time

keyboard = KeyboardController()
mouse = MouseController()

# Key mapping based on character, not hex codes
key_map = {
    'w': 'w',
    'a': 'a',
    's': 's',
    'd': 'd',
    'm': 'm',
    'k': 'k'
}

def PressKey(k):
    keyboard.press(key_map[k])

def ReleaseKey(k):
    keyboard.release(key_map[k])

def click(x, y):
    moveMouseTo(x, y)
    time.sleep(0.01)
    mouse.click(Button.left, 1)

def moveMouseTo(x, y):
    # Mac screen origin is bottom-left, Quartz needs this
    Quartz.CGWarpMouseCursorPosition((x, y))
    Quartz.CGAssociateMouseAndMouseCursorPosition(True)

def queryMousePosition():
    loc = Quartz.NSEvent.mouseLocation()
    return int(loc.x), int(loc.y)  # top-left origin
