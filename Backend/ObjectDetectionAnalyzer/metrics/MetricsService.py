from numpy import nan
from src.bounding_box import BoundingBox
from src.evaluators import coco_evaluator
from src.evaluators import pascal_voc_evaluator
from src.utils.enumerators import CoordinatesType, BBType, BBFormat, MethodAveragePrecision


class MetricsService:
    """
    Service that contains methods for calculating pascal voc and coco detection metric

    Methods
    -------
    calculate_pascal_voc(ground_truths, predictions, iou, classes)
        Calculates pascal voc metric for given predictions
    calculate_coco(ground_truths, predictions, classes)
        Calculates coco detection metric for given predictions
    _extract_results_per_class(classes, metrics, coco=False)
        Extract results from metric calculation for each class
    _get_overall_positives(self, classes)
        Count all positives, true positives and false positives
    _extract_coco_summary(summary)
        Extract results from coco summary
    _convert_ground_truths(gts)
        Convert ground truth values from dictionaries to metric compatible form
    _convert_predictions(preds)
        Convert predictions values from dictionaries to metric compatible form
    _get_percent(value)
        Calculate percent values up to two digits
    """

    def calculate_pascal_voc(self, ground_truths, predictions, iou, classes):
        """
        Calculates coco detection metric for given predictions.

        Parameters
        ----------
        ground_truths : list
            List of dictionaries, each representing a single ground truth
        predictions : list
            List of dictionaries, each representing a single prediction
        iou : float
            Minium IoU value
        classes : list
            List of class names

        Returns
        -------
        dict
            Dictionary containing the most relevant values from pascal voc metric
        """
        ground_truths = self._convert_ground_truths(ground_truths)
        predictions = self._convert_predictions(predictions)

        metrics = pascal_voc_evaluator.get_pascalvoc_metrics(ground_truths, predictions, iou, generate_table=False,
                                                             method=MethodAveragePrecision.ELEVEN_POINT_INTERPOLATION)

        classes = self._extract_results_per_class(classes, metrics['per_class'])
        TP, FP, positives = self._get_overall_positives(classes)
        precision = self._get_percent(TP / positives) if positives > 0 else -1
        recall = self._get_percent(TP / (TP + FP)) if TP + FP > 0 else -1
        results = {'mAP': self._get_percent(metrics['mAP']),
                   'classes': classes,
                   'precision': precision,
                   'recall': recall,
                   'positives': positives,
                   'TP': TP,
                   'FP': FP}

        return results

    def calculate_coco(self, ground_truths, predictions, classes):
        """
        Calculates coco detection metric for given predictions.

        Parameters
        ----------
        ground_truths : list
            List of dictionaries, each representing a single ground truth
        predictions : list
            List of dictionaries, each representing a single prediction
        classes : list
            List of class names

        Returns
        -------
        dict
            Dictionary containing the most relevant values from coco metric
        """
        ground_truths = self._convert_ground_truths(ground_truths)
        predictions = self._convert_predictions(predictions)

        summary = coco_evaluator.get_coco_summary(ground_truths, predictions)
        metrics = coco_evaluator.get_coco_metrics(ground_truths, predictions)

        classes = self._extract_results_per_class(classes, metrics, True)
        TP, FP, positives = self._get_overall_positives(classes)
        precision = self._get_percent(TP / positives) if positives > 0 else -1
        recall = self._get_percent(TP / (TP + FP)) if TP + FP > 0 else -1
        results = {
            'summary': self._extract_coco_summary(summary),
            'classes': classes,
            'precision': precision,
            'recall': recall,
            'positives': positives,
            'TP': TP,
            'FP': FP
        }

        return results

    def _extract_results_per_class(self, classes, metrics, coco=False):
        """
        Extract results from metric calculation for each class.

        Parameters
        ----------
        classes : list
            List of class names
        metrics : dict
            Result of calculated metric
        coco : bool
            Indicates whether coco detection metric is calculated or pascal voc

        Returns
        -------
        dict
            Dictionary containing the most relevant values per class
        """
        results = {}
        for class_ in classes:
            if class_ not in metrics:
                continue

            class_results = metrics[class_]
            results[class_] = {}
            # prevent nan values
            results[class_]['AP'] = self._get_percent(class_results['AP']) if class_results['AP'] else -1
            results[class_]['positives'] = class_results['total positives'] if class_results['total positives'] else 0

            if coco:
                results[class_]['TP'] = class_results['TP'] if class_results['TP'] else 0
                results[class_]['FP'] = class_results['FP'] if class_results['FP'] else 0
            else:
                results[class_]['TP'] = class_results['total TP'] if class_results['total TP'] else 0
                results[class_]['FP'] = class_results['total FP'] if class_results['total FP'] else 0

            if results[class_]['TP'] > 0:
                results[class_]['precision'] = self._get_percent(
                    results[class_]['TP'] / (results[class_]['TP'] + results[class_]['FP']))
            else:
                results[class_]['precision'] = -1
            if results[class_]['positives'] > 0:
                results[class_]['recall'] = self._get_percent(results[class_]['TP'] / results[class_]['positives'])
            else:
                results[class_]['recall'] = -1

        return results

    def _get_overall_positives(self, classes):
        """
        Count all positives, true positives and false positives

        Parameters
        ----------
        classes : dict
            Dictionary containing the classes and the values for each class

        Returns
        -------
        int
            True positives
        int
            False positives
        int
            Positives
        """
        TP, FP, positives = 0, 0, 0
        for class_, values in classes.items():
            TP += values['TP']
            FP += values['FP']
            positives += values['positives']
        return TP, FP, positives

    def _extract_coco_summary(self, summary):
        """
        Extract results from coco summary.

        Parameters
        ----------
        summary : dict
            Dictionary containing the results in coco summary

        Returns
        -------
        dict
            Dictionary containing the most relevant values
        """
        result = {}
        for key, value in summary.items():
            if value is not nan:
                result[key] = self._get_percent(value)
            else:
                result[key] = -1

        return result

    def _convert_ground_truths(self, gts):
        """
        Convert ground truth values from dictionaries to metric compatible form.

        Parameters
        ----------
        gts : list
            List of dictionaries, each representing a single ground truth

        Returns
        -------
        list
            List of BoundingBox objects
        """
        converted_gts = []
        for gt in gts:
            xmin, ymin, xmax, ymax = gt['xmin'], gt['ymin'], gt['xmax'], gt['ymax']
            box = BoundingBox(image_name=gt['file_name'], class_id=gt['class'], coordinates=(xmin, ymin, xmax, ymax),
                              type_coordinates=CoordinatesType.ABSOLUTE, bb_type=BBType.GROUND_TRUTH,
                              format=BBFormat.XYX2Y2)
            converted_gts.append(box)
        return converted_gts

    def _convert_predictions(self, preds):
        """
        Convert predictions values from dictionaries to metric compatible form.

        Parameters
        ----------
        preds : list
            List of dictionaries, each representing a single prediction

        Returns
        -------
        list
            List of BoundingBox objects
        """
        converted_preds = []
        for pred in preds:
            xmin, ymin, xmax, ymax = pred['xmin'], pred['ymin'], pred['xmax'], pred['ymax']
            box = BoundingBox(image_name=pred['file_name'], class_id=pred['class'], confidence=pred['confidence'],
                              coordinates=(xmin, ymin, xmax, ymax), type_coordinates=CoordinatesType.ABSOLUTE,
                              bb_type=BBType.DETECTED, format=BBFormat.XYX2Y2)
            converted_preds.append(box)
        return converted_preds

    def _get_percent(self, value):
        """
        Calculate percent values up to two digits.

        Parameters
        ----------
        value : float
            Number that should be converted

        Returns
        -------
        float
            Converted value
        """
        return round(value * 100, 2)
