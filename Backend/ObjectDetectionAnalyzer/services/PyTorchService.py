import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks


class PyTorchService:
    """
    Service that provides methods for getting predictions from a given tensorflow model

    Methods
    -------
    get_detections_for_task_images(model_path, image_paths, task)
        Retrieves predictions for given images from a given model updating a current task

    get_detections_for_images(model_path, image_paths)
        Retrieves predictions for given images from a given model. Used to validate an uploaded model

    _load_model(self, model_path, device)
        Loads the model

    _get_detections(self, model, device, image_path, transform)
        Retrieves all predictions for a given image

    _extract_predictions(self, outputs)
        Extracts predictions for a single image
    """

    def get_detections_for_task_images(self, model_path, image_paths, task):
        """
        Retrieves predictions for given images from a given model updating a current task

        Parameters
        ----------
        model_path : Path
            Path of the PyTorch model that should be used
        image_paths : list
            List of paths of all images that should be predicted
        task: Task
            Task object that should be updated indicating the progress

        Returns
        -------
        dict
            Dictionary with file name as key and a list of dictionaries as value, each representing a single prediction
        """
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = self._load_model(model_path, device)

        transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        detections = {}
        progress_step = 100 / len(image_paths)
        for image_path in image_paths:
            detections[image_path] = self._get_detections(model, device, image_path, transform)
            task.progress = task.progress + progress_step
            if not Tasks.objects.filter(id=task.id):
                return None
            task.save()

        return detections

    def get_detections_for_images(self, model_path, image_paths):
        """
        Retrieves predictions for given images from a given model. Used to validate an uploaded model

        Parameters
        ----------
        model_path : Path
            Path of the TensorFlow model that should be used
        image_paths : list
            List of paths of all images that should be predicted

        Returns
        -------
        dict
            Dictionary with file name as key and a list of dictionaries as value, each representing a single prediction
        """
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = self._load_model(model_path, device)

        transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        detections = {}
        for image_path in image_paths:
            detections[image_path] = self._get_detections(model, device, image_path, transform)

        return detections

    def _load_model(self, model_path, device):
        """
        Load PyTorch model

        Parameters
        ----------
        model_path : Path
            Path of the model that should be loaded
        device : str
            Indicating if cpu or gpu should be used

        Returns
        -------
        Model
            Loaded PyTorch model
        """
        model = torch.load(model_path)
        model.eval().to(device)
        return model

    def _get_detections(self, model, device, image_path, transform):
        """
        Retrieve predictions directly from the model and return extracted values.

        Parameters
        ----------
        model : Model
            Loaded PyTorch model
        device : str
            Indicating if cpu or gpu should be used
        image_path : Path
            Path of the image that should be predicted
        transform : Compose
            Composed function to transform image

        Returns
        -------
        list
            List of dictionaries, each representing a single prediction
        """
        image = Image.open(image_path).convert('RGB')
        image = transform(image).to(device)
        image = image.unsqueeze(0)

        with torch.no_grad():
            outputs = model(image)

        return self._extract_predictions(outputs)

    def _extract_predictions(self, outputs):
        """
        Read predictions coming directly from the model and convert them to a dictionary containing the rounded values.

        Parameters
        ----------
        outputs : list
            List with Dictionary as first item containing tensors for labels, scores and boxes

        Returns
        -------
        list
            List of dictionaries, each representing a single prediction
        """
        scores = list(outputs[0]['scores'].detach().cpu().numpy())
        bboxes = outputs[0]['boxes'].detach().cpu().numpy()
        boxes = bboxes.astype(np.float64)
        labels = outputs[0]['labels'].cpu().numpy()
        predictions = []
        for index in range(len(labels)):
            prediction = {'class': labels[index],
                          'confidence': scores[index],
                          'xmin': round(boxes[index][0]),
                          'ymin': round(boxes[index][1]),
                          'xmax': round(boxes[index][2]),
                          'ymax': round(boxes[index][3])}
            if prediction['xmin'] < prediction['xmax'] and prediction['ymin'] < prediction['ymax']:
                predictions.append(prediction)
        return predictions
