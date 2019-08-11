import collections, wave, time
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

#---For testing imports only ---
import math, os
import pyaudio as p
#-------------------------------

#
#  TransObject is meant to be a pickup and throwaway object that wraps
#	Pocketsphinx transcription into a simple task for threading reasons.
#
class transObject:
    def __init__(self, id):
        self.id = id
        self.debug = False
        self.data=collections.deque()
        self.chunk = 1024

    def dPrint(self, text):
        if self.debug:
            print(">>DEBUG ID:", self.id, text)

    def calibrate(self):
        self.dPrint("Getting average audio intensity..")
        self.dPrint("Completed Calibation.")

    def recieve(self, data):
        self.dPrint("Recieved audio clip..")
        self.data.append(data)

    # Later this will write to file and transcribe that then return text.
    def transcribe(self, sampleSize):
        self.dPrint("Transcribed looks like:")
        filename = self.saveSpeech(self.data, sampleSize)
        text = self.sttPocketsphinx(filename)
        self.data = []
        os.remove(filename)
        return text

    # Leverage Pocketsphinx to convert saved sound file to text and send back down the pipe.
    def sttPocketsphinx(self, wav_file):
        # Gotta setup the decoder.
        config = Decoder.default_config()
        config.set_string('-hmm', "model/en-us/en-us")
        config.set_string('-lm', 'lang_models/9228.lm')
        config.set_string('-dict', 'lang_models/9228.dic')
        config.set_string('-dictcase', 'yes')
        #config.set_string('-jsgf', 'grams/goforward.gram')
        config.set_string('-logfn', '/dev/null')
        decoder = Decoder(config)

        # Grammar based rules setup.
        #jsgf = Jsgf('grams/commands.gram')
        #rule = jsgf.get_rule('commands.action1')
        #fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
        #fsg.writefile('grams/commands.fsg')
        #decoder.set_fsg('commands', fsg)
        #decoder.set_search('commands')

        # Start decoding file.
        decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
            buf = stream.read(self.chunk)
            if buf:
                decoder.process_raw(buf, False, False)
            else:
                break
        decoder.end_utt()

        # Write those words to an easy to parse format.
        words = []
        #[words.append(seg.word) for seg in decoder.seg()]
        for seg in decoder.seg():
            if "NULL" not in seg.word and "sil" not in seg.word:
                words.append(seg.word)
        if decoder.hyp() != None:
            hypothesis = decoder.hyp()
            #print('Best hypothesis: ' + hypothesis.hypstr)
            words.append(hypothesis.best_score)
        else:
            words.append(0)

        return words

    def saveSpeech(self, data, sample_size):
        filename = 'output_'+str(int(time.time()))
        data = ''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_size)
        wf.setframerate(16000)
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def start(self):
        self.dPrint("Stub start")

    def stop(self):
        self.dPrint("Stub start")


if(__name__ == '__main__'):
    test = transObject(1)
    test.debug = True
    print(test.sttPocketsphinx("../tests/test.wav"))
    # test.start()
    # test.stop()
