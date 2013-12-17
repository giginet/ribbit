"""
This example generates random data and plots a graph in the browser.

Run it using Gevent directly using:
    $ python plot_graph.py

Or with an Gunicorn wrapper:
    $ gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" \
        plot_graph:resource
"""


from geventwebsocket import WebSocketServer, Resource
from ribbit.socket.server import RibbitApplication

resource = Resource({
    '/chat': RibbitApplication
})

if __name__ == "__main__":
    server = WebSocketServer(('', 9000), resource, debug=True)
    server.serve_forever()