import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks


class PyTorchService:
    def get_detections_for_task_images(self, model_path, image_paths, task):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = self.load_model(model_path, device)

        transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        detections = {}
        progress_step = 100 / len(image_paths)
        for image_path in image_paths:
            detections[image_path] = self.get_detections(model, device, image_path, transform)
            task.progress = task.progress + progress_step
            # make sure task was deleted, even if instantly readded
            if not Tasks.objects.get(name=task.name, progress=task.progress - progress_step):
                return None
            task.save()

        return detections

    def get_detections_for_images(self, model_path, image_paths):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = self.load_model(model_path, device)

        transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        detections = {}
        for image_path in image_paths:
            detections[image_path] = self.get_detections(model, device, image_path, transform)

        return detections

    def load_model(self, model_path, device):
        model = torch.load(model_path)
        model.eval().to(device)
        return model

    def get_detections(self, model, device, image_path, transform):
        image = Image.open(image_path).convert('RGB')
        image = transform(image).to(device)
        image = image.unsqueeze(0)

        with torch.no_grad():
            outputs = model(image)

        return self.extract_predictions(outputs)

    def extract_predictions(self, outputs):
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
