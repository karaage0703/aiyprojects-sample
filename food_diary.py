#!/usr/bin/env python3
from PIL import Image

from aiy.vision.inference import ImageInference
from aiy.vision.models import dish_classifier
from aiy.toneplayer import TonePlayer
from aiy.vision.leds import Leds

from gpiozero import Button
from time import sleep
import picamera
from slacker import Slacker
import time
import os

BUZZER_GPIO = 22
BUTTON_GPIO = 23

slack = Slacker('xxx')
toneplayer = TonePlayer(BUZZER_GPIO)
leds = Leds()
button = Button(BUTTON_GPIO)

photo_filename = 'dish.jpg'
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
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.start_preview()
            sleep(3.000)
            camera.capture(photo_filename)

        leds.update(Leds.rgb_on(GREEN))
        print("Dish classifier")
        with ImageInference(dish_classifier.model()) as inference:
            image = Image.open(photo_filename)
            classes = dish_classifier.get_classes(
                inference.run(image), max_num_objects=5, object_prob_threshold=0.1)
            dish_name = ''
            for i, (label, score) in enumerate(classes):
                dish_name += label + '/'
                print('Result %d: %s (prob=%f)' % (i, label, score))

        leds.update(Leds.rgb_on(BLUE))
        print("Post to slack")
        slack.files.upload(photo_filename, channels='#food_diary', title=dish_name)

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
    main()
