import numpy as np
import tensorflow as tf


class FilterPredictionsService:
    def get_interval_predictions(self, predictions, min_conf, max_conf):
        new_predictions = []
        for prediction in predictions:
            if min_conf <= prediction['confidence'] <= max_conf:
                new_predictions.append(prediction)

        return new_predictions

    def get_nms_predictions(self, predictions, iou, score):
        if not predictions:
            return []

        boxes, classes, scores = self.extract_lists_from_predictions(predictions)

        indices = tf.image.non_max_suppression(boxes, scores, 100, iou, score).numpy().tolist()

        nms_predictions = self.recreate_predictions(boxes, classes, scores, indices)
        return nms_predictions

    def extract_lists_from_predictions(self, image_predictions):
        boxes = []
        scores = []
        classes = []
        for pred in image_predictions:
            boxes.append([pred['ymin'], pred['xmin'], pred['ymax'], pred['xmax']])
            scores.append(pred['confidence'])
            classes.append(pred['class'])
        return boxes, classes, scores

    def recreate_predictions(self, boxes, classes, scores, indices):
        classes = np.array(classes)[indices].tolist()
        boxes = np.array(boxes)[indices].tolist()
        scores = np.array(scores)[indices].tolist()

        nms_image_predictions = []
        for class_, box, score_ in zip(classes, boxes, scores):
            nms_image_predictions.append({'class': class_,
                                          'confidence': score_,
                                          'xmin': box[1],
                                          'ymin': box[0],
                                          'xmax': box[3],
                                          'ymax': box[2]})
        return nms_image_predictions
