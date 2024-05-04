import asyncio
from asyncio import Lock

from sanic import Blueprint
from sanic.server.websockets.impl import WebsocketImplProtocol

from loguru import logger

bp = Blueprint("detector", url_prefix="/detector", version=1)

_dummy_sender_lock = Lock()


async def _dummy_sender(ws: WebsocketImplProtocol):
    # get root service
    global _dummy_sender_lock
    await _dummy_sender_lock.acquire()
    while True:
        try:
            # send ping message
            await ws.send("ping")
            # image, err = cam.read()
            # if err is not None:
            #     logger.error(err)
            # annoed, uvs = detector.get_landmarks(image)
            await asyncio.sleep(2)  # wait for 120 seconds
        except Exception as e:
            logger.error(f"connection closed: {e}")
            break
    _dummy_sender_lock.release()


@bp.websocket("/dummy", name="detector_dummy")
async def websocket_dummy_handler(request, ws: WebsocketImplProtocol):
    task_name = f"receiver:{request.id}"
    # start sender task
    request.app.add_task(_dummy_sender(ws), name=task_name)
    try:
        while True:
            await asyncio.sleep(86400)
    finally:
        request.app.purge_tasks()
