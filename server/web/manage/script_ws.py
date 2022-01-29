from flask_socketio import emit


from ..blueprintio import IOBlueprint


script_ws = IOBlueprint("script_ws", __name__)


@script_ws.on('connect')
def connect():
    print("* WS client: connected")


@script_ws.on('debug_script')
def connect(data):
    script_ws.emit("debug_console", data)





@script_ws.on('message')
def connect(data):
    print("* WS client: New message: " + data["data"])

