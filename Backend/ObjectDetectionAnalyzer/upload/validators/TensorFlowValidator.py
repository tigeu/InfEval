from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.TensorFlowService import TensorFlowService


class TensorFlowValidator:
    """
    Service that contains methods for validating an uploaded TensorFlow model

    Attributes
    ----------
    tensorflow_service : TensorFlowService
        Service for running inference on TensorFlow models

    Methods
    -------
    is_valid(file_path, is_tensorflow_1)
        Loads the uploaded model with given TensorFlow version and indicates whether it is valid
    _create_test_image()
        Creates a dummy image with no content to test if inference is working
    """

    def __init__(self):
        """
        Initialise required services
        """
        self.tensorflow_service = TensorFlowService()

    def is_valid(self, file_path, is_tensor_flow_1):
        """
        Loads the uploaded model with given TensorFlow version and indicates whether it is valid

        Parameters
        ----------
        file_path : Path
            Path of uploaded TensorFlow model
        is_tensor_flow_1 : bool
            Indicates whether model is TensorFlow 1 or TensorFlow 2

        Returns
        -------
        bool
            Indicates whether model is valid
        """
        file = self._create_test_image()

        try:
            self.tensorflow_service.get_detections_for_images(file_path, [file], is_tensor_flow_1)
        except Exception as e:
            print(e)
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
        image = Image.new('RGB', size=(500, 500))
        image.save(file, 'png')

        return file
