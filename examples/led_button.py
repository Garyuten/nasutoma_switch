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
time.sleep(1)
print "--LED ON（ゆっくり）"
i = 0
n = 2
while True:
  i = i + 1
  GPIO.output(pin_led, True)
  time.sleep(0.8)
  GPIO.output(pin_led, False)
  time.sleep(0.4)
  if i >= n:
    break


while True :
  ButtonInput = GPIO.input(pin_button)
  print GPIO.input(pin_button)
#  print ButtonInput
  if ButtonInput != True:
    print "button pressed"
    GPIO.output(pin_led, 1)
    time.sleep(0.1)
    print "--LED ON（ゆっくり）"
    i = 0
    n = 2
    while True:
      i = i + 1
      GPIO.output(pin_led, True)
      time.sleep(0.8)
      GPIO.output(pin_led, False)
      time.sleep(0.4)
      if i >= n:
        break
  else:
    print "button"
    GPIO.output(pin_led, 0)
#    time.sleep(0.11)
  
  time.sleep(0.2)

GPIO.cleanup()
#time.sleep(5)
