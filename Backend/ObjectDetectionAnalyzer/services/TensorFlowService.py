import numpy as np
import tensorflow as tf
from PIL import Image


class TensorFlowService:
    def get_detections_for_task_images(self, model_path, image_paths, task, is_tensor_flow_1=False):
        saved_model = self.load_model(is_tensor_flow_1, model_path)

        detections = {}
        progress_step = 100 / len(image_paths)
        for image_path in image_paths:
            detections[image_path] = self.get_detections(saved_model, image_path)
            task.progress = task.progress + progress_step
            task.save()

        return detections

    def get_detections_for_images(self, model_path, image_paths, is_tensor_flow_1=False):
        saved_model = self.load_model(is_tensor_flow_1, model_path)

        detections = {}
        for image_path in image_paths:
            detections[image_path] = self.get_detections(saved_model, image_path)

        return detections

    def load_model(self, is_tensor_flow_1, model_path):
        saved_model = tf.saved_model.load(export_dir=model_path, tags=None)
        if is_tensor_flow_1:
            saved_model = saved_model.signatures['serving_default']
        return saved_model

    def get_detections(self, saved_model, image_path):
        with Image.open(image_path) as image:
            image_width, image_height = image.size
            image_np = np.array(image)
            image_tensor = tf.convert_to_tensor(image_np)
            image_tensor = image_tensor[tf.newaxis, ...]

        predictions = saved_model(image_tensor)

        return self.extract_predictions(predictions, image_width, image_height)

    def extract_predictions(self, predictions, image_width, image_height):
        classes = predictions["detection_classes"][0][:].numpy()
        scores = predictions["detection_scores"][0][:].numpy()
        boxes = predictions["detection_boxes"][0][:].numpy()

        predictions = []
        for index in range(len(classes)):
            prediction = {'class': classes[index],
                          'confidence': scores[index],
                          'xmin': round(boxes[index][1] * image_width),
                          'ymin': round(boxes[index][0] * image_height),
                          'xmax': round(boxes[index][3] * image_width),
                          'ymax': round(boxes[index][2] * image_height)}
            if prediction['xmin'] < prediction['xmax'] and prediction['ymin'] < prediction['ymax']:
                predictions.append(prediction)

        return predictions
