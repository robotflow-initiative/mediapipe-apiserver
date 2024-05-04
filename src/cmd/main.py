import click

from src.camera import KinectCamera 
from src.detector import MediaPipeDetector
from src.common.option import CameraOption
from src.restful import controller_app

from loguru import logger

@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option('--port', default=3000, help="listen port")
@click.option('--debug', default=False, help="toggle sanic debug")
@click.pass_context
def serve(ctx, port: int, debug: bool):
    opt = CameraOption(use_depth=False)
    cam = KinectCamera("0", opt)
    detector = MediaPipeDetector()
    cam.open()

    controller_app.ctx.camera = cam
    controller_app.ctx.detector = detector
    controller_app.run(host="0.0.0.0", port=port, single_process=True, auto_reload=False, debug=debug)


def entrypoint():
    cli()