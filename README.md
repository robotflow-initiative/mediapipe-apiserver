# MediaPipe API Server

## TODO

- [ ] update requirements
- [ ] raw image api, annotated image API
1、发送坐标同时发送raw image图片,time stamp,capture的时间
.jpeg 图片
- [ ] client library
写一个类，connect read uvs
- [ ] add `__enter__` to camera class that supports `with` context

## Develope Guide

### Requirements

- A Azure Kinect camera.
- Azure Kinect SDK Installed. See [https://learn.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download](https://learn.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download).
- A Websocket debug tool, such as `wscat`(Run `npm -g install wscat` to install).

## Licenses

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project uses [MediaPipe](https://github.com/google/mediapipe), which is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
