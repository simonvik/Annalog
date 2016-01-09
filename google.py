import re
import time
import json
import urllib
import urllib2
import collections
import sys

class Google():
    def __init__(self, mucbot):
        self.mucbot = mucbot

    def google(self, q):
        data = json.load(urllib2.urlopen("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % urllib.quote_plus(q)))
        
        ret = []
        for i in range(0, min(3, len(data["responseData"]["results"]))):
            res = data["responseData"]["results"][i]
            ret.append("%s - %s" % (res["titleNoFormatting"], res["url"]))
        
        return "\n".join(ret)

    def handle(self, msg):
        if msg['body'][:7] == "!google":
            q = msg['body'][8:]
            body = "Results:\n" + self.google(q)

            self.mucbot.send_message(mto=msg['from'].bare,
                mbody=body,
                mtype='groupchat')

    def help(self):
        return ["google - Return top 3 results for a Google query"]

class MUCBotMock():
    def send_message(self, mto, mbody, mtype):
        print "MUCBotMock:", mto, mbody, mtype

class FromMock():
    def __init__(self, _from):
        self.bare = _from

def do_test():
    x = Google(MUCBotMock())
    msg = {"from" : FromMock("channel@example.com"), "mucnick" : "kallsse", "body" : "!google four lights"}
    x.handle(msg)

if __name__ == "__main__":
    do_test()
