import mediapipe
from mediapipe.tasks import python as python_tasks
from mediapipe.tasks.python import vision
import numpy as np
import cv2
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import os

class MediaPipeDetector:
    def __init__(self) -> None:
        # create detector
        self.base_options = python_tasks.BaseOptions(model_asset_path='pose_landmarker.task')
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(self.options)

    def get_landmarks(self, image: np.ndarray):
        image = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=image)
        detection_result = self.detector.detect(image)

        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = image.numpy_view()

        uvs = []
        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            uvs.append([(landmark.x, landmark.y) for landmark in pose_landmarks])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style()
            )

        return annotated_image, uvs