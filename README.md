Whisper
=======

###Installing Whisper

*Need to update this, forking Whisper inorder to combine it with my wrapper around pocketsphinx and create a self hostable Speech-to-text service for building voice activation without botnet. This package relies on Pocketsphinx CMS for more information on Pocketsphinx see: https://cmusphinx.github.io/

In order to use this project you will need to:
1. Install Pocketsphinx, Shinxbase and it's Python interface Library. This is a Opensource library for text to speech. To do that please see installing pocketsphinx section below.

2. You will need to install python Twisted and Autobahn. This repo includes them, but you can install them using:
```
pip install twisted
pip install autobahn
```

###Installing Pocketsphinx 
1. First git clone the python source, it comes with git links to known good versions of both pocketsphinx and sphinx base.
```
git clone --recursive https://github.com/cmusphinx/pocketsphinx-python/
```
2. Install dependencies:
```
sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev automake autoconf libtool python-pyaudio
```
3. cd into the cloned directory and then into sphinxbase/. In here you will have to make and build Sphinxbase.
```
cd pocketsphinx-python/sphinxbase
./autogen.h
./configure
make
sudo make install
```
4. Backout one directory and go into the Pocketsphinx directory and run the same commands as above to compile and install pocketsphinx
```
cd ../pocketsphinx
./autogen.h
./configure
make
sudo make install 
```
5. You will most likely need to export these variables in your .bashrc.
```
# Pocketsphinx
export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
```
6. Finally you can install the pocketsphinx python library by backing out one and running setup:
```
sudo python setup.py install
```
7. You can test that it works using the example.py in the same directory. If you encounter an error please contact your system admin.


###How to use this Service
To make use of this software you have to:
1. Have installed the dependencies above.
2. Cloned the source and moved into the directory.
3. In the servers/ directory there is a server.py, run this or use the run.sh script.
    (At this point your Speech to text service is running.)
4. Inside the same servers/ directory there is webserver.py that will host all the files in the local directory. Run that and navigate to the localhost:8081 then find /tests/php/test.php. This should load a web page that will connect to the server.
5. You can hit start, this will record audio until you click stop. Following this you can click the media play button to hear yourself. If you open your javascript console(F12 function key on real operating systems) you should see some words. The server sends back transcribed words and this prints them to the javascript console.
6. Additionally there is also a local python websocket server example in the tests/ directory named websocket_local.py

When a websocket is open with this server on port 9001 it awaits a 'start' UTF8 string and all binary after that will be treated as an audio stream until it receives a 'stop' UTF8 string. Following this it will transcribe the audio sent to it and send it back down the websocket that was opened. 


###Google Chrome
This project requires testing the functionality of [`getUserMedia`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator.getUserMedia).  The [Google Chrome](https://www.google.com/intl/en_us/chrome/browser/) browser, ensures, and provides this functionality.

```
# Google Chrome Dependencies:
sudo apt-get install libappindicator1
sudo apt-get install libindicator7
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
```

**Note:** This project assumes [Ubuntu Server 14.04](http://www.ubuntu.com/download/server) as the operating system.


###AutobahnPython
Provides an open-source, real-time framework implementation for the following protocols:

- [WebSocket Protocol](http://tools.ietf.org/html/rfc6455)
- [Web Application Messaging Protocol](http://wamp.ws/) (WAMP)

Either protocols, excel at [pushing data](http://autobahn.ws/python/#what-can-i-do-with-this-stuff) asynchronously between the client, and server in real-time.  In order to use the [*AutobahnPython*](https://github.com/tavendo/AutobahnPython) framework, it must first be installed:

```
cd /var/www/html/whisper/AutobahnPython/autobahn/
sudo python setup.py install
```

###Twisted
AutobahnPython [requires](http://autobahn.ws/python/installation.html#requirements) a networking framework, which must be either [Twisted](https://github.com/twisted/twisted), or [asyncio](https://docs.python.org/3.4/library/asyncio.html).  This project implements the *Twisted* framework:

```
cd /var/www/html/whisper/twisted
sudo python setup.py install
```

**Note:** Generally, *Twisted* is the framework of choice if the environment only provides python 2.x (will [support](http://twistedmatrix.com/trac/milestone/Python-3.x) python 3.x).  Whereas, *asyncio* is generally preferred if the environment is python 3.x ([included](https://docs.python.org/3/whatsnew/3.4.html) in python 3.4+).

Also thank you Jeff for doing all the hardwork of compiling this together it has been a lifesaver for a couple of my apps. 
