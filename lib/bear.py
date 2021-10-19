#!/usr/bin/env python
import os
import subprocess
import time

from servo import Servo
from random import randint
from threading import Thread

class Bear:
  def __init__(self, config, audio):

    self.isRunning = False

    # attach audio player
    self.audio = audio

    # add list of supported phrases
    self.phrases = config.phrases

    # bind mouth and eye servos based on pins defined in config
    self.eyes = Servo(
      pwm_pin=config.getint('pins', 'pwma'),
      dir_pin=config.getint('pins', 'ain1'),
      cdir_pin=config.getint('pins', 'ain2'),
      duration=config.getfloat('settings', 'eyes_duration'),
      speed=config.getint('settings', 'eyes_speed'),
      label='eyes'
    )

    self.mouth = Servo(
      pwm_pin=config.getint('pins', 'pwmb'),
      dir_pin=config.getint('pins', 'bin1'),
      cdir_pin=config.getint('pins', 'bin2'),
      duration=config.getfloat('settings', 'mouth_duration'),
      speed=config.getint('settings', 'mouth_speed'),
      label='mouth'
    )

    self.mouth.close()
    self.mouthThread = Thread(target=self.__updateMouth)
    print("bear constructor finished")

  def __del__(self):
    print("bear deconstructor finished")

  def activate(self):
    self.isRunning = True
    self.mouthThread.start()
    print("bear instance activated")

  def deactivate(self):
    self.isRunning = False
    print("bear instance deactivated")

  def __updateMouth(self):
    while self.isRunning:
      if self.mouth.to == 'open' and self.mouth.state != 'open':
          self.mouth.open()
      elif self.mouth.to =='closed' and self.mouth.state != 'closed':
          self.mouth.close()

  def update(self, data):
    if('eyes' in data['bear']):
      if data['bear']['eyes']['to']: self.eyes.to=data['bear']['eyes']['to']
    if('mouth' in data['bear']):
      if data['bear']['mouth']['to']: self.mouth.to=data['bear']['mouth']['to']
    return self.getStatus()

  def getStatus(self):
    print(self)
    return { "bear": { "eyes": { "state": self.eyes.state }, "mouth": { "state": self.mouth.state } } }

  def play(self, filename):
    self.isTalking = True
    self.audio.play("public/sounds/"+filename+".wav")
    self.isTalking = False

  def say(self, text):
    # Sometimes the beginning of audio can get cut off. Insert silence.
    os.system( "espeak \",...\" 2>/dev/null" )
    time.sleep( 0.5 )
    # TODO: make speech params configurable
    subprocess.call([
      "espeak", 
      "-w","speech.wav",
      "-s","125", 
      "-v","en+m3",
      "-p","25",
      "-a","150", 
      text
    ])
    self.audio.play("speech.wav")

