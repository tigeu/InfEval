from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService


class PredictionsValidator:
    def __init__(self):
        self.csv_parse_service = CSVParseService()

    def is_valid(self, file_path):
        indices = {'file_name': 0, 'class': 1, 'confidence': 2, 'xmin': 3, 'ymin': 4, 'xmax': 5, 'ymax': 6}
        try:
            values = self.csv_parse_service.get_values(file_path, indices)
        except Exception:
            return False

        if values:
            return True

        return False
   