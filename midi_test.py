#!/usr/bin/env python3
from aiy.toneplayer import TonePlayer
from aiy.leds import Leds

from gpiozero import Button
from time import sleep
import time
import os

import pygame
import pygame.midi
from time import sleep

BUZZER_GPIO = 22
BUTTON_GPIO = 23

toneplayer = TonePlayer(BUZZER_GPIO)
leds = Leds()
button = Button(BUTTON_GPIO)

instrument = 2

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
        print("process")

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
        pygame.midi.quit()
        pass

if __name__ == '__main__':
    print("Start program")
    pygame.init()
    pygame.midi.init()

    for i in range(pygame.midi.get_count()):
        interf, name, input_dev, output_dev, opened = pygame.midi.get_device_info(i)
        if output_dev and b'NSX-39 ' in name:
            midiOutput = pygame.midi.Output(i)

    midiOutput.set_instrument(instrument)

    midiOutput.write_sys_ex(0, b'\xF0\x43\x09\x11\x0A\x00\x70\x43\x64\x43\x25\x4E\x7B\x65\x18\x71\x43\x6E\x04\x04\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x6F) # reverb

    midiOutput.note_on(74,80)
    sleep(.500)

    midiOutput.note_off(74,80)

    main()
