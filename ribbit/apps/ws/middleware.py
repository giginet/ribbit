#! -*- coding: utf-8 -*-
#
# created by giginet on 2013/12/17
#
from django.conf import settings
from django.http import HttpResponse
from pulsar.apps import ws, pubsub
from handler import Chat

class WebSocketMiddleWare(object):
    '''Django middleware for serving the Chat websocket.'''
    def __init__(self):
        self._web_socket = ws.WebSocket('/ws', Chat())

    def process_request(self, request):
        environ = request.META
        environ['django.user'] = request.user
        response = self._web_socket(environ)
        if response is not None:
            # we have a response, this is the websocket upgrade.
            # Convert to django response
            resp = HttpResponse(status=response.status_code,
                                content_type=response.content_type)
            for header, value in response.headers:
                resp[header] = value
            return resp
        else:
            environ.pop('django.user')