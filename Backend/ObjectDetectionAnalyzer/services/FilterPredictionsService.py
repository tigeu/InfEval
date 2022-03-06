import numpy as np
import tensorflow as tf


class FilterPredictionsService:
    """
    Service that contains methods for interval and nms filtering.

    Methods
    -------
    get_interval_predictions(predictions, min_conf, max_conf)
        Returns a list of predictions in the given confidence interval
    get_nms_predictions(predictions, iou, score)
        Returns a list of predictions after applying non-max-suppression
    get_ground_truth_results(gts, predictions, iou)
        Update given ground truths indicating if that box was matched by a prediction for a given iou
    _extract_lists_from_predictions(image_predictions)
        Converts prediction list into lists of boxes, scores and classes
    _recreate_predictions(boxes, classes, scores, indices)
        Creates list of predictions from lists of boxes, scores and classes
    _calculate_iou(box1, box2)
        Calculate IoU for two given boxes
    _get_overlap_coordinates
        Get overlapping bounding box
    """

    def get_interval_predictions(self, predictions, min_conf, max_conf):
        """
        Returns a list of predictions in the given confidence interval

        Parameters
        ----------
        predictions : list
            List of dictionaries, each representing a single prediction
        min_conf : float
            Minimum confidence of prediction
        max_conf : float
            Maximum confidence of prediction

        Returns
        -------
        list
            List of dictionaries, each containing a single prediction
        """
        new_predictions = []
        for prediction in predictions:
            if min_conf <= prediction['confidence'] <= max_conf:
                new_predictions.append(prediction)

        return new_predictions

    def get_nms_predictions(self, predictions, iou, score):
        """
        Returns a list of predictions after applying non-max-suppression

        Parameters
        ----------
        predictions : list
            List of dictionaries, each representing a single prediction
        iou : float
            Minimum IoU that has to be scored
        score : float
            Minimum Score that the confidence has to exceed

        Returns
        -------
        list
            List of dictionaries, each containing a single prediction
        """
        if not predictions:
            return []

        boxes, classes, scores = self._extract_lists_from_predictions(predictions)

        indices = tf.image.non_max_suppression(boxes, scores, 100, iou, score).numpy().tolist()

        nms_predictions = self._recreate_predictions(boxes, classes, scores, indices)
        return nms_predictions

    def get_ground_truth_results(self, gts, predictions, iou):
        """
        Update given ground truths indicating if that box was matched by a prediction for a given iou

        Parameters
        ----------
        gts : list
            List of dictionaries, each representing a single ground truth
        predictions : list
            List of dictionaries, each representing a single prediction
        iou : float
            Minimum IoU that has to be scored

        Returns
        -------
        list
            List of dictionaries, each containing a single ground truth with an indication whether it was matched
        """
        gt_results = []
        predictions = sorted(predictions, key=lambda x: x['confidence'], reverse=True)
        for gt in gts:
            matched_pred = None
            for pred in predictions:
                if gt['class'] == pred['class'] and self._calculate_iou(gt, pred) >= iou:
                    gt_results.append({'matched': True,
                                       'xmin': gt['xmin'], 'xmax': gt['xmax'], 'ymin': gt['ymin'], 'ymax': gt['ymax']})
                    matched_pred = pred
            if matched_pred:
                predictions.remove(matched_pred)
            else:
                gt_results.append({'matched': False,
                                   'xmin': gt['xmin'], 'xmax': gt['xmax'], 'ymin': gt['ymin'], 'ymax': gt['ymax']})

        return gt_results

    def _extract_lists_from_predictions(self, image_predictions):
        """
        Converts prediction list into lists of boxes, scores and classes

        Parameters
        ----------
        image_predictions : list
            List of dictionaries, each representing a prediction

        Returns
        -------
        list
            List of bounding boxes
        list
            List of classes
        list
            List of scores
        """
        boxes = []
        scores = []
        classes = []
        for pred in image_predictions:
            boxes.append([pred['ymin'], pred['xmin'], pred['ymax'], pred['xmax']])
            scores.append(pred['confidence'])
            classes.append(pred['class'])
        return boxes, classes, scores

    def _recreate_predictions(self, boxes, classes, scores, indices):
        """
        Creates list of predictions from lists of boxes, scores and classes

        Parameters
        ----------
        boxes : list
            List of bounding boxes
        classes : list
            List of classes
        scores : list
            List of scores
        indices : list
            List of indices that should be considered

        Returns
        -------
        list
            List of dictionaries, each representing a prediction
        """
        classes = np.array(classes)[indices].tolist()
        boxes = np.array(boxes)[indices].tolist()
        scores = np.array(scores)[indices].tolist()

        nms_image_predictions = []
        for class_, box, score in zip(classes, boxes, scores):
            nms_image_predictions.append({'class': class_,
                                          'confidence': score,
                                          'xmin': box[1],
                                          'ymin': box[0],
                                          'xmax': box[3],
                                          'ymax': box[2]})
        return nms_image_predictions

    def _calculate_iou(self, box1, box2):
        """
        Calculate IoU for two given boxes

        Parameters
        ----------
        box1 : dict
            Dictionary containing coordinates
        box2 : dict
            Dictionary containing coordinates

        Returns
        -------
        float
            IoU
        """
        box = self._get_overlap_coordinates(box1, box2)

        width = box['xmax'] - box['xmin']
        height = box['ymax'] - box['ymin']
        overlap_area = width * height
        if width > 0 and height > 0:
            box1_area = (box1['xmax'] - box1['xmin']) * (box1['ymax'] - box1['ymin'])
            box2_area = (box2['xmax'] - box2['xmin']) * (box2['ymax'] - box2['ymin'])
            return overlap_area / (box1_area + box2_area - overlap_area)
        return 0.0

    def _get_overlap_coordinates(self, box1, box2):
        """
        Get overlapping bounding box

        Parameters
        ----------
        box1 : dict
            Dictionary containing coordinates
        box2 : dict
            Dictionary containing coordinates

        Returns
        -------
        dict
            Dictionary containing coordinates of overlapping box
        """
        xmin = max(box1['xmin'], box2['xmin'])
        ymin = max(box1['ymin'], box2['ymin'])
        xmax = min(box1['xmax'], box2['xmax'])
        ymax = min(box1['ymax'], box2['ymax'])
        return {'xmax': xmax, 'xmin': xmin, 'ymin': ymin, 'ymax': ymax}
