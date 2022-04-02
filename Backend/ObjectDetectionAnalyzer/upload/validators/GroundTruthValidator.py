from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.settings import GROUND_TRUTH_INDICES


class GroundTruthValidator:
    """
    Service that contains methods for validating an uploaded ground truth CSV-file

    Attributes
    ----------
    csv_parse_service : CSVParseService
        Service for parsing CSV-files

    Methods
    -------
    is_valid(file_path)
        Parses the uploaded CSV-file and returns its content if it is valid
    """

    def __init__(self):
        """
        Initialise required services
        """
        self.csv_parse_service = CSVParseService()

    def is_valid(self, file_path):
        """
        Parses the uploaded CSV-file and returns its content if it is valid

        Parameters
        ----------
        file_path : Path
            Path of temporarily saved file

        Returns
        -------
        list
            List with valid values. List is empty if file is invalid.
        """
        try:
            values = self.csv_parse_service.get_values(file_path, GROUND_TRUTH_INDICES)
        except Exception:
            return []

        if values:
            return values

        return []
