import asyncio
from asyncio import Lock

from sanic import Blueprint
from sanic.server.websockets.impl import WebsocketImplProtocol

from loguru import logger

bp = Blueprint("detector", url_prefix="/detector", version=1)

_dummy_sender_lock = Lock()


async def _dummy_sender(ws: WebsocketImplProtocol, camera, detector):
    # get root service
    global _dummy_sender_lock
    await _dummy_sender_lock.acquire()
    while True:
        try:
            # send ping message
            image, err = camera.read()
            if err is not None:
                logger.error(err)
            annoted, uvs = detector.get_landmarks(image)
            await ws.send(str(uvs))
        except Exception as e:
            logger.error(f"connection closed: {e}")
            break
    _dummy_sender_lock.release()


@bp.websocket("/dummy", name="detector_dummy")
async def websocket_dummy_handler(request, ws: WebsocketImplProtocol):
    task_name = f"receiver:{request.id}"
    # start sender task
    camera, detector = request.app.ctx.camera,request.app.ctx.detector
    request.app.add_task(_dummy_sender(ws, camera, detector), name=task_name)
    try:
        while True:
            await asyncio.sleep(86400)
    finally:
        request.app.purge_tasks()
