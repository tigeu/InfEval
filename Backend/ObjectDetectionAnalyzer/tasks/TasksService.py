class TasksService:
    def replace_class_names(self, model_predictions, label_map):
        for image_path, detections in model_predictions.items():
            for detection in detections:
                detection_class = str(int(detection['class']))
                if detection_class in label_map:
                    detection['class'] = label_map[detection_class]
