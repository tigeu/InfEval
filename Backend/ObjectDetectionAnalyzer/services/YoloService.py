import torch


class YoloService:
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
                          'xmin': xmin,
                          'ymin': ymin,
                          'xmax': xmax,
                          'ymax': ymax}
            if prediction['xmin'] < prediction['xmax'] and prediction['ymin'] < prediction['ymax']:
                predictions.append(prediction)

        return predictions
