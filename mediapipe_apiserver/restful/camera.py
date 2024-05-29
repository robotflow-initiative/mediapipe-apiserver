from sanic import Blueprint, Sanic
from sanic.server.websockets.impl import WebsocketImplProtocol
from sanic.response import json as json_response
from sanic_ext import openapi
import http

from mediapipe_apiserver.common.datamodels import IntrinsicsMatrix


bp = Blueprint("camera", url_prefix="/camera", version=1)


@bp.get("/intrinsics", name="detector_dummy")
@openapi.definition(
    response=[
        openapi.definitions.Response(
            {'application/json': IntrinsicsMatrix.model_json_schema(ref_template="#/components/schemas/{model}")},
            status=200)
    ],
)
async def camera_intrinsics_handler(request) -> IntrinsicsMatrix:
    # start sender task
    camera, detector = request.app.ctx.camera,request.app.ctx.detector
    res: IntrinsicsMatrix = camera.get_intrinsics()
    return json_response(res.model_dump(), status=http.HTTPStatus.OK)
