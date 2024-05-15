import cv2
import sys
sys.path.append('./')
from mediapipe_apiserver.camera import FileCamera  
from mediapipe_apiserver.detector import MediaPipeDetector
from mediapipe_apiserver.common.option import CameraOption
import os
from loguru import logger

def main():
    print('program started')
    opt = CameraOption(use_depth=False)
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.dirname(current_directory)
    new_directory = os.path.join(parent_directory, 'file_camera')

    cam = FileCamera(new_directory, opt)
    
    detector = MediaPipeDetector()
    
    cam.open()
    cam.start()
    
    cv2.namedWindow('File Image', cv2.WINDOW_NORMAL)
    
    try:
        while True:
            image, err = cam.read()
            if err is not None:
                logger.error(err)
                break
            annoed, uvs = detector.get_landmarks(image)
            cv2.imshow('Annotated Image', annoed)
            
            if cv2.waitKey(1) == ord('q'):
                break
    except KeyboardInterrupt:
        print("Keyboard Interrupt Captured")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        cam.close()  # 确保释放资源
        cv2.destroyAllWindows()
        print('program ended')

if __name__ == '__main__':
    logger.info("Press Q to exit")
    main()
