import wave, time, logging, sys, os
import transcriber as trans
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol, \
                                       listenWS
# Globals
logger = logging.getLogger(__name__)

#
#  Server listens over websocket port 9001, receiving binary audio input on start/stop command and writing it to output_(time).wav file.
#
class StreamingServerProtocol(WebSocketServerProtocol):
   # Simple object that wraps around pocketsphinx for easy use.
   tr = trans.transObject(1)
   # tr.debug = True           

   # Autobahn websocket connection event handlers. Async
   def onConnect(self, request):
       logger.info("Client connecting: {}".format(request.peer))
   def onClose(self, wasClean, code, reason):
       logger.info("WebSocket connection closed: {}".format(reason))

   def onMessage(self, msg, binary):
      if binary:
          self.file.writeframes(msg)

      elif "start" in msg:
          logger.debug(">>Start received")
          self.filename = 'output_'+str(int(time.time()))
          self.file = wave.open(self.filename + '.wav',"wb")
          self.file.setparams((1, 2, 16000, 76000, 'NONE', 'not compressed'))

      elif "stop" in msg:
          logger.debug(">>Stop received..")
          self.file.close()
          # This is where we use the object to do speech to text.
          output = self.tr.sttPocketsphinx(self.filename + '.wav')
          logger.debug(">>Output:")
          logger.debug(output)
          # Then we package it up and send it bakc down the websocket.
          cat = ""
          for values in output:
              if '<' not in str(values):
                  cat += ":" + str(values)
          self.sendMessage(''+ cat)
          os.remove(self.filename + '.wav')


if __name__ == '__main__':
   logging.basicConfig(level=logging.DEBUG)
   # logging.basicConfig(level=logging.INFO)
   factory = WebSocketServerFactory("ws://localhost:9001")

   logger.info("Whisper started websocket server on localhost:9001")
   factory.protocol = StreamingServerProtocol
   listenWS(factory)

   logger.info("Program started...")
   reactor.run()
   logger.info("Program exiting...")
