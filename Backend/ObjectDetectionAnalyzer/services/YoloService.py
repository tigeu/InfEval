import torch

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks


class YoloService:
    def get_detections_for_task_images(self, yolo_dir, weight_path, image_paths, task):
        model = torch.hub.load(yolo_dir, 'custom', path=weight_path, source='local')

        detections = {}
        progress_step = 100 / len(image_paths)
        for image_path in image_paths:
            results = model(image_path)
            detections[str(image_path)] = self.extract_predictions(results)  # use string to avoid unhashable exception
            task.progress = task.progress + progress_step
            # make sure task was deleted, even if instantly readded
            if not Tasks.objects.get(name=task.name, progress=task.progress - progress_step):
                return None
            task.save()

        return detections

    def get_detections_for_images(self, yolo_dir, weight_path, image_paths):
        model = torch.hub.load(yolo_dir, 'custom', path=weight_path, source='local')

        detections = {}
        for image_path in image_paths:
            results = model(image_path)
            detections[str(image_path)] = self.extract_predictions(results)  # use string to avoid unhashable exception

        return detections

    def extract_predictions(self, results):
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
