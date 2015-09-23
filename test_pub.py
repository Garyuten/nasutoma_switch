#!/usr/bin/env python
# coding=utf-8
# ======== 送信テスト用 =========
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import threading
import time
import wave
import time
import json

HOST_NAME = "cgfm.jp"

STATUS_PUB = 0
STATUS_SUB = 0

"""
サーバーに送信する
"""
def publish_mqtt(msg):
  try:
    STATUS_PUB = 1
    print "try publish_mqtt=" + msg
    publish.single(
      "messageID",
      client_id="1",
      payload=msg,
      hostname=HOST_NAME)
    print "publish mqtt time %f"
    print "payload=" + msg
  except IOError:
    print "publish error."
    STATUS_PUB = 0
    
  #when pressing CTRL-c 
  except KeyboardInterrupt:
    print "KeyboardInterrupt Success"
  except:
    print "Something else"
  finally:
    print "Finally"


"""
接続完了
"""
def on_connect(mqttc, obj, rc):
  mqttc.subscribe("$SYS/#", 0)
  print("rc: " + str(rc))
    
"""
受信したメッセージ
"""
def on_message(mqttc, obj, msg):
  global STATUS_PUB,STATUS_SUB
#  print("msg:"+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
  if msg.topic == "messageID":
    myName = "test_pub"
    yourName = str(msg.payload).split("::")
    print("msg.payload = "+ msg.payload )
    print("len(yourName) :"+ str(len(yourName)) )
    if len(yourName) >= 2 :
      print("yourName:"+yourName[1])
      print("publish %s" % msg)
      if myName != yourName[1]:
        print("違う機種からのメッセージ")

        
"""
publishした情報
"""
def on_publish(mqttc, obj, mid):
  print("mid: " + str(mid))
"""
"""
def on_subscribe(mqttc, obj, mid, granted_qos):
  print("Subscribed: " + str(mid) + " " + str(granted_qos))
"""
ログ
"""
def on_log(mqttc, obj, level, string):
  print("log:" + string)
	



try:
  #MQTT待機
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

#when pressing CTRL-c 
except KeyboardInterrupt:
  print "MQTT - KeyboardInterrupt Success"
  mqttc.loop_stop(force=False)
except:
  print "MQTT - Something else"
finally:
  mqttc.loop_stop(force=False)
  print "MQTT - Finally"



#送信
publish_mqtt("knock from ::test_pub")


#待機開始
try:
  mqttc.loop_forever()
#when pressing CTRL-c 
except KeyboardInterrupt:
  mqttc.loop_stop(force=False)
  print "MQTT - loop - KeyboardInterrupt Success"
except Exception as e:
  print "MQTT - loop - e.message : " + e.message
except:
  print "MQTT - loop - Something else"
finally:
#  mqttc.loop_stop(force=False)
#  GPIO.cleanup()
  print "MQTT - loop - Finally"