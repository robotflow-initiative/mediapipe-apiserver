try:
    from .kinect_camera import KinectCamera
except:
    print("KinectCamera is not available")

try:
    from .zed_camera import ZED2Camera
except:
    print("ZED2Camera is not available")
