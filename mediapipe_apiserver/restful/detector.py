import asyncio
from asyncio import Lock

from sanic import Blueprint, Sanic
from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.connection import State

from loguru import logger

bp = Blueprint("detector", url_prefix="/detector", version=1)

_dummy_sender_lock = Lock()


async def _dummy_sender(ws: WebsocketImplProtocol, camera, detector):
    # get root service
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



@bp.websocket("/dummy", name="detector_dummy")
async def websocket_dummy_handler(request, ws: WebsocketImplProtocol):
    task_name = f"receiver:{request.id}"
    # start sender task
    camera, detector = request.app.ctx.camera,request.app.ctx.detector
    _app: Sanic = request.app
    try:
        await _dummy_sender_lock.acquire()
        _app.add_task(_dummy_sender(ws, camera, detector), name=task_name)
        while True:
            if ws.ws_proto.state in (State.CLOSED, State.CLOSING):
                break
            else:
                await asyncio.sleep(1)
    finally:
        ws.close()
        ws.wait_for_connection_lost()
        _app.cancel_task(task_name)
        _dummy_sender_lock.release()
        _app.purge_tasks()
