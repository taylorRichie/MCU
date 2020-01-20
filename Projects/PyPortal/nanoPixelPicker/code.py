import time
import board
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import neopixel
import analogio
import terminalio
import displayio



#FONT
font = bitmap_font.load_font("/fonts/Arial-12.bdf")
my_display_group = displayio.Group(max_size=25)
board.DISPLAY.show(my_display_group)




# Set the background color
BACKGROUND_COLOR = 0x443355

# Set the NeoPixel brightness
BRIGHTNESS = 0.1

light_sensor = analogio.AnalogIn(board.LIGHT)

strip_1 = neopixel.NeoPixel(board.D4, 16, brightness=BRIGHTNESS)
strip_2 = neopixel.NeoPixel(board.D3, 16, brightness=BRIGHTNESS)

# Turn off NeoPixels to start
strip_1.fill(1)
#strip_2.fill(0)

# Setup PyPortal without networking
pyportal = PyPortal(default_bg=BACKGROUND_COLOR)

# Button colors
RED = (255, 0, 0)
ORANGE = (255, 34, 0)
YELLOW = (255, 170, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
VIOLET = (153, 0, 255)
MAGENTA = (255, 0, 51)
PINK = (255, 51, 119)
AQUA = (85, 125, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

my_label = Label(terminalio.FONT, text="My Label Text", color=AQUA)
my_display_group.append(my_label)

spots = [
    {'label': "1", 'pos': (10, 10), 'size': (60, 20), 'color': AQUA},
    {'label': "2", 'pos': (90, 10), 'size': (60, 20), 'color': ORANGE},
    {'label': "3", 'pos': (170, 10), 'size': (60, 20), 'color': YELLOW},
    {'label': "4", 'pos': (250, 10), 'size': (60, 20), 'color': WHITE},
    {'label': "5", 'pos': (10, 40), 'size': (60, 20), 'color': OFF}
    ]

buttons = []
for spot in spots:
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.SHADOWROUNDRECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['label'])
    pyportal.splash.append(button.group)
    buttons.append(button)

my_button = Button(x=20, y=200, width=80, height=40,
                   label="My Button", label_font=font)

mode = 0
mode_change = None

# Calibrate light sensor on start to deal with different lighting situations
# If the mode change isn't responding properly, reset your PyPortal to recalibrate
initial_light_value = light_sensor.value
while True:
    if light_sensor.value < (initial_light_value * 0.3) and mode_change is None:
        mode_change = "mode_change"
    if light_sensor.value > (initial_light_value * 0.5) and mode_change == "mode_change":
        mode += 1
        mode_change = None
        if mode > 2:
            mode = 0
        print(mode)
    touch = pyportal.touchscreen.touch_point
    if touch:
        for button in buttons:
            if button.contains(touch):
                print("Touched", button.name)
                if mode == 0:
                    strip_1.fill(button.fill_color)
                elif mode == 1:
                    strip_2.fill(button.fill_color)
                elif mode == 2:
                    strip_1.fill(button.fill_color)
                    strip_2.fill(button.fill_color)
                break
    time.sleep(0.05)
