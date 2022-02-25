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

    def get_ground_truth_results(self, gts, predictions, iou):
        gt_results = []
        predictions = sorted(predictions, key=lambda x: x['confidence'], reverse=True)
        for gt in gts:
            matched_pred = None
            for pred in predictions:
                if gt['class'] == pred['class'] and self.calculate_iou(gt, pred) >= iou:
                    gt_results.append({'matched': True,
                                       'xmin': gt['xmin'], 'xmax': gt['xmax'], 'ymin': gt['ymin'], 'ymax': gt['ymax']})
                    matched_pred = pred
            if matched_pred:
                predictions.remove(matched_pred)
            else:
                gt_results.append({'matched': False,
                                   'xmin': gt['xmin'], 'xmax': gt['xmax'], 'ymin': gt['ymin'], 'ymax': gt['ymax']})

        return gt_results

    def calculate_iou(self, box1, box2):
        box = self.get_overlap_coordinates(box1, box2)

        width = box['xmax'] - box['xmin']
        height = box['ymax'] - box['ymin']
        overlap_area = width * height
        if width > 0 and height > 0:
            box1_area = (box1['xmax'] - box1['xmin']) * (box1['ymax'] - box1['ymin'])
            box2_area = (box2['xmax'] - box2['xmin']) * (box2['ymax'] - box2['ymin'])
            return overlap_area / (box1_area + box2_area - overlap_area)
        return 0.0

    def get_overlap_coordinates(self, box1, box2):
        xmin = max(box1['xmin'], box2['xmin'])
        ymin = max(box1['ymin'], box2['ymin'])
        xmax = min(box1['xmax'], box2['xmax'])
        ymax = min(box1['ymax'], box2['ymax'])
        return {'xmax': xmax, 'xmin': xmin, 'ymin': ymin, 'ymax': ymax}
