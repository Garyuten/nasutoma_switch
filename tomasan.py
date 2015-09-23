#!/usr/bin/env python
# coding=utf-8
# ======== 受信発信両用 =========
import os, sys
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import threading
import time
import pygame.mixer
import wave
import time
import json

time.sleep(0.3)
GPIO.cleanup()
time.sleep(0.3)

# ======= 設定 ==============

# 設定ファイル
#SETTING_FILE = os.path.dirname(__file__) + "/setting.json"
SETTING_FILE = "/home/pi/project1/setting.json"
#SETTING_FILE = os.abspath.dirname(__file__) + "/setting.json"
HOST_NAME = "cgfm.jp" # Mosquitto host
PIN_LED = 11
PIN_BUTTON = 15
led_flag = False

# 音関係
SOUND_FILE       = '/home/pi/project1/sounds/knock.wav' #音ファイル
SOUND_FILE_START = '/home/pi/project1/sounds/start.wav' #起動音
SOUND_FILE_SEND  = '/home/pi/project1/sounds/chime.mp3' #呼び出し音
SOUND_LOOP = 3 #loop count
SOUND_SLEEP = 5 # 10秒再生

STATUS_PUB = 0
STATUS_SUB = 0


# 設定ファイル読み込み 
with open(SETTING_FILE) as f:
  data = json.load(f)
print data
print data["device_id"]
myName = data["device_id"]


"""
knock再生
"""
#def sound_on():
#  print("音再生中 =================")
#  global SOUND_FILE, SOUND_LOOP, SOUND_SLEEP, sound_th
#  pygame.mixer.init()
#  pygame.mixer.music.load(SOUND_FILE)
#  pygame.mixer.music.play(SOUND_LOOP) #loop count
#  time.sleep(SOUND_SLEEP)  #指定秒数秒再生
#  pygame.mixer.music.stop()  #停止
#  print("音再生完了 =================")
#  
#  sound_th.join()
#  print "sound_on_send でバックグラウンド再生のスレッドをストップ"

### 音声再生を別スレッドで行う ###
#try:
#  sound_th = threading.Thread(target=sound_on, name="sound_th")
#  sound_th.daemon = True
#  # 指定しておかないと生きているスレッドが全て daemon になったときプログラムが終了するので、main スレッドの終了に合わせてプログラムが終了するようにするため
#  # sound_th.start() #サウンド実行方法
#except KeyboardInterrupt:
#  print "sound_th - KeyboardInterrupt Success"
#except Exception as e:
#  print "sound_th - e.message : " + e.message
#except:
#  print "sound_th - Something else"
#finally:
#  print "sound_th - Finally"

class Sound():
  def __init__(self, loop = SOUND_LOOP, sleep = SOUND_SLEEP, file = SOUND_FILE):
    self.loop = loop
    self.sleep = sleep
    self.file = file
    
    self.play_event = threading.Event() #再生させるかのフラグ
    self.stop_event = threading.Event() #停止させるかのフラグ
  
    self._started = threading.Event()
    self._running = threading.Event()
    self._resume = threading.Event()
    

    #スレッドの作成と開始
    self._thread = threading.Thread(target = self.target)
    self._thread.start()
    
  def target(self):
    print("音再生スレッド開始 =================")
    if self.running:
      self.stop()
    self.play()
    
  def play(self):
    # """音声を再生させる"""
    self.play_event.set()
    print("音再生中 =================")
    pygame.mixer.init()
    pygame.mixer.music.load(self.file)
    pygame.mixer.music.play(self.loop) #loop count
    time.sleep(self.sleep)  #指定秒数秒再生
    pygame.mixer.music.stop()  #停止
    pygame.mixer.quit() #音源への電源停止：サーってノイズを消す
    print("音再生完了 =================")
    
#    self._thread.join()
    self.stop()
    print("音再生スレッド完了 =================")
    
    
  def stop(self, wait=True):
    """スレッドを停止させる"""
#    self.stop_event.set()
#    self.thread.join()    #スレッドが停止するのを待つ

    if self.started:
        self._running.clear()

        # We cannot wait for ourself
        if wait and (threading.current_thread() != self._thread):
            self._thread.join()

        self._started.clear()
        self._resume.clear()


  @property  
  def running(self):
      """ Whether the thread is running. """
      return self._running.is_set()

  @property
  def started(self):
    """ Whether the thread has been started. """
    return self._started.is_set()



"""
knock再生(呼びかけ)
"""
def sound_on_send():
  print("呼び出し音再生中 =================")
  global SOUND_FILE, SOUND_LOOP, SOUND_SLEEP
#  pygame.mixer.init()
#  pygame.mixer.music.load(SOUND_FILE)
#  pygame.mixer.music.play(1) # loop count
#  time.sleep(5)  #指定秒数秒再生
#  pygame.mixer.music.stop()  #停止

  # サウンド再生コマンドをバックグラウンドで実行します
  cmd = "/usr/bin/aplay " + d + " &"
  os.system(cmd)
  print("呼び出し音再生完了 =================")


"""
LED点灯　応答あり
"""
def led_on():
  global PIN_LED, led_flag
  print "--LED ON " + str(led_flag)
  i = 0
  n = 5
  if led_flag:
    while True:
      i = i + 1
      # ループ中にLEDがOFFに指定された場合
      if led_flag:
        GPIO.output(PIN_LED, True)
        time.sleep(0.6)
        GPIO.output(PIN_LED, False)
        time.sleep(0.1)
      else:
        break
      if i >= n:
        break
  else:
    GPIO.output(PIN_LED, False)


