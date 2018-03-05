import json, wave, time
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol, \
                                       listenWS
#
#  Server listens over websocket port 9001, receiving binary audio input on start/stop command and writing it to output_(time).wav file.
#
class StreamingServerProtocol(WebSocketServerProtocol):
   filename = 'output_'+str(int(time.time()))
   file = wave.open(filename + '.wav',"wb")
   file.setparams((1, 2, 16000, 76000, 'NONE', 'not compressed'))

   def onMessage(self, msg, binary):
      # print 'sending echo:'#, msg
      if binary:
          self.file.writeframes(msg)
      elif "start" in msg:
          print("starting")
      elif "stop" in msg:
          print("stopping")
          self.file.close()
      # self.sendMessage(msg, binary)

if __name__ == '__main__':
   factory = WebSocketServerFactory("ws://localhost:9001")
   factory.protocol = StreamingServerProtocol
   listenWS(factory)
   reactor.run()
