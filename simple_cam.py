#!/usr/bin/env python3
from aiy.toneplayer import TonePlayer
from aiy.leds import Leds

from gpiozero import Button
from time import sleep
import time
import os

import shutter as sh

BUZZER_GPIO = 22
BUTTON_GPIO = 23

toneplayer = TonePlayer(BUZZER_GPIO)
leds = Leds()
button = Button(BUTTON_GPIO)

BEEP_SOUND = ('E6q', 'C6q')
RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
WHITE = (0xFF, 0xFF, 0xFF)

def KeepWatchForSeconds(seconds):
    GoFlag = True
    while seconds > 0:
        time.sleep(0.1)
        seconds -= 0.1
        if not button.is_pressed:
            GoFlag = False
            break
    return GoFlag

def run():
    if KeepWatchForSeconds(3):
        print("Going shutdown by GPIO")
        leds.update(Leds.rgb_off())
        os.system("/sbin/shutdown -h now 'Poweroff by GPIO'")

    else:
        print("Beep sound")
        toneplayer.play(*BEEP_SOUND)

        leds.update(Leds.rgb_on(RED))
        print("Taking photo")
        sh.cameraLoad()
        sh.shutter()
        sh.cameraSave()

        print("Done")
        leds.update(Leds.rgb_on(WHITE))

def main():
    button.when_pressed = run
    leds.update(Leds.rgb_on(WHITE))

    try:
        while True:
            pass
    except KeyboardInterrupt:
        leds.update(Leds.rgb_off())
        pass

if __name__ == '__main__':
    print("Start program")

    sh.photodirCheck()
    sh.cameraLoad()
 
    main()
