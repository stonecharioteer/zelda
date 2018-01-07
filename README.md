# Zelda

**A Google Voice Hat Experiment**

------------------

Zelda is my personal voice assistant that I'm setting up to work for me around the house. She is named after Zelda Fitzgerald.


## Hardware:


Zelda runs off a Raspberry Pi with a Voice hat. It uses the assistant API to convert speech to text, and the google Speech API to convert
text to speech, but the keyword recognition and actions are coded using pure python.

Any hardware that I will be linking Zelda to, like the Rocket Andon signal, will run off a NodeMCU running my own arduino code.

Check the ``andon`` project for more details about how I've adapted the Google Paper Signal idea for my own purposes.


## Software:

Zelda is written in Python and relies on the Google aiy module for STT. I chose the ``google_speech`` python module for TTS, 
because being able to play around with the language settings, the accent and the access to libSOX is amazing.

I personally like that module better than ``aiy.voice.say``, because it doesnt' sound **as** robotic.

## TODO:

    [*] Scan Wifi constantly to see if I've connected so it can greet me.
    [*] Build a corpus of poems from Gutenburg so it can wake me up with a morning poem.
    [*] Do the same for random quotes from Goodreads.
    [*] Scan Amazon and tell me if a particular product's price has reduced drastically.
    [*] Log conversations and present the log via a REST API.
    [?] Allow for connecting to different WiFi signals through voice.
    [*] Use ``tomodachi`` so that it tells me if a new One Piece Chapter is out.
    [!] Use ``nltk`` to build a decent conversation bot.
    [*] Allow entry and query to Goodreads or to a private repository of my Books.

-------------------------    


