import numpy as np
import tensorflow as tf
from PIL import Image

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks


class TensorFlowService:
    """
    Service that provides methods for getting predictions from a given tensorflow model

    Methods
    -------
    get_detections_for_task_images(model_path, image_paths, task, is_tensor_flow_1=False)
        Retrieves predictions for given images from a given model updating a current task

    get_detections_for_images(model_path, image_paths, is_tensor_flow_1=False)
        Retrieves predictions for given images from a given model. Used to validate an uploaded model

    _load_model(self, is_tensor_flow_1, model_path)
        Loads the saved model (takes ~30 second to load)

    _get_detections(self, saved_model, image_path)
        Retrieves all predictions for a given image

    _extract_predictions(self, predictions, image_width, image_height)
        Extracts predictions for a single image in absolute coordinates
    """

    def get_detections_for_task_images(self, model_path, image_paths, task, is_tensor_flow_1=False):
        """
        Retrieves predictions for given images from a given model updating a current task

        Parameters
        ----------
        model_path : Path
            Path of the TensorFlow model that should be used
        image_paths : list
            List of paths of all images that should be predicted
        task: Task
            Task object that should be updated indicating the progress
        is_tensor_flow_1 : bool
            Indicates whether the current model is TF1 or TF2

        Returns
        -------
        dict
            Dictionary with file name as key and a list of dictionaries as value, each representing a single prediction
        """
        saved_model = self._load_model(is_tensor_flow_1, model_path)

        detections = {}
        progress_step = 100 / len(image_paths)
        for image_path in image_paths:
            detections[image_path] = self._get_detections(saved_model, image_path)
            task.progress = task.progress + progress_step
            if not Tasks.objects.filter(id=task.id):
                return None
            task.save()

        return detections

    def get_detections_for_images(self, model_path, image_paths, is_tensor_flow_1=False):
        """
        Retrieves predictions for given images from a given model. Used to validate an uploaded model

        Parameters
        ----------
        model_path : Path
            Path of the TensorFlow model that should be used
        image_paths : list
            List of paths of all images that should be predicted
        is_tensor_flow_1 : bool
            Indicates whether the current model is TF1 or TF2

        Returns
        -------
        dict
            Dictionary with file name as key and a list of dictionaries as value, each representing a single prediction
        """
        saved_model = self._load_model(is_tensor_flow_1, model_path)

        detections = {}
        for image_path in image_paths:
            detections[image_path] = self._get_detections(saved_model, image_path)

        return detections

    def _load_model(self, is_tensor_flow_1, model_path):
        """
        Load TensorFlow model

        Parameters
        ----------
        is_tensor_flow_1 : bool
            Indicates whether the current model is TF1 or TF2
        model_path : Path
            Path of the model that should be loaded

        Returns
        -------
        Model
            Loaded TensorFlow model
        """
        saved_model = tf.saved_model.load(export_dir=model_path, tags=None)
        if is_tensor_flow_1:
            saved_model = saved_model.signatures['serving_default']
        return saved_model

    def _get_detections(self, saved_model, image_path):
        """
        Retrieve predictions directly from the model and return extracted values.

        Parameters
        ----------
        saved_model : Model
            Loaded TensorFlow model
        image_path : Path
            Path of the image that should be predicted

        Returns
        -------
        list
            List of dictionaries, each representing a single prediction
        """
        with Image.open(image_path) as image:
            image_width, image_height = image.size
            image_np = np.array(image)
            image_tensor = tf.convert_to_tensor(image_np)
            image_tensor = image_tensor[tf.newaxis, ...]

        predictions = saved_model(image_tensor)

        return self._extract_predictions(predictions, image_width, image_height)

    def _extract_predictions(self, predictions, image_width, image_height):
        """
        Read predictions coming directly from the model and convert them to a dictionary containing the absolute
        rounded values.

        Parameters
        ----------
        predictions : dict
            Dictionary containing tensors for detection_classes, detection_scores and detection_boxes
        image_width : int
            Width of current image
        image_height : int
            Height of current image

        Returns
        -------
        list
            List of dictionaries, each representing a single prediction
        """
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
