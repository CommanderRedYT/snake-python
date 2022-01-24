#!/usr/bin/python3
# websocket server that distributes all messages to all clients

import argparse
from simple_websocket_server import WebSocket, WebSocketServer

clients = {}

def setup_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a file from one format to another."
    )
    parser.add_argument(
        "-p",
        "--port",
        required=True,
        dest="listen_port",
        help="The port to listen on.",
    )
    parser.add_argument(
        "-a",
        "--address",
        default="0.0.0.0",
        dest="listen_address",
        help="The address to listen on.",
    )
    return parser.parse_args()

class RelayToAllConnections(WebSocket):
    def handle(self):
        for client in clients.values():
            if client !=self:
                client.send_message(self.data)

    def broadcast(self, message):
        for client in clients.values():
            client.send_message(message)

    def connected(self):
        print(self.address, 'connected')
        clients[self.address] = self

    def handle_close(self):
        print(self.address, 'closed')
        self.broadcast(f"I:{self.address} has disconnected")
        del clients[self.address]

def server():
    args = setup_args()
    server = WebSocketServer(args.listen_address, args.listen_port, RelayToAllConnections)
    server.serve_forever()
