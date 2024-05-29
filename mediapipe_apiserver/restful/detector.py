import asyncio
import time
import json
from asyncio import Lock

import cv2
from sanic import Blueprint, Sanic
from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.connection import State

from loguru import logger

bp = Blueprint("detector", url_prefix="/detector", version=1)

_dummy_sender_lock = Lock()

_interval_sec = 2

async def _dummy_sender(ws: WebsocketImplProtocol, camera, detector):
    # get root service
    global _dummy_sender_lock
    seq = 0
    uvs = None
    while True:
        try:
            # send ping message
            image, err = camera.read()
            if err is not None:
                logger.error(err)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            _, uvs = detector.get_landmarks(image)
            res = {
                'time': time.time_ns(),
                'uvs': uvs,
                'seq': seq
            }
            await ws.send(json.dumps(res))
            seq += 1
        except Exception as e:
            logger.error(f"connection closed: {e}")
            break



@bp.websocket("/dummy", name="detector_dummy")
async def websocket_dummy_handler(request, ws: WebsocketImplProtocol):
    task_name = f"receiver:{request.id}"
    # start sender task
    camera, detector = request.app.ctx.camera,request.app.ctx.detector
    _app: Sanic = request.app
    _app.add_task(_dummy_sender(ws, camera, detector), name=task_name)
    try:
        await _dummy_sender_lock.acquire()
        while True:
            if ws.ws_proto.state in (State.CLOSED, State.CLOSING):
                break
            else:
                await asyncio.sleep(1)
    finally:
        ws.close()
        ws.wait_for_connection_lost()
        _dummy_sender_lock.release()
        _app.cancel_task(task_name)
        _app.purge_tasks()
