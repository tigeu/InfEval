from io import BytesIO

from PIL import Image

from ObjectDetectionAnalyzer.services.YoloService import YoloService


class YoloValidator:
    """
    Service that contains methods for validating an uploaded Yolo model

    Attributes
    ----------
    yolo_service : YoloService
        Service for running inference on Yolo models

    Methods
    -------
    is_valid(file_path, yolo_dir)
        Loads the uploaded model with given yolo dir and indicates whether it is valid
    _create_test_image()
        Creates a dummy image with no content to test if inference is working
    """

    def __init__(self):
        """
        Initialise required services
        """
        self.yolo_service = YoloService()

    def is_valid(self, file_path, yolo_dir):
        """
        Loads the uploaded model with given yolo dir and indicates whether it is valid

        Parameters
        ----------
        file_path : Path
            Path of uploaded Yolo weights

        Returns
        -------
        bool
            Indicates whether model is valid
        """
        image = self._create_test_image()

        try:
            self.yolo_service.get_detections_for_images(yolo_dir, file_path, [image])
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
        image = Image.new('RGBA', size=(500, 500))
        image.save(file, 'png')
        image = Image.open(file)

        return image
