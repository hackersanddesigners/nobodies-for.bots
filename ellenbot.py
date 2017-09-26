#!/usr/bin/env python
# -*- coding: UTF-8 =-*-

#first run 'pip install nltk'
import socket
import select
import random
import ssl
import sys, os
import time
from ellen import ellen

if len(sys.argv) != 5:
  print "Usage: python %s <host> <channel> (no need for '#')> [--ssl|--plain] <nick>"
  exit(0)

HOST = sys.argv[1]
CHANNEL = '##'+sys.argv[2]
SSL = sys.argv[3].lower() == '--ssl'
PORT = 6697 if SSL else 6667
NICK = sys.argv[4]

plain = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(plain) if SSL else plain

print "Connecting ☺︎"

s.connect((HOST, PORT))
def read_loop(callback):
  data = ''
  CRLF = '\r\n'
  while True:
    time.sleep(0.2) #prevent CPU hogging
    try:
      readables, writables, exceptionals = select.select([s], [s], [s])
      if len(readables) == 1:
        data += s.recv(512);
        while CRLF in data:
          msg = data[:data.index(CRLF)]
          data = data[data.index(CRLF)+2:]
          callback(msg)
    except KeyboardInterrupt:
      print 'Leaving!'
      s.sendall('PART %s :Bye\r\n'%(CHANNEL))
      s.close()
      exit(0)

print 'Registering...'

s.sendall('NICK %s\r\n'%(NICK))
s.sendall("USER %s * * :aff-ect's companion species\r\n"%(NICK))

connected = False

def send(x):
    s.send(x+"\r\n")

def display(x):
    send("PRIVMSG %s :%s"%(CHANNEL, x))

def got_msg(msg):
  print msg
  global connected
  words = msg.split(' ')
  if 'PING' in msg:
    s.sendall('PONG\r\n')
  if words[1] == '001' and not connected:
    # as per section 5.1 of the RFC, `001` is the numeric response for
    # successful connection && welcome message.
    connected = True
    s.sendall('JOIN %s\r\n'%(CHANNEL))
    print 'Joining ☺︎'
  elif words[1] == 'PRIVMSG' and words[2] == CHANNEL and 'programming' in words[3] and connected:
    display(random.choice(ellen))
  elif words[1] == 'PRIVMSG' and words[2] == CHANNEL and 'programming' in words and connected:
    display(random.choice(ellen))
  # elif words[1] == 'PRIVMSG' and words[2] == CHANNEL and connected:
  #       display("test")


read_loop(got_msg)
