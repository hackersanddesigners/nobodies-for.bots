#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.tag import pos_tag_sents
import socket
import select
import random
import ssl
import sys
import time

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

#-- nktk
file = 'input-text.txt'
with open(file) as fp:
  txi = fp.readlines()
  
  JJ = []
  NN = []
  NNP = []
  RB = []
  DT = []
  VB = []
  VBZ = []
  VBP = []
  VBD = []
  TO = []
  CC = []
  MD = []
  PRPS = []
  IN = []

  for line in txi:
    line = line.decode('utf8')
    tokens = nltk.word_tokenize(line)
    tags = nltk.pos_tag(tokens)
    print (tags)

    for pair in tags:
      tag = pair[1]
      tok = pair[0]
      if tag == 'JJ':
        JJ.append(tok)
      elif tag == 'NN':
        NN.append(tok)
      elif tag == 'NNP':
        NNP.append(tok)
      elif tag == 'RB':
        RB.append(tok)
      elif tag == 'DT':
        DT.append(tok)
      elif tag == 'VB':
        VB.append(tok)
      elif tag == 'VBZ':
        VBZ.append(tok)
      elif tag == 'VBP':
        VBP.append(tok)
      elif tag == 'VBD':
        VBD.append(tok)
      elif tag == 'TO':
        TO.append(tok)
      elif tag == 'CC':
        CC.append(tok)
      elif tag == 'MD':
        MD.append(tok)
      elif tag == 'PRP$':
        PRPS.append(tok)
      elif tag == 'IN':
        IN.append(tok)

    print JJ, len(JJ)
    print NN, len(NN)
    # print NNP, len(NNP)
    # print RB, len(RB)
    # print DT, len(DT)
    # print VB, len(VB)
    # print VBZ, len(VBZ)
    # print VBP, len(VBP)
    # print VBD, len(VBD)
    # print TO, len(TO)
    # print CC, len(CC)
    # print MD, len(MD)
    # print PRPS, len(PRPS)
    # print IN, len(IN)

connected = False
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
  elif words[1] == 'PRIVMSG' and words[2] == CHANNEL and connected:
    chat = ' '.join(words[3:])
    tok = nltk.word_tokenize(chat)
    tokens = tok[1:]
    print str(tokens), '**'
    tags = nltk.pos_tag(tokens)

    JJc = []
    NNc = []
    NNPc = []

    for pair in tags:
      tag = pair[1]
      value = pair[0]
      if tag == 'JJ':
        JJc.append(value)
      elif tag == 'NN':
        NNc.append(value)
      elif tag == 'NNP':
        NNPc.append(value)

    print JJc, len(JJc)
    if len(JJc) > 3 and len(JJ) > 15:
      s.sendall('PRIVMSG %s :'%(CHANNEL) + 'a lot of adjectives\r\n')
    else:
      s.sendall('PRIVMSG %s :'%(CHANNEL) + 'a terse text\r\n')

    if len(tokens) < 3:
      s.sendall('PRIVMSG %s :'%(CHANNEL) + '😶\r\n')
      print str(tokens), '--+++---'

read_loop(got_msg)
