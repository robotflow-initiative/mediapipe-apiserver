"""
This scripts try to connect to a dummy server and display
Set the CONFIG_WS_ENDPOINT variable with `export CONFIG_WS_ENDPOINT=xxx`
"""
import asyncio
import websockets
import os

from loguru import logger

CONFIG_WS_ENDPOINT = os.environ.get("CONFIG_WS_ENDPOINT", "ws://127.0.0.1:3000/v1/detector/dummy")
async def connect_to_server():
    uri = CONFIG_WS_ENDPOINT
    logger.info(f"uri={uri}")
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(connect_to_server())