#!/usr/bin/python

import sys
import ConfigParser
import json
import os
import RPi.GPIO as GPIO

from lib.audioPlayer import AudioPlayer
from lib.bear import Bear
from lib.webFramework import WebFramework

# read main config file
config = ConfigParser.RawConfigParser()
config.read('config/main.cfg')

# read phrases config file
with open('config/phrases.json', 'r') as f:
  phrases = json.load(f)
  config.phrases = phrases

# init audio player & bear
audio = AudioPlayer()
bear = Bear(config, audio, GPIO)

# init web framework
web = WebFramework(bear)

GPIO.cleanup()

# sys.exit(1)
