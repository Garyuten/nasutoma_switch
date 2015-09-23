#!/usr/bin/env python
# coding=utf-8
import RPi.GPIO as GPIO
import time

#MQTT
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

HOST_NAME = "cgfm.jp"


button = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN)


"""
ボタン情報をサーバーに送信する
"""
def publish_mqtt( msg ):
	try:
		publish.single(
				"messageID",
				client_id="1",
				payload= msg ,
				hostname=HOST_NAME)
		print "publish mqtt time %f"
		print "payload=" + msg
	except IOError:
		print "publish error."


#mqttc = paho.Client()
#mqttc.on_message = on_message
#mqttc.on_connect = on_connect
#mqttc.on_subscribe = on_subscribe
#mqttc.connect(HOST_NAME, 1883, 60)
#mqttc.subscribe("messageID", 0)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.


while GPIO.input(button) :
    pass
 
print "button pushed"
#送信
publish_mqtt("LED ON")
time.sleep(5)
publish_mqtt("LED OFF")
GPIO.cleanup()


#mqttc.loop_forever()