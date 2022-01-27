import socketio

from flask import Blueprint


class IOBlueprint(Blueprint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.namespace = self.url_prefix or '/'
        self._socketio_handlers = []
        self.socketio = None
        self.record_once(self.init_socketio)

    def init_socketio(self, state):
        self.socketio: socketio.Client = state.app.extensions['socketio']
        for f in self._socketio_handlers:
            f(self.socketio)

        return self.socketio

    def on(self, key):
        """ A decorator to add a handler to a blueprint. """

        def wrapper(f):
            def wrap(sio):
                @sio.on(key, namespace=self.namespace)
                def wrapped(*args, **kwargs):
                    return f(*args, **kwargs)

                return sio

            self._socketio_handlers.append(wrap)

        return wrapper

    def emit(self, *args, **kwargs):
        self.socketio.emit(*args, **kwargs)