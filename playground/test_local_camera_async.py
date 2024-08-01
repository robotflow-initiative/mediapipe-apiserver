"""This scripts tests the availability of local camera
- open a kinect camera
- run capture/detector in sync mode
- display annotated images with opencv
"""
import cv2

import sys
sys.path.append('./')
from mediapipe_apiserver.camera import AsyncCamera
# from mediapipe_apiserver.camera import KinectCamera 
from mediapipe_apiserver.camera import ZED2Camera
from mediapipe_apiserver.detector import MediaPipeDetector,MMPoseDetector
from mediapipe_apiserver.common.option import CameraOption

from loguru import logger
from tqdm import tqdm

def main():
    opt = CameraOption(use_depth=False)
    base_cam = ZED2Camera("0", opt)
    cam = AsyncCamera(base_cam)
    # detector = MediaPipeDetector()
    detector = MMPoseDetector()

    cam.open()
    cam.start()
    # print(cam.get_intrinsics())

    cv2.namedWindow('RAW Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Annoed Image', cv2.WINDOW_NORMAL)
    try:
        with tqdm() as pbar:
            while True:
                # Get capture
                image, err = cam.read()
                # print(image.shape)
                if err is not None:
                    logger.error(err)
                    break
                cv2.imshow('RAW Image', image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                annoed, uvs = detector.get_landmarks(image)
                annoed = cv2.cvtColor(annoed, cv2.COLOR_RGB2BGR)
                cv2.imshow('Annoed Image', annoed)
                # Press q key to stop
                if cv2.waitKey(1) == ord('q'):  
                    break
                pbar.update()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Captured")
        cam.stop()
        cam.close()
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    logger.info("Press Q to exit")
    main()