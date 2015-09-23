#!/usr/bin/env python
# coding=utf-8
import RPi.GPIO as GPIO
import time

pin_led = 11
pin_button = 15

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin_led, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(pin_led, 0)
#GPIO.output(pin_led, GPIO.LOW)

time.sleep(1)
#print GPIO.input(pin_button)

while True :
  ButtonInput = GPIO.input(pin_button)
  print GPIO.input(pin_button)
#  print ButtonInput
  if ButtonInput != True:
    print "button pressed"
    GPIO.output(pin_led, 1)
    time.sleep(0.1)
  else:
    print "button"
    GPIO.output(pin_led, 0)
#    time.sleep(0.11)
  
  time.sleep(0.2)

GPIO.cleanup()
#time.sleep(5)
