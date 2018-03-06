Whisper
=======

*Need to update this, forking Whisper inorder to combine it with my wrapper around pocketsphinx and create a self hostable Speech-to-text service for building voice activation without botnet.

In order to use this project you will need to:
1. Install Pocketsphinx, Shinxbase and it's Python interface Library. This is a Opensource library for text to speech. To do that please follow this tutorial:
http://www.instructables.com/id/Introduction-to-Pocketsphinx-for-Voice-Controled-A/

2. You will need to install python Twisted and Autobahn. This repo includes them and instructions are found below.

Here is how you run the current build:
1. Clone and move into the directory.
2. Make run.sh executable and run it. (Your headless server is now running.)
3. To test it please run the webserver.py in the servers director and navigate to tests/php/test.php.
4. Once there you can start and stop streaming audio to server. When you hit stop it should print the transcribed text in your terminal but it is also being sent back to your browser if you examine the javascript console.



###Overview

This project utilizes the [*WebSocket Protocol*](https://developer.mozilla.org/en-US/docs/WebSockets).  Some configurations need to be made at each end, in order for WebSocket to be able to communicate from the browser to the server (and vice versa):

First, a WebSocket server needs to be defined.  Since [*AutobahnPython*](https://github.com/tavendo/AutobahnPython) is the chosen server-side implementation, the corresponding [`server.py`](https://github.com/jeff1evesque/whisper/blob/master/websocket/server.py) will need to utilize the respective [interfaces](https://github.com/tavendo/AutobahnPython/blob/master/autobahn/autobahn/websocket/interfaces.py).

Once the server has been created, the client-side implementation needs to be defined.  This project chooses to use the javascript [*WebSocket Protocols*](https://developer.mozilla.org/en-US/docs/WebSockets/Writing_WebSocket_client_applications).  However, other client-side schemes are possible, for example, [*AutobahnJS*](https://github.com/tavendo/AutobahnJS).  Implementing *AutobahnJS* on the client-side, would require the use of the [*WAMP Protocol*](http://wamp.ws/) on the server-side (provided in AutobahnPython) as well.  The change from [*WebSockets*](https://developer.mozilla.org/en-US/docs/WebSockets), to the *WAMP Protocol* would change [`server.py`](https://github.com/jeff1evesque/whisper/blob/master/websocket/server.py), respectively.

**Note:** The *WebSocket* protocol is [supported](http://caniuse.com/websockets) by all major browsers, except:

- IE 9-
- Opera Mini 5-7
- Android Browser 4.3-

After the WebSocket protocol has been defined, this application is able to stream to the server using the HTML5 [`getUserMedia`](https://developer.mozilla.org/en-US/docs/NavigatorUserMedia.getUserMedia) object. This object first prompts permission to access the microphone. Once granted, an audio stream object is created.  The stream is sent to the [`server.py`](https://github.com/jeff1evesque/whisper/blob/master/websocket/server.py), where it can be accessed, and modified.

Unfortunately, not all browsers (Internet Explorer, Safari, and mobile devices) support the  `getUserMedia` object.  In particular, Internet Explorer claims to [support](http://status.modern.ie/mediacaptureandstreams?term=getUser) this feature in later releases, while Safari supports its own [streaming API](https://developer.apple.com/streaming/).  Mobile devices will need to incorporate a framework such as [Cordova](http://cordova.apache.org/), or [Phonegap](http://phonegap.com/) in order to support audio streaming.

Since `getUserMedia` has not been adopted by all browser, a fallback is required.  In this project, a basic flash fallback has been implemented.  This implementation requires users to start, then stop recording an audio, and click upload, before the entire audio recording is saved to the server.  Later releases for this project, may incorporate a flash fallback [implementation](https://github.com/jeff1evesque/whisper/issues/71) that streams audio from the browser to server, along with a mobile device [polyfill](https://github.com/jeff1evesque/whisper/issues/165).

**Note:** to see a working example of this project, refer to [`test.php`](https://github.com/jeff1evesque/whisper/blob/master/tests/php/test.php).

##Installation

###Linux Packages

The following packages need to be installed through terminal in Ubuntu:

```
# Google Chrome Dependencies:
sudo apt-get install libappindicator1
sudo apt-get install libindicator7
```

###Google Chrome

This project requires testing the functionality of [`getUserMedia`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator.getUserMedia).  The [Google Chrome](https://www.google.com/intl/en_us/chrome/browser/) browser, ensures, and provides this functionality.

```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
```

**Note:** This project assumes [Ubuntu Server 14.04](http://www.ubuntu.com/download/server) as the operating system.

##Configuration


####GIT Submodule

We need to initialize our git *submodules*:

```
sudo git submodule init
sudo git submodule update
```

**Note:** We have to use the *sudo* prefix, since we haven't taken care of file permissions yet.

The above two commands will update submodules.  If they are already initialized, then the latter command will suffice. Then, we need to pull the code-base into the initialized submodule directory:

```
cd /var/www/html/whisper/
git checkout -b NEW_BRANCH master
cd [YOUR_SUBMODULE]/
git checkout master
git pull
cd ../
git status
```


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