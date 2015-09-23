# -*- coding: utf-8 -*-
from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop,web
import time,datetime
import tornado.websocket
import tornado.template
import base64
import random
from pprint import pprint 


port = "8000"
host = "http://nasutoma-here.cgfm.jp"
path = "/demo"
origin = "http://nasutoma-here.cgfm.jp"

def generate_random_string(length = 10, addSpaces = True, addNumbers = True):
  characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"§$%&/()=[]{}'
  useChars=[]
  for i in range(0, length -1):
#    print int(i)
#    print random.randint(0, len(characters)-1)
#    print characters[22]
    randomInt = random.randint(0, len(characters)-1)
    tmpStr = characters[randomInt]
#    print tmpStr
#    useChars[i] = characters[random.randint(0, len(characters)-1)]
    useChars.extend(tmpStr)
  if(addSpaces):
    useChars.extend((' ', ' ', ' ', ' ', ' ', ' '))
  if(addNumbers):
    useChars.extend((random.randint(0,9), random.randint(0,9), random.randint(0,9)))
  # 配列の数値を文字列化
  useChars = [str(s) for s in useChars]
  
#  print "useChars:" + pprint(useChars) 
#  print "[useChars] "+ useChars
  random.shuffle(useChars)
#  pprint (useChars) 
#  randomString = useChars;
  randomString = "".join(useChars)
#  print "randomString:" + randomString 
  randomString = randomString.strip()
#  print "randomString:" + randomString 
  randomString = randomString[0:length]
#  print "randomString:" + randomString 
  return randomString


keyTmp = generate_random_string(16, False, True)
key = base64.b64encode(keyTmp)

protocol_str = "GET " + path + " HTTP/1.1\r\n"
protocol_str += "Host: " + host + ":" + port +"\r\n"
protocol_str += "Upgrade: websocket\r\n"
protocol_str += "Connection: Upgrade\r\n"
protocol_str += "Pragma: no-cache\r\n"
protocol_str += "Cache-Control: no-cache\r\n"
protocol_str += "Sec-WebSocket-Key: " + key + "\r\n"
protocol_str += "Sec-WebSocket-Origin: " + origin + "\r\n"
protocol_str += "Sec-WebSocket-Version: 13\r\n"
protocol_str += "Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n"
protocol_str += "Accept-Encoding: gzip, deflate, sdch\r\n"
protocol_str += "Accept-Language: ja,en-US;q=0.8,en;q=0.6\r\n"
  
  
print "protocol_str:" + protocol_str 

protocol_str = ""

class MyClient(TornadoWebSocketClient):
     def opened(self):
        print "[Client] connection opened"
        self.send("hello "+str(datetime.datetime.now()))

     def received_message(self, m): 
         print "[Client] Received from central: ",
         print m

     def closed(self, code, reason=None):
         ioloop.IOLoop.instance().stop()
         print reason
         print code
         print "[Client] close MyClient socket"

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print '[Server] connection opened...'
        self.write_message("The server says: 'Hello'. Connection was accepted.")
  
    def on_message(self, message):
        self.write_message("The server says: " + message + " back at you")
        print '[Server] received:', message
  
    def on_close(self):
        print '[Server] connection closed...'

  
#application = web.Application([
#        (r'/ws', WSHandler),
#])

def process_handshake_header(self, headers):
  print 'over ride'


#application.listen(8000)
#print "server open at 8000"
#ws = MyClient('ws://nasutoma-here.cgfm.jp:8000/demo', protocols=['http-only', 'chat'])
#ws = MyClient('ws://nasutoma-here.cgfm.jp:8000/demo', url="http://nasutoma-here.cgfm.jp", protocols=['http-only', 'chat'], headers=[protocol_str])
ws = MyClient(
  'ws://nasutoma-here.cgfm.jp:8000/demo',
  protocols=['http-only', 'chat'],
  headers=protocol_str
)
ws.connect()
ioloop.IOLoop.instance().start()