import torch

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks


class YoloService:
    """
    Service that provides methods for getting predictions from a given YOLO model

    Methods
    -------
    get_detections_for_task_images(yolo_dir, weight_path, image_paths, task)
        Retrieves predictions for given images from a given model updating a current task

    get_detections_for_images(yolo_dir, weight_path, image_paths)
        Retrieves predictions for given images from a given model. Used to validate an uploaded model

    _extract_predictions(self, results)
        Extracts predictions for a single image
    """

    def get_detections_for_task_images(self, yolo_dir, weight_path, image_paths, task):
        """
        Retrieves predictions for given images from a given model updating a current task

        Parameters
        ----------
        yolo_dir : Path
            Path of the yolo repository that should be used (v3 or v5)
        weight_path : Path
            Path of the model (weights) that should be used
        image_paths : list
            List of paths of all images that should be predicted
        task: Task
            Task object that should be updated indicating the progress

        Returns
        -------
        dict
            Dictionary with file name as key and a list of dictionaries as value, each representing a single prediction
        """
        model = torch.hub.load(yolo_dir, 'custom', path=weight_path, source='local')

        detections = {}
        progress_step = 100 / len(image_paths)
        for image_path in image_paths:
            results = model(image_path)
            detections[str(image_path)] = self._extract_predictions(
                results)  # use string to avoid unhashable exception
            task.progress = task.progress + progress_step
            if not Tasks.objects.filter(id=task.id):
                return None
            task.save()

        return detections

    def get_detections_for_images(self, yolo_dir, weight_path, image_paths):
        """
        Retrieves predictions for given images from a given model. Used to validate an uploaded model

        Parameters
        ----------        yolo_dir : Path
            Path of the yolo repository that should be used (v3 or v5)
        weight_path : Path
            Path of the model (weights) that should be used
        image_paths : list
            List of paths of all images that should be predicted

        Returns
        -------
        dict
            Dictionary with file name as key and a list of dictionaries as value, each representing a single prediction
        """
        model = torch.hub.load(yolo_dir, 'custom', path=weight_path, source='local')

        detections = {}
        for image_path in image_paths:
            results = model(image_path)
            detections[str(image_path)] = self._extract_predictions(
                results)  # use string to avoid unhashable exception

        return detections

    def _extract_predictions(self, results):
        """
       Read results coming directly from the model and convert them to a dictionary containing the rounded values.

       Parameters
       ----------
       results : DataFrame
           panadas Dataframe containing the prediction results

       Returns
       -------
       list
           List of dictionaries, each representing a single prediction
       """
        det = results.pandas().xyxy[0]
        predictions = []
        for name, conf, xmin, ymin, xmax, ymax in zip(det.name, det.confidence, det.xmin, det.ymin, det.xmax, det.ymax):
            prediction = {'class': name,
                          'confidence': conf,
                          'xmin': round(xmin),
                          'ymin': round(ymin),
                          'xmax': round(xmax),
                          'ymax': round(ymax)}
            if prediction['xmin'] < prediction['xmax'] and prediction['ymin'] < prediction['ymax']:
                predictions.append(prediction)

        return predictions
