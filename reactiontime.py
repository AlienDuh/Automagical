import Quartz
import threading
import time

NORMAL_GREEN = 0
FAST_GREEN = 145
THRESHOLD = 4
SAMPLE_DELAY = 0  # No delay

# Shared variables
current_g = None
current_pos = (0, 0)
lock = threading.Lock()
running = True

def get_pixel_color(x, y):
    region = Quartz.CGRectMake(x, y, 1, 1)
    img = Quartz.CGWindowListCreateImage(region, Quartz.kCGWindowListOptionOnScreenOnly,
                                         Quartz.kCGNullWindowID, Quartz.kCGWindowImageDefault)
    bitmap = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(img))
    pixel = list(bitmap)
    return pixel[1], pixel[2], pixel[3]  # R, G, B (BGRA on macOS)

def close_enough(val, target):
    return abs(val - target) <= THRESHOLD

def fast_click():
    loc = Quartz.NSEvent.mouseLocation()
    for _ in range(2):
        Quartz.CGEventPost(Quartz.kCGHIDEventTap,
            Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, loc, Quartz.kCGMouseButtonLeft))
        Quartz.CGEventPost(Quartz.kCGHIDEventTap,
            Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, loc, Quartz.kCGMouseButtonLeft))

def normal_click():
    loc = Quartz.NSEvent.mouseLocation()
    Quartz.CGEventPost(Quartz.kCGHIDEventTap,
        Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, loc, Quartz.kCGMouseButtonLeft))
    Quartz.CGEventPost(Quartz.kCGHIDEventTap,
        Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, loc, Quartz.kCGMouseButtonLeft))

# Background reader
def reader():
    global current_g, current_pos, running
    while running:
        loc = Quartz.NSEvent.mouseLocation()
        x, y = int(loc.x), int(Quartz.CGDisplayPixelsHigh(0) - loc.y)  # Flip y-axis on macOS
        try:
            _, g, _ = get_pixel_color(x, y)
        except Exception:
            continue
        with lock:
            current_g = g
            current_pos = (x, y)
        if SAMPLE_DELAY > 0:
            time.sleep(SAMPLE_DELAY)

# Start background thread
thread = threading.Thread(target=reader, daemon=True)
thread.start()

# Main loop: acts on latest G value
try:
    while True:
        with lock:
            g = current_g
        if g is None:
            continue

        if close_enough(g, NORMAL_GREEN):
            normal_click()
        elif close_enough(g, FAST_GREEN):
            fast_click()

        # Don’t hog 100% CPU but still fast
        time.sleep(0.0005)

except KeyboardInterrupt:
    running = False
    thread.join()
