import websocket
try:
    import thread
except ImportError:  #TODO use Threading instead of _thread in python3
    import _thread as thread
import time
import sys


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("on_open...")

#      payload.action = $('#action').val();
#      payload.data = $('#data').val();

    def run(*args):
        for i in range(3):
            # send the message, then wait
            # so thread doesnt exit and socket
            # isnt closed
            ws.send("Hello %d" % i)
            time.sleep(1)


        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        # host = "ws://nasutoma-here:8000/demo"
        host = "ws://nasutoma-here.cgfm.jp:8000/demo"
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()