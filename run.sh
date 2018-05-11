#!/bin/sh
# ps aux | grep server.py | grep -v grep
#if [ $? != 0 ]
#then
cd ~/Code/whisper/servers
python server.py 2>&1 | tee -a /tmp/whisper.log &
rm out*
#fi
