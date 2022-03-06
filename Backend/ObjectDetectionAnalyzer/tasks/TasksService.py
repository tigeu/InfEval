class TasksService:
    """
    Service that contains a method for replacing class indices with class names

    Methods
    -------
    replace_class_names(model_predictions, label_map)
        Replaces the class index with the class name from label map
    """

    def replace_class_names(self, model_predictions, label_map):
        """
        Replaces the class index with the class name from label map

        Parameters
        ----------
        model_predictions : list
            List of dictionaries, each representing a single prediction
        label_map : dict
            Dictionary with class indices as keys and the class names as values
        """
        for image_path, detections in model_predictions.items():
            for detection in detections:
                detection_class = str(int(detection['class']))
                if detection_class in label_map:
                    detection['class'] = label_map[detection_class]
