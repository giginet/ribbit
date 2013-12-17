#! -*- coding: utf-8 -*-
#
# created by giginet on 2013/12/17
#
__author__ = 'giginet'

import gevent
import random
from geventwebsocket import WebSocketApplication

class RibbitApplication(WebSocketApplication):
    def on_open(self):
        self.ws.send('welcome')

    def on_message(self, message, *args, **kwargs):
        self.ws.send(message + ' ' + message)

    def on_close(self, reason):
        print "Connection Closed!!!", reason
