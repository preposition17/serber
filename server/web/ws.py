from flask_sock import Sock


sock = Sock()


@sock.route('/test')
def echo(ws):
    while True:
        data = ws.receive()
        print(data)
        ws.send(data)


