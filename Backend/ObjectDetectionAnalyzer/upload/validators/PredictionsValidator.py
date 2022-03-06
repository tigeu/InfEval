from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService


class PredictionsValidator:
    """
    Service that contains methods for validating an uploaded prediction CSV-file

    Attributes
    ----------
    csv_parse_service : CSVParseService
        Service for parsing CSV-files

    Methods
    -------
    is_valid(file_path)
        Parses the uploaded CSV-file and indicates whether it is valid
    """

    def __init__(self):
        """
        Initialise required services
        """
        self.csv_parse_service = CSVParseService()

    def is_valid(self, file_path):
        """
        Parses the uploaded CSV-file and indicates whether it is valid

        Parameters
        ----------
        file_path : Path
            Path of temporarily saved file

        Returns
        -------
        bool
            Indicates whether file is valid
        """
        indices = {'file_name': 0, 'class': 1, 'confidence': 2, 'xmin': 3, 'ymin': 4, 'xmax': 5, 'ymax': 6}
        try:
            values = self.csv_parse_service.get_values(file_path, indices)
        except Exception:
            return False

        if values:
            return True

        return False
