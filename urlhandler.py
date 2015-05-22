import re
import json
import time
import hashlib
import sqlite3
from datetime import datetime

class URLHandler():
  def __init__(self, mucbot):
    self.mucbot = mucbot
    self.salt1 = "bork bork"
    self.salt2 = "sad pandas are happy"
    self.db = sqlite3.connect('db.sq3')

  def hash(self, plaintext):
    return hashlib.sha256(self.salt1 + str(plaintext) + self.salt2).hexdigest()

  def get_or_set(self, url_plaintext, nick, time):
    url = self.hash(url_plaintext)
    c = self.db.execute('SELECT * FROM urls WHERE url = ? ORDER BY time DESC LIMIT 1', [url])
    row = c.fetchone()
    if row:
       return row
    else:
       self.db.execute('INSERT INTO urls (nick, url, time) VALUES (?,?,?)', (nick, url, time) );
       self.db.commit()
       return None
    
  def handle(self, msg):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg['body'])
    if not urls:
      return
    for url in urls:
      urldata = self.get_or_set(url, msg['mucnick'], int(time.time()) )
      if urldata:
          tdiff = datetime.now() - datetime.fromtimestamp(urldata[2])
          self.mucbot.send_message(mto=msg['from'].bare,
             mbody="%s: Oooooooooold! %s was first (%s)" % (msg['mucnick'], urldata[0], tdiff),
             mtype='groupchat')

class MUCBotMock():
  def send_message(self, mto, mbody, mtype):
    print "MUCBotMock:", mto, mbody, mtype

class FromMock():
  def __init__(self, _from):
    self.bare = _from

if __name__ == "__main__":
  x = URLHandler(MUCBotMock())
  msg = {"from" : FromMock("channel@example.com"), "mucnick" : "kalle", "body" : "hello http://github.com/"}
  x.handle(msg)

