"""
This scripts try to connect to a dummy server and display
Set the CONFIG_WS_ENDPOINT variable with `export CONFIG_WS_ENDPOINT=xxx`
"""
import asyncio
import websockets
import os
import time

from loguru import logger

CONFIG_WS_ENDPOINT = os.environ.get("CONFIG_WS_ENDPOINT", "ws://127.0.0.1:3000/v1/detector/dummy")
_interval_sec = 2
async def connect_to_server():
    uri = CONFIG_WS_ENDPOINT
    logger.info(f"uri={uri}")
    async with websockets.connect(uri) as ws:
        seq = 0
        start_t = time.time()
        last_seq = seq
        while True:
            message = await ws.recv()
            seq += 1
            # print(f"Received: {message}")
            if time.time() - start_t > _interval_sec:
                logger.info(f"refresh rate: {(seq - last_seq)/ _interval_sec}")
                start_t = time.time()
                last_seq = seq

asyncio.run(connect_to_server())