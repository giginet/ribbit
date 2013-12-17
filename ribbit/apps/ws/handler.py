#! -*- coding: utf-8 -*-
#
# created by giginet on 2013/12/17
#
import time
import json
from pulsar.apps import ws, pubsub

from ribbit.apps.messages.models import Message
from ribbit.apps.rooms.models import Room

class Client(pubsub.Client):

    def __init__(self, connection, room):
        self.connection = connection
        self.room = room

    def __call__(self, channel, message):
        if self.room.slug == channel:
            self.connection.write(message)

class Chat(ws.WS):
    '''The websocket handler managing the chat application.
    '''
    _pubsub_cache = {}

    def pubsub(self, websocket, room):
        if not room.slug in self._pubsub_cache.keys():
            # ``pulsar.cfg`` is injected by the pulsar server into
            # the wsgi environ. Here we pick up the name of the wsgi
            # application running the server. This is **only** needed by the
            # test suite which tests several servers/clients at once.
            name = websocket.handshake.environ['pulsar.cfg'].name
            self._pubsub_cache[room.slug] = pubsub.PubSub(name=name)
            self._pubsub_cache[room.slug].subscribe(room.slug)
        return self._pubsub_cache[room.slug]

    def on_open(self, websocket):
        '''A new websocket connection is established.

        Add it to the set of clients listening for messages.
        '''
        room_slug = websocket.handshake.environ.get('QUERY_STRING', '')
        # ToDo check permissions
        try:
            room = Room.objects.get(slug=room_slug)
            client = Client(websocket, room)
            self.pubsub(websocket, room).add_client(client)
        except:
            client.connection.write(json.dumps({
                'action' : 'error',
                'body' : 'Invalid Room ID'}
            ))

    def on_message(self, websocket, message):
        '''
        When a new message arrives, it publishes to all listening clients.
        '''
        try:
            data = json.loads(message)
        except:
            data = None
        if not data: return

        user = websocket.handshake.get('django.user')
        # ToDo check permissions
        if user.is_authenticated():
            username = user.username
            if data['action'] == 'post':
                room = Room.objects.get(slug=data['room'])
                if room:
                    message = room.add_message(data['body'], user)

                response = {
                    'action' : 'receive',
                    'author' : user.serialize(),
                    'body' : message.body,
                    'room' : room.serialize(),
                    'timestamp' : time.time()
                }
                self.pubsub(websocket, room).publish(room.slug, json.dumps(response))
