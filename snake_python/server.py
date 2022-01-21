#!/usr/bin/python3
# websocket server that distributes all messages to all clients

import argparse
import asyncio

import websockets


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

async def handle(websocket):
    async for message in websocket:
        await websocket.send(message)

async def server():
    config = setup_args()
    async with websockets.serve(handle, host=config.listen_address, port=config.listen_port) as server:
        await asyncio.Future()

asyncio.run(server())
