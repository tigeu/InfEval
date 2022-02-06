from ObjectDetectionAnalyzer.services.JSONService import JSONService


class LabelMapValidator:
    def __init__(self):
        self.json_service = JSONService()

    def is_valid(self, file_path):
        try:
            values = self.json_service.read_label_map(file_path)
        except Exception:
            return False

        if values:
            return True

        return False
   