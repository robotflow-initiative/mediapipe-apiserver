import asyncio

from sanic import Blueprint
from sanic.server.websockets.impl import WebsocketImplProtocol

from loguru import logger

bp = Blueprint("detector", url_prefix="/detector", version=1)

async def _dummy_sender(ws: WebsocketImplProtocol):
    # get root service
    while True:
        try:
            # send ping message
            await ws.send("ping")
            await asyncio.sleep(2)  # wait for 120 seconds
        except Exception as e:
            logger.error(f"connection closed: {e}")
            break


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
