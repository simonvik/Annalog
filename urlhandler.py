import re
import json
import time
import hashlib
from datetime import datetime

class URLHandler():
  def __init__(self, mucbot):
    self.mucbot = mucbot
    self.salt1 = "bork bork"
    self.salt2 = "sad pandas are happy"
    self.whitelist = ["1b49f24e1acf03ef8ad1b803593227ca1b94868c29d41a8ab22fbc7b6d94342c"]
    filename = "url.txt"
    self.urlfile = open(filename, "a+")
    self.urldata = [json.loads(line) for line in self.urlfile]
    self.urls = [line["url"] for line in self.urldata]
    self.urlfile.seek(0, 2)

  def hash(self, plaintext):
    return hashlib.sha256(self.salt1 + str(plaintext) + self.salt2).hexdigest()

  def get(self, url_plaintext):
    url = self.hash(url_plaintext)
    if url in self.whitelist:
      return {"type" : "whitelisted"}
    index = self.urls.index(url) if url in self.urls else -1
    return {"type" : "urldata", "data" : self.urldata[index]} if index >= 0 else {"type" : "notfound"}

  def add(self, url_plaintext, nick, timestamp):
    url = self.hash(url_plaintext)
    urldata = {"url" : url, "timestamp" : timestamp, "nick" : nick}
    self.urldata.append(urldata)
    self.urls.append(url)
    self.urlfile.write(json.dumps(urldata))
    self.urlfile.write("\n")
    self.urlfile.flush()

  def handle(self, msg):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg['body'])
    if not urls:
      return
    for url in urls:
      urldata = self.get(url)
      if urldata["type"] == "urldata":
        print "Found URL:", url
        tdiff = datetime.now() - datetime.fromtimestamp(int(urldata['data']['timestamp']))
        self.mucbot.send_message(mto=msg['from'].bare,
          mbody="%s: Oooooooooold! %s was first (%s)" % (msg['mucnick'], urldata['data']['nick'], tdiff),
          mtype='groupchat')
      elif urldata["type"] == "notfound":
        print "Adding URL:", url
        self.add(url, str(msg['mucnick']), str(int(time.time())))
      elif urldata["type"] == "whitelisted":
        print "Whitelisted:", url

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

