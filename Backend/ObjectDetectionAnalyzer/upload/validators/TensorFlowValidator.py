from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.TensorFlowService import TensorFlowService


class TensorFlowValidator:
    def __init__(self):
        self.tensorflow_service = TensorFlowService()

    def is_valid(self, file_path, is_tensor_flow_1):
        file = self.create_test_image()

        try:
            self.tensorflow_service.get_detections_for_images(file_path, [file], is_tensor_flow_1)
        except Exception as e:
            print(e)
            return False

        return True

    def create_test_image(self):
        file = BytesIO()
        file.name = "test_image"
        image = Image.new('RGB', size=(500, 500))
        image.save(file, 'png')
        
        return file
