from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.YoloService import YoloService


class YoloValidator:
    def __init__(self):
        self.yolo_service = YoloService()

    def is_valid(self, file_path, yolo_dir):
        image = self.create_test_image()

        try:
            self.yolo_service.get_detections_for_images(yolo_dir, file_path, [image])
        except Exception as e:
            print(e)
            return False

        return True

    def create_test_image(self):
        file = BytesIO()
        file.name = "test_image"
        image = Image.new('RGBA', size=(500, 500))
        image.save(file, 'png')
        image = Image.open(file)
        
        return image
