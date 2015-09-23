#!/usr/bin/env python
# coding=utf-8
#LED
import RPi.GPIO as GPIO
import time
#MQTT
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

HOST_NAME = "cgfm.jp"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
  
"""
LEDをOFF
"""
def led_off():
  print "LED OFF"
  GPIO.output(11, False)


"""
接続完了
"""
def on_connect(mqttc, obj, rc):
    mqttc.subscribe("$SYS/#", 0)
    print("rc: "+str(rc))


mqttc = paho.Client()
mqttc.connect(HOST_NAME, 1883, 60)
mqttc.subscribe("messageID", 0)
mqttc.loop_stop()
mqttc.disconnect()

led_off()

