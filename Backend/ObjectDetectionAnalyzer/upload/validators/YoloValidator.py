from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.YoloService import YoloService


class YoloValidator:
    def __init__(self):
        self.yolo_service = YoloService()

    def is_valid(self, yolo_dir, file_path):
        file = BytesIO()
        file.name = "test_image"
        image = Image.new('RGBA', size=(500, 500))
        image.save(file, 'png')

        try:
            self.yolo_service.get_detections_for_images(yolo_dir, file_path, [file])
        except Exception:
            return False

        return True
