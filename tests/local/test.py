import time
import pyaudio
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    # Start!
    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("start".encode('utf8'))

        # Init audio input stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()
        print("Recording...")

        # Configure time, 10 second recording.
        start = time.time()
        cur_time = time.time() - start
        delay = 5

        # Loop through and send packets.
        while cur_time < delay:
            print(cur_time)
            buf = stream.read(1024)
            if buf:
                self.sendMessage(buf, isBinary=True)
            else:
                break
            cur_time = time.time() - start    

        # Clean up
        stream.stop_stream()
        stream.close()
        self.sendMessage("stop".encode('utf8'))

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        self.transport.loseConnection()
        reactor.stop()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    import sys
    # from twisted.python import log
    from twisted.internet import reactor
    # log.startLogging(sys.stdout)
    factory = WebSocketClientFactory(u"ws://127.0.0.1:9001")
    factory.protocol = MyClientProtocol
    reactor.connectTCP("127.0.0.1", 9001, factory)
    reactor.run()




