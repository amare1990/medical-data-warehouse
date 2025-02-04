import os
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
            return torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)  # for PyTorch-based YOLO
        # elif self.model_type == 'tensorflow':
        #     return tf.saved_model.load("yolov4")  # for TensorFlow-based YOLO
        else:
            raise ValueError("Unsupported model type. Choose 'yolov5' or 'tensorflow'.")

    def detect_objects(self, image_folder="../data/images/"):
        """
        Perform object detection on all images in the given folder.
        """
        if not os.path.exists(image_folder):
            print(f"The folder {image_folder} does not exist!")
            return []

        image_files = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

        if not image_files:
            print(f"No images found in {image_folder}.")
            return []

        all_results = {}

        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            print(f"Processing: {image_path}")

            img = cv2.imread(image_path)
            if img is None:
                print(f"Error: Could not read {image_path}. Skipping.")
                continue

            print("Image loaded successfully using cv2.")

            results = self.model(img)
            print(f"Results from model: {results}")

            self.detection_results = results.pandas().xyxy[0]  # Extract detection results as DataFrame
            all_results[image_file] = self.process_detection_results()

        return all_results  # Dictionary with image names as keys and detection results as values

    def process_detection_results(self):
        """
        Extract relevant information such as bounding box, confidence score, and class label.
        """
        if self.detection_results is None or self.detection_results.empty:
            print("No objects detected!")
            return []

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

