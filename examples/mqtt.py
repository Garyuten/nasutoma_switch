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
LEDを光らせる
"""
def led_on():
  print "--LED ON"
  while True:
      GPIO.output(11, True)
      time.sleep(0.3)
      GPIO.output(11, False)
      time.sleep(0.3)

"""
LEDをOFF
"""
def led_off():
  print "--LED OFF"
  GPIO.output(11, False)


"""
ボタン情報をサーバーに送信する
"""
def publish_mqtt():
	try:
		publish.single(
				"messageID",
				client_id="1",
				payload="hogehoge",
				hostname=HOST_NAME)
		print "publish mqtt time %f"
	except IOError:
		print "publish error."
		
"""
接続完了
"""
def on_connect(mqttc, obj, rc):
    mqttc.subscribe("$SYS/#", 0)
    print("rc: "+str(rc))
"""
受信したメッセージ
"""
def on_message(mqttc, obj, msg):
    print("msg:"+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if msg.topic == "messageID":
        print("publish %s" % msg)
    if msg.payload == "LED ON":
        led_on()
#        mqttc.loop_forever()
    elif msg.payload == "LED OFF":
        led_off()
#        mqttc.loop_forever()
        
        
"""
publishした情報
"""
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))
"""
"""
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
"""
ログ
"""
def on_log(mqttc, obj, level, string):
    print("log:"+string)
	



mqttc = paho.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.connect(HOST_NAME, 1883, 60)
mqttc.subscribe("messageID", 0)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

#送信
#publish_mqtt()

mqttc.loop_forever()