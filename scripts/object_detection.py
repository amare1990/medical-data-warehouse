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

    def detect_objects(self, image_path):
        """
        Perform object detection on an image.
        """
        img = cv2.imread(image_path)
        results = self.model(img)
        self.detection_results = results.pandas().xywh  # Extracting detection results as pandas DataFrame
        return self.detection_results

    def process_detection_results(self):
        """
        Extract relevant information such as bounding box, confidence score, and class label.
        """
        processed_data = []
        for _, row in self.detection_results.iterrows():
            data = {
                "class": row["name"],
                "confidence": row["confidence"],
                "bbox": {
                    "x_min": row["xmin"],
                    "y_min": row["ymin"],
                    "x_max": row["xmax"],
                    "y_max": row["ymax"]
                }
            }
            processed_data.append(data)
        return processed_data

    def log_detection(self, message):
        """
        Implement logging functionality.
        """
        logging.basicConfig(filename='detection_log.log', level=logging.INFO)
        logging.info(message)


    def store_to_database(self, processed_data, db_connection):
        """
        Store the processed detection results into a database.
        """
        try:
            for data in processed_data:
                db_connection.add_data(data)
            db_connection.commit()
            self.log_detection(f"Stored {len(processed_data)} detection results to the database.")
        except Exception as e:
            self.log_detection(f"Error storing data: {str(e)}")

