#! -*- coding: utf-8 -*-
#
# created by giginet on 2013/12/17
#
import time
import json
from pulsar.apps import ws, pubsub

class Client(pubsub.Client):

    def __init__(self, connection):
        self.connection = connection

    def __call__(self, channel, message):
        if channel == 'webchat':
            self.connection.write(message)

class Chat(ws.WS):
    '''The websocket handler managing the chat application.
    '''
    _pubsub = None

    def pubsub(self, websocket):
        if not self._pubsub:
            # ``pulsar.cfg`` is injected by the pulsar server into
            # the wsgi environ. Here we pick up the name of the wsgi
            # application running the server. This is **only** needed by the
            # test suite which tests several servers/clients at once.
            name = websocket.handshake.environ['pulsar.cfg'].name
            self._pubsub = pubsub.PubSub(name=name)
            self._pubsub.subscribe('webchat')
        return self._pubsub

    def on_open(self, websocket):
        '''A new websocket connection is established.

        Add it to the set of clients listening for messages.
        '''
        client = Client(websocket)
        self.pubsub(websocket).add_client(client)
        client.connection.write("welcome")

    def on_message(self, websocket, msg):
        '''When a new message arrives, it publishes to all listening clients.
        '''
        if msg:
            lines = []
            for l in msg.split('\n'):
                l = l.strip()
                if l:
                    lines.append(l)
            msg = ' '.join(lines)
            if msg:
                user = websocket.handshake.get('django.user')
                if user.is_authenticated():
                    user = user.username
                else:
                    user = 'anonymous'
                msg = {'message': msg, 'user': user, 'time': time.time()}
                self.pubsub(websocket).publish('webchat', json.dumps(msg))
