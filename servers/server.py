import json, wave, time
import transcriber as trans
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol, \
                                       listenWS
#
#  Server listens over websocket port 9001, receiving binary audio input on start/stop command and writing it to output_(time).wav file.
#
class StreamingServerProtocol(WebSocketServerProtocol):
   # Simple object that wraps around pocketsphinx for easy use.
   tr = trans.transObject(1)
   tr.debug = True

   def onMessage(self, msg, binary):
      # print 'sending echo:'#, msg
      if binary:
          self.file.writeframes(msg)
      elif "start" in msg:
          print("starting")
          self.filename = 'output_'+str(int(time.time()))
          self.file = wave.open(self.filename + '.wav',"wb")
          self.file.setparams((1, 2, 16000, 76000, 'NONE', 'not compressed'))
      elif "stop" in msg:
          print("stopping")
          self.file.close()
          print(self.tr.sttPocketsphinx(self.filename + '.wav'))

      # self.sendMessage(msg, binary)

if __name__ == '__main__':
   factory = WebSocketServerFactory("ws://localhost:9001")
   factory.protocol = StreamingServerProtocol
   listenWS(factory)
   reactor.run()
