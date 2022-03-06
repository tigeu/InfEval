from ObjectDetectionAnalyzer.services.JSONService import JSONService


class LabelMapValidator:
    """
    Service that contains methods for validating an uploaded label map txt-file

    Attributes
    ----------
    json_service : JSONService
        Service for parsing JSON-files

    Methods
    -------
    is_valid(file_path)
        Parses the uploaded JSON-file and indicates whether it is valid
    """

    def __init__(self):
        """
        Initialise required services
        """
        self.json_service = JSONService()

    def is_valid(self, file_path):
        """
        Parses the uploaded JSON-file and indicates whether it is valid

        Parameters
        ----------
        file_path : Path
            Path of temporarily saved file

        Returns
        -------
        bool
            Indicates whether file is valid
        """
        try:
            values = self.json_service.read_label_map(file_path)
        except Exception:
            return False

        if values:
            return True

        return False
