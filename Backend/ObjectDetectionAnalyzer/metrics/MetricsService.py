import src.evaluators.pascal_voc_evaluator as pascal_voc_evaluator
from numpy import nan
from src.bounding_box import BoundingBox
from src.utils.enumerators import CoordinatesType, BBType, BBFormat, MethodAveragePrecision

from metric.review_object_detection_metrics.src.evaluators import coco_evaluator


class MetricsService:
    def calculate_pascal_voc(self, ground_truths, predictions, iou, classes):
        ground_truths = self.convert_ground_truths(ground_truths)
        predictions = self.convert_predictions(predictions)

        metrics = pascal_voc_evaluator.get_pascalvoc_metrics(ground_truths, predictions, iou, generate_table=False,
                                                             method=MethodAveragePrecision.ELEVEN_POINT_INTERPOLATION)

        results = {'mAP': self.get_percent(metrics['mAP']),
                   'classes': self.extract_results_per_class(classes, metrics['per_class'])}

        return results

    def calculate_coco(self, ground_truths, predictions, classes):
        ground_truths = self.convert_ground_truths(ground_truths)
        predictions = self.convert_predictions(predictions)

        summary = coco_evaluator.get_coco_summary(ground_truths, predictions)
        metrics = coco_evaluator.get_coco_metrics(ground_truths, predictions)

        results = {
            'summary': self.extract_coco_summary(summary),
            'classes': self.extract_results_per_class(classes, metrics, True)
        }

        return results

    def extract_results_per_class(self, classes, metrics, coco=False):
        results = {}
        for class_ in classes:
            if class_ not in metrics:
                continue

            class_results = metrics[class_]
            results[class_] = {}
            # prevent nan values
            results[class_]['AP'] = self.get_percent(class_results['AP']) if class_results['AP'] else -1
            results[class_]['positives'] = class_results['total positives'] if class_results['total positives'] else 0

            if coco:
                results[class_]['TP'] = class_results['TP'] if class_results['TP'] else 0
                results[class_]['FP'] = class_results['FP'] if class_results['FP'] else 0
            else:
                results[class_]['TP'] = class_results['total TP'] if class_results['total TP'] else 0
                results[class_]['FP'] = class_results['total FP'] if class_results['total FP'] else 0

        return results

    def extract_coco_summary(self, summary):
        result = {}
        for key, value in summary.items():
            if value is not nan:
                result[key] = self.get_percent(value)
            else:
                result[key] = -1

        return result

    def convert_ground_truths(self, gts):
        converted_gts = []
        for gt in gts:
            xmin, ymin, xmax, ymax = gt['xmin'], gt['ymin'], gt['xmax'], gt['ymax']
            box = BoundingBox(image_name=gt['file_name'], class_id=gt['class'], coordinates=(xmin, ymin, xmax, ymax),
                              type_coordinates=CoordinatesType.ABSOLUTE, bb_type=BBType.GROUND_TRUTH,
                              format=BBFormat.XYX2Y2)
            converted_gts.append(box)
        return converted_gts

    def convert_predictions(self, preds):
        converted_preds = []
        for pred in preds:
            xmin, ymin, xmax, ymax = pred['xmin'], pred['ymin'], pred['xmax'], pred['ymax']
            box = BoundingBox(image_name=pred['file_name'], class_id=pred['class'], confidence=pred['confidence'],
                              coordinates=(xmin, ymin, xmax, ymax), type_coordinates=CoordinatesType.ABSOLUTE,
                              bb_type=BBType.DETECTED, format=BBFormat.XYX2Y2)
            converted_preds.append(box)
        return converted_preds

    def get_percent(self, value):
        return round(value * 100, 2)
