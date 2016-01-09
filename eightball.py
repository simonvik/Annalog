import re
import time
import random
import collections
import sys

class EightBall():
    def __init__(self, mucbot):
        self.mucbot = mucbot

    def handle(self, msg):
        if msg['body'][:6] == "!8ball":
            answers = ['It is certain', 'It is decidedly so', 'Without a doubt', \
                'Yes - definitely', 'You may rely on it', 'As I see it, yes',\
                'Most likely', 'Outlook good', 'Signs point to yes', 'Yes', \
                'Reply hazy, try again', 'Ask again later', 'Better not tell you now', \
                'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', \
                'My reply is no', 'My sources say no', 'Outlook not so good', \
                'Very doubtful'
            ]

            random.shuffle(answers)
            body = "Eight Ball says: " + random.choice(answers)

            self.mucbot.send_message(mto=msg['from'].bare,
                mbody=body,
                mtype='groupchat')

    def help(self):
        return ["8ball - Ask the all-knowing magic 8 ball"]

class MUCBotMock():
    def send_message(self, mto, mbody, mtype):
        print "MUCBotMock:", mto, mbody, mtype

class FromMock():
    def __init__(self, _from):
        self.bare = _from

def do_test():
    x = EightBall(MUCBotMock())
    msg = {"from" : FromMock("channel@example.com"), "mucnick" : "kallsse", "body" : "!8ball"}
    x.handle(msg)

    msg = {"from" : FromMock("channel@example.com"), "mucnick" : "kallsse", "body" : "!8ball"}
    x.handle(msg)

    msg = {"from" : FromMock("channel@example.com"), "mucnick" : "kallsse", "body" : "!8ball"}
    x.handle(msg)

    msg = {"from" : FromMock("channel@example.com"), "mucnick" : "kallsse", "body" : "!8ball"}
    x.handle(msg)

if __name__ == "__main__":
    do_test()
