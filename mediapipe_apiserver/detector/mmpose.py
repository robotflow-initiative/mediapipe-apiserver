import time
from typing import Optional, List, Tuple

import numpy as np

import mmcv
import torch
from mmengine.config import Config, ConfigDict
from mmengine.infer.infer import ModelType
from mmengine.logging import print_log
from mmengine.model import revert_sync_batchnorm
from mmengine.registry import init_default_scope
from mmengine.structures import InstanceData
from mmpose.apis.inferencers import Pose2DInferencer
from mmpose.evaluation.functional import nearby_joints_nms, nms
from mmpose.registry import INFERENCERS
from mmpose.structures import merge_data_samples
import logging
from typing import Dict, List, Optional, Sequence, Tuple, Union


from rich.progress import track


class MyPoseInferencer(Pose2DInferencer):
    """Custom Pose Inferencer inheriting from Pose2DInferencer."""
    def select_instance(self,result,mode = 'bbox_score'):
        pred_instances = result.pred_instances.cpu().numpy()
        # print(pred_instances)
        if not hasattr(pred_instances, 'bboxes') or len(pred_instances.bboxes) == 0:
            
            return None

        # Option 1: Select by highest bbox score
        max_score_idx = np.argmax(pred_instances.bbox_scores)

        # Option 2: Select by largest bbox area
        bbox_areas = (pred_instances.bboxes[:, 2] - pred_instances.bboxes[:, 0]) * (pred_instances.bboxes[:, 3] - pred_instances.bboxes[:, 1])
        max_area_idx = np.argmax(bbox_areas)

        # Choose one of the options (here we choose by bbox score)
        if mode == 'bbox_score':
            selected_idx = max_score_idx
        else:
            selected_idx = max_area_idx
        # print(f"Selected instance: {selected_idx}")
        selected_instance = InstanceData(
            scores=pred_instances.scores[selected_idx:selected_idx+1],
            bboxes=pred_instances.bboxes[selected_idx:selected_idx+1],
            labels=pred_instances.labels[selected_idx:selected_idx+1],
            keypoints_visible=pred_instances.keypoints_visible[selected_idx:selected_idx+1],
            keypoints=pred_instances.keypoints[selected_idx:selected_idx+1],
            bbox_scores=pred_instances.bbox_scores[selected_idx:selected_idx+1],
            keypoint_scores=pred_instances.keypoint_scores[selected_idx:selected_idx+1]
        )
        return selected_instance
            
    def get_landmarks(self, image: np.ndarray, require_annotation=True, **kwargs) -> Tuple[Optional[np.ndarray], List[List[Tuple[float, float]]]]:
        """Get landmarks from image using pose estimation model."""
        kwargs = {
            key: value
            for key, value in kwargs.items()
            if key in set.union(self.inferencer.preprocess_kwargs,
                                self.inferencer.forward_kwargs,
                                self.inferencer.visualize_kwargs,
                                self.inferencer.postprocess_kwargs)
        }
        (
            preprocess_kwargs,
            forward_kwargs,
            visualize_kwargs,
            postprocess_kwargs,
        ) = self._dispatch_kwargs(**kwargs)
        super().update_model_visualizer_settings(**kwargs)
        inputs = super()._inputs_to_list(image)
        inputs = self.preprocess(inputs, batch_size=1, **preprocess_kwargs)
        
        for proc_inputs, ori_inputs in (track(inputs, description='Inference') if self.show_progress else inputs):
            preds = self.forward(proc_inputs, **forward_kwargs)
            # print(preds)
        for result in preds:
            # print(result.pred_instances.numpy())
            selected_instances =self.select_instance(result) 
        # print(selected_instances)
        if selected_instances is None:
            return image, []
        selected_instances = [inst for inst in selected_instances]
        uvs = []
        # print (preds)
        for instance in selected_instances:
            # print(instance)
            uvs.append([(keypoint[0], keypoint[1], keypoint[2]) for keypoint in instance.keypoints])

        annotated_image = np.copy(image) if require_annotation else None
        if require_annotation and annotated_image is not None:
            for result, instance in zip(preds, selected_instances):
                result.pred_instances = instance  # Update result with the selected instance
                annotated_image = self.visualizer.add_datasample(
                    'result', annotated_image, data_sample=result, draw_gt=False, draw_heatmap=False, draw_bbox=True, show_kpt_idx=False, skeleton_style='mmpose'
                )
        return annotated_image, uvs

   
class MMPoseDetector:
    def __init__(self, model_asset_path: str = None, model_config_path: str = None) -> None:
        if model_asset_path is None or model_asset_path == "":
            model_asset_path = r"ckpt\rtmo-t_8xb32-600e_body7-416x416-f48f75cb_20231219.pth"
            model_config_path = r"configs\body_2d_keypoint\rtmo\body7\rtmo-t_8xb32-600e_body7-416x416.py"      
        self.inferencer = MyPoseInferencer(
            model=model_config_path,
            weights=model_asset_path
        )  
    def get_landmarks(self, image: np.ndarray, require_annotation=True) -> Tuple[Optional[np.ndarray], List[List[Tuple[float, float]]]]:
        annotated_image, landmarks = self.inferencer.get_landmarks(image)
        return annotated_image, landmarks
        

