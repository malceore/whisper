import sys, socket, pyaudio
#
# This is an example file of using a local python program to 
#    capture audio from a microphone and send it to the Whisper
#    service via websocket. You could change the IP and use this
#    on a different machine than the Whisper service.
#

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the websocket to the port where the server is listening
server_address = ('localhost', 9001)
sock.connect(server_address)

try:
    sock.sendall("start")
    p = pyaudio.PyAudio()
    # Channels and rate are important, needs to be 16k and mono.
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    # Process audio chunk by chunk. On keyphrase detected perform action and restart search
    while True:
        buf = stream.read(1024)
        # Send data.
        if buf:
            print("BUFF")
            # decoder.process_raw(buf, False, False)
        #    sock.sendall(buf)
        else:
            # sock.sendall("stop")
            break

except ValueError:
    print("Looks like there was an error..")