# MediaPipe API Server

## Get Started

```shell
pip install -r requirements.txt -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
```

Acquire ckpt for mmpose via https://github.com/open-mmlab/mmpose/tree/main/projects/rtmo and put it in `./ckpt`. After that, select the corresponding configuration file, the default configuration is for "rtmo-t_8xb32-600e_body7-416x416-f48f75cb_20231219.pth"

Start server

```shell
python -m mediapipe_apiserver serve
```

Start Client

```shell
wscat -c 127.0.0.1:3000/v1/dummy
python ./playground/test_ws_client.py
```

## TODO

- [√] update requirements
- [ ] raw image api, annotated image API
- [ ] client library
- [ ] add `__enter__` to camera class that supports `with` context

## Develope Guide

### Requirements

- A Azure Kinect camera.
- Azure Kinect SDK Installed. See [https://learn.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download](https://learn.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download).
- A Websocket debug tool, such as `wscat`(Run `npm -g install wscat` to install).

## Licenses

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project uses [MediaPipe](https://github.com/google/mediapipe), which is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
