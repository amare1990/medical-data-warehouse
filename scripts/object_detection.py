import cv2
import torch
# import tensorflow as tf
import logging

class YoloObjectDetection:
    def __init__(self, model_type='yolov5'):
        self.model_type = model_type
        self.model = self.load_model()
        self.detection_results = []


    def load_model(self):
        """
        Load the YOLO model depending on the specified model type (PyTorch or TensorFlow).
        """
        if self.model_type == 'yolov5':
            return torch.hub.load('ultralytics/yolov5', 'yolov5s')  # for PyTorch-based YOLO
        elif self.model_type == 'tensorflow':
            return tf.saved_model.load("yolov4")  # for TensorFlow-based YOLO
        else:
            raise ValueError("Unsupported model type. Choose 'yolov5' or 'tensorflow'.")
