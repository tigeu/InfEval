from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.PyTorchService import PyTorchService


class PyTorchValidator:
    def __init__(self):
        self.pytorch_service = PyTorchService()

    def is_valid(self, file_path):
        file = self.create_test_image()

        try:
            self.pytorch_service.get_detections_for_images(file_path, [file])
        except Exception:
            return False

        return True

    def create_test_image(self):
        file = BytesIO()
        file.name = "test_image"
        image = Image.new('RGBA', size=(500, 500))
        image.save(file, 'png')
        
        return file
