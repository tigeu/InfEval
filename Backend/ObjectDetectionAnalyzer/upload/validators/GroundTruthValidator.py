from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService


class GroundTruthValidator:
    def __init__(self):
        self.csv_parse_service = CSVParseService()

    def is_valid(self, file_path):
        indices = {'file_name': 0, 'class': 1, 'xmin': 2, 'ymin': 3, 'xmax': 4, 'ymax': 5}
        try:
            values = self.csv_parse_service.get_values(file_path, indices)
        except Exception:
            return False

        if values:
            return True

        return False
