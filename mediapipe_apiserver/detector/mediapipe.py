# This file uses MediaPipe, licensed under the Apache License, Version 2.0.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

from typing import Optional, List, Tuple
 
import numpy as np

import mediapipe
from mediapipe.tasks import python as python_tasks
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


class MediaPipeDetector:
    def __init__(self, model_asset_path: str = None) -> None:
        # create detector
        if model_asset_path is None or model_asset_path == "":
            model_asset_path = "assets/pose_landmarker_lite.task"
        self.base_options = python_tasks.BaseOptions(model_asset_path=model_asset_path)
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options, output_segmentation_masks=False,
            # running_mode=mediapipe.tasks.vision.RunningMode.VIDEO,
        )
        self.detector = vision.PoseLandmarker.create_from_options(self.options)

    def get_landmarks(self, image: np.ndarray, require_annotation=True) -> Tuple[Optional[np.ndarray], List[List[Tuple[float, float]]]]:
        # convert image format
        image = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=image)

        # run detection
        detection_result = self.detector.detect(image)

        pose_landmarks_list = detection_result.pose_landmarks

        # make a copy so that cv2 can draw on the image
        if require_annotation:
            annotated_image = np.copy(image.numpy_view())
        else:
            annotated_image = None

        uvs = []
        # loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x,
                        y=landmark.y,
                        z=landmark.visibility,
                    )
                    for landmark in pose_landmarks
                ]
            )
            # add to results
            uvs.append([(landmark.x, landmark.y, landmark.visibility) for landmark in pose_landmarks])
            
            # if require annotation
            if annotated_image is not None:
                solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    pose_landmarks_proto,
                    solutions.pose.POSE_CONNECTIONS,
                    solutions.drawing_styles.get_default_pose_landmarks_style(),
                )

        return annotated_image, uvs