"""
LED点灯（はやい）応答受付中
"""
def led_on_fast():
  global PIN_LED, led_flag
  print "--LED ON（はやい）" + str(led_flag)
  i = 0
  n = 5
  if led_flag:
    while True:
      i = i + 1
      if led_flag:
        GPIO.output(PIN_LED, True)
        time.sleep(0.2)
        GPIO.output(PIN_LED, False)
        time.sleep(0.2)
        GPIO.output(PIN_LED, True)
        time.sleep(0.2)
        GPIO.output(PIN_LED, False)
        time.sleep(0.6)
      else:
        break
      if i >= n:
        break
  else:
    GPIO.output(PIN_LED, False)

  print "--LED ON（はやい） 終了"


"""
LED点灯（ゆっくり） 呼び出し中
"""
def led_on_slow():
  global PIN_LED
  print "--LED ON（ゆっくり）"
  i = 0
  n = 2
  if led_flag:
    while True:
      i = i + 1
      if led_flag:
        GPIO.output(PIN_LED, True)
        time.sleep(0.8)
        GPIO.output(PIN_LED, False)
        time.sleep(0.4)
      else:
        break
      if i >= n:
        break
  else:
    GPIO.output(PIN_LED, False)



"""
LEDをOFF
"""
def led_off():
  global PIN_LED
  print "--LED OFF"
  GPIO.output(PIN_LED, False)


"""
メッセージをサーバーに送信する
"""
def publish_mqtt(msg):
  global led_flag
  try:
    print "try publish_mqtt=" + msg
    publish.single(
      "messageID",
      client_id="1",
      #      clean_session=True,
      payload=msg,
      hostname=HOST_NAME)
    print "publish mqtt time %f"
    print "payload=" + msg
  except IOError:
    print "publish error."


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
  global myName, STATUS_PUB, STATUS_SUB, led_flag, sound_th
#  print("msg:"+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))":
  
  if msg.topic == "messageID":
    print("knock受付 =================")
    yourName = str(msg.payload).split("::")
    print("msg.payload = "+ msg.payload )
    print("len(yourName) :"+ str(len(yourName)) )
    if len(yourName) >= 2 :
      print("yourName:"+yourName[1])
      if myName != yourName[1]:
        print("publish %s" % msg)
        sound = Sound() #音再生スレッドの開始
#        sound.play()
        led_flag = True
        led_on_fast()

        
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
  
"""
gpioを監視するスレッド
"""
def gpio_watch():
  global PIN_LED, PIN_BUTTON , STATUS_PUB, led_flag , SOUND_FILE_START, SOUND_FILE_SEND
  
  print "起動音 =================="
  sound_start = Sound(1,3, SOUND_FILE_START)
#  sound_start.play()
  time.sleep(0.2)        
  print "thred start -- gpio_watch =================="
  
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN_LED, GPIO.OUT)
  GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  time.sleep(0.2)
  GPIO.output(PIN_LED, 1)
  time.sleep(0.5)
  GPIO.output(PIN_LED, 0)
  time.sleep(0.5)
  GPIO.output(PIN_LED, 1)
  time.sleep(0.5)
  GPIO.output(PIN_LED, 0)
#  print PIN_BUTTON
  #ボタン待機
  try:
    while True:
      ButtonInput = GPIO.input(PIN_BUTTON)
  #    print GPIO.input(PIN_BUTTON)
      if ButtonInput != True:
        print "button pressed"
        #よびかけ送信
        publish_mqtt("knock form ::"+ myName)
        sound_send = Sound(1,2,SOUND_FILE_SEND) #音再生スレッドの開始 Sound({ループ回数},{再生秒数},{音声ファイル}) 
#        sound_send.play()
        # sound バックグラウンド再生
        # sound_on_send()

        # LED点灯
        led_flag = True
        led_on_slow()
      else:
#        print "ButtonInput : else"
      # LED OFF
        GPIO.output(PIN_LED, 0)
        time.sleep(0.11)
      time.sleep(0.4)
  
  #program should be finished with "clean" gpio-ports
  #when pressing CTRL-c 
  except KeyboardInterrupt:
    print "KeyboardInterrupt Success"
    GPIO.cleanup()    
  except Exception as e:
    print e.message
    print "Something else"
  finally:
#    GPIO.cleanup()
    print "Finally"


### GPIOのループを別スレッドで行う ###
gpio_th = threading.Thread(target=gpio_watch, name="gpio_th")
# gpio_th.daemon = True
# threads.append(gpio_th)
time.sleep(0.1)
gpio_th.start()

time.sleep(0.5)
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

#送信
#publish_mqtt()

#待機開始
try:
  mqttc.loop_forever()
#when pressing CTRL-c 
except KeyboardInterrupt:
  mqttc.loop_stop(force=False) # loopの強制解除
  GPIO.cleanup()
  print "MQTT - loop - KeyboardInterrupt Success"
except Exception as e:
  print "MQTT - loop - e.message : " + e.message
except:
  print "MQTT - loop - Something else"
finally:
  mqttc.loop_stop(force=False)
  GPIO.cleanup()
  print "MQTT - loop - Finally"
