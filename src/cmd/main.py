import sys
sys.path.append('./')

import click
import argparse

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
@click.pass_context
def serve(ctx):
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=3000)
    args = parser.parse_args(sys.argv[2:])

    opt = CameraOption(use_depth=False)
    cam = KinectCamera("0", opt)
    detector = MediaPipeDetector()
    cam.open()

    controller_app.ctx.camera = cam
    controller_app.detector = detector
    controller_app.run(host="0.0.0.0", port=args.port, single_process=True, auto_reload=False, debug=True)


def entrypoint():
    cli()