#!/home/vinay/AIY-voice-kit-python/env/bin/python
# -*- coding: utf-8 -*-

"""
ZELDA


2017-12-10
Vinay Keerthi
"""

import os
import time
import sys
sys.path.append("/home/vinay/AIY-voice-kit-python/src/")
import aiy.audio
import aiy.voicehat
import aiy.assistant.grpc

def launch_rocket():
    from urllib import request
    import time
    # 90 is base.
    # 0 is in the air.
    url = "http://nodemcu-02/SERVO=0"
    say("Launch sequence initiated.")
    colors = ["blue","yellow","red","green"]
    for i in reversed(range(10)):
        for color in colors:
            blink(color, 0.05)
        if i+1 <= 5:
            say(str(i+1))
        else:
            say("T minus {} seconds to launch.".format(str(i+1)))
        time.sleep(0.3)
    for color in colors:
        toggle_light(color, "ON")
    say("Houston, we have lift off!")
    request.urlopen(url)
    say("One small step for man and a giant leap for robot kind!")
    time.sleep(2)
    say("We're bringing her down!")
    url = "http://nodemcu-02/SERVO=90"
    request.urlopen(url)
    for color in reversed(colors):
        toggle_light(color, "OFF")


def toggle_light(color, state):
    from urllib import request

    url = "http://nodemcu-01/{}?COLOR={}".format(state.upper(), 
            color.upper())
    request.urlopen(url)

def blink(color, sleep=1):
    toggle_light(color,"ON")
    time.sleep(sleep)
    toggle_light(color, "OFF")

def say(text=None, lang="en", robot=False):
    import os
    from google_speech import Speech
    if text is None:
        say_fortune()
    elif text=="flipkart":
        say_fk_fortune()
    else:
        speech = Speech(text, lang)
        if not robot:
            sox_effects = ("speed","1.02")
        else:
            sox_effects = (
                    "speed 0.9 overdrive 10 echo 0.8 0.7 "
                    "6 0.7 echo 0.8 0.7 10 0.7 echo 0.8 0.7 "
                    "12 0.7 echo 0.8 0.88 12 0.7 echo 0.8 "
                    "0.88 30 0.7 echo 0.6 0.6 60 0.7"
                    ).split(" ")
        speech.play(sox_effects)
        print(text)
        # os.system("google_speech -l en '{}'".format(text.replace("'","")))

def say_fk_fortune():
    import random
    with open("quotes.txt", "r") as f:
        quotes = f.readlines()

    say(random.choice(quotes))

def say_fortune():
    import subprocess
    fortune = subprocess.check_output(["fortune"]).decode("utf-8").replace("\n","")
    for character in [".","?",";", ":","-"]:
        fortune = fortune.replace(character,character+"\n")
    for line in fortune.split("\n"):
        if line.strip() != "":
            say(line.strip())

def main_cloud():
    """Main function. Duh."""
    import aiy.cloudspeech
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase("Yabadabado")

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    led.set_state(aiy.voicehat.LED.BLINK)
    while True:
        try:
            say("Press the button")
            button.wait_for_press()
            led.set_state(aiy.voicehat.LED.ON)
            say("Say something!")
            text = recognizer.recognize()
            if text is None:
                say("I thought I told you to say something.")
            else:
                say('You said: {}'.format( text))
            led.set_state(aiy.voicehat.LED.OFF)
        except KeyboardInterrupt:
            led.set_state(aiy.voicehat.LED.OFF)
            led.set_state(aiy.voicehat.LED.BLINK)
            led.set_state(aiy.voicehat.LED.BLINK)
            break

    say("buh bye!")

def main_grpc():
    import aiy.assistant.grpc
    import time
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status("starting")
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.BLINK)
    time.sleep(1)
    led.set_state(aiy.voicehat.LED.OFF)
    say("Press the button and speak.")
    with aiy.audio.get_recorder():
        while True:
            try:
                status_ui.status("ready")
                button.wait_for_press()
                status_ui.status("listening")
                say("Listening...")
                text, audio = assistant.recognize()
                if text is not None:
                    if text == "goodbye":
                        status_ui.status("stopping")
                        say("Bye!")
                        break
                    elif "fortune" in text.lower():
                        say()
                    elif "flipkart" in text.lower():
                        say("flipkart")
                    elif "blink" in text.lower():
                        colors = ["RED","GREEN","BLUE","YELLOW"]
                        for color in colors:
                            if color.lower() in text.lower():
                                say("Blinking the {} light.".format(color.lower()))
                                blink(color)
                    elif "japanese" in text.lower():
                        say("konichiwa! watashiwa Google desu. Yoroshiku!", lang="ja")
                    elif "modi" in text.lower():
                        say("Seig Heil!", lang="de")
                    elif "rocket" in text.lower() or "launch" in text.lower():
                        launch_rocket()
                    elif "robot" in text.lower():
                        say("A robot? I am no robot!", robot=True)
                        say("Oops. I think I have a cold.")
                    else:
                        say("You said: {}. I need to ask Google to help me with that.".format(text))
                        if audio is None:
                            say("I did not get any response from Google.")
                        else:
                            try:
                                aiy.audio.play_audio(audio)
                            except:
                                say("There was some problem trying to say what Google wants me to say.")
                else:
                    say("I did not catch that boss.")
            except KeyboardInterrupt:
                led.set_state(aiy.voicehat.LED.OFF)
                say("I am done, boss!")
                break


if __name__ == "__main__":
    main_grpc()

