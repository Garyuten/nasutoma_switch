from __future__ import print_function
import websocket

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.create_connection("ws://nasutoma-here.cgfm.jp:8000/demo")
#    ws = websocket.create_connection("ws://nasutoma-here.cgfm.jp:8000", http_proxy_port=8000)
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()
