import cv2
import torch
# import tensorflow as tf
import logging

class YoloObjectDetection:
    def __init__(self, model_type='yolov5'):
        self.model_type = model_type
        self.model = self.load_model()
        self.detection_results = []
