from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.PyTorchService import PyTorchService


class PyTorchValidator:
    """
    Service that contains methods for validating an uploaded PyTorch model

    Attributes
    ----------
    pytorch_service : PyTorchService
        Service for running inference on PyTorch models

    Methods
    -------
    is_valid(file_path)
        Loads the uploaded model and indicates whether it is valid
    _create_test_image()
        Creates a dummy image with no content to test if inference is working
    """

    def __init__(self):
        """
        Initialise required services
        """
        self.pytorch_service = PyTorchService()

    def is_valid(self, file_path):
        """
        Loads the uploaded model and indicates whether it is valid

        Parameters
        ----------
        file_path : Path
            Path of uploaded Yolo model

        Returns
        -------
        bool
            Indicates whether model is valid
        """
        file = self._create_test_image()

        try:
            self.pytorch_service.get_detections_for_images(file_path, [file])
        except Exception:
            return False

        return True

    def _create_test_image(self):
        """
        Creates a dummy image with no content to test if inference is working

        Returns
        -------
        Image
            Dummy image for inference
        """
        file = BytesIO()
        file.name = "test_image"
        image = Image.new('RGBA', size=(500, 500))
        image.save(file, 'png')

        return file
