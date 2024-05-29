"""This scripts tests the availability of local camera
- open a kinect camera
- run capture/detector in sync mode
- display annotated images with opencv
"""
import cv2

import sys
sys.path.append('./')
from mediapipe_apiserver.camera import KinectCamera 
from mediapipe_apiserver.detector import MediaPipeDetector
from mediapipe_apiserver.common.option import CameraOption

from loguru import logger

def main():
    opt = CameraOption(use_depth=False)
    cam = KinectCamera("0", opt)
    detector = MediaPipeDetector()

    cam.open()
    cam.start()
    print(cam.get_intrinsics())

    cv2.namedWindow('Annoed Depth Image',cv2.WINDOW_NORMAL)
    try:
        while True:
            # Get capture
            image, err = cam.read()
            if err is not None:
                logger.error(err)
                break
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            annoed, uvs = detector.get_landmarks(image)
            annoed = cv2.cvtColor(annoed, cv2.COLOR_RGB2BGR)
            cv2.imshow('Annoed Depth Image', annoed)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'):  
                break
    except KeyboardInterrupt:
        print("Keyboard Interrupt Captured")
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    logger.info("Press Q to exit")
    main()